"""Run inference against any agent HTTP endpoint — agent-agnostic.

POSTs a templated JSON body per benchmark instance and extracts the answer
from the response. The body template and headers come from a named preset
(``--preset``), an inline ``--body`` template, or both — any ``{placeholder}``
in the template is filled per request:

    {message}      benchmark prompt (question + options)
    {message_id}   unique id per request (``bench-<instance>-<uuid8>``)
    {chat_id}      unique conversation id per request
    {instance_id}  benchmark instance id
    {<key>}        required variable — ``--var key=value`` or the preset's env map
    {<key>?}       optional variable — the field is dropped when unset

``$VAR``/``${VAR}`` environment references in templates and headers are
expanded first, so secrets stay out of command lines.

Response handling is generic too: for JSON responses, ``--response_field``
is a dotted path to the answer text (e.g. ``choices.0.message.content``);
``--error_field`` (default ``error``) marks an error field that raises when
present. Non-JSON bodies are returned as-is.

Usage (any endpoint):

    python -m brokerbench.inference.run_http \
        --endpoint http://localhost:8080/chat \
        --body '{"input": "{message}"}' \
        --header 'Authorization: Bearer $MY_AGENT_TOKEN' \
        --response_field text \
        --dataset all --output_file predictions/my-agent.jsonl

Usage (BrokerBot's V2 agent gateway via the built-in preset):

    python -m brokerbench.inference.run_http \
        --preset brokerbot \
        --var team_id=<team-uuid> --var user_id=<user-id> \
        --var agent_id=<agent-uuid> --var auth_token=<jwt> \
        --dataset all --output_file predictions/brokerbot.jsonl
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import uuid
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from rich.console import Console

from brokerbench.harness.types import Instance, Prediction
from brokerbench.inference import build_prompt, load_instances
from brokerbench.inference.run_api import _max_concurrency, _run_instances

console = Console()

_REQUEST_TIMEOUT = 300  # agent turns can run multi-step tool loops

_PLACEHOLDER_RE = re.compile(r"\{([a-zA-Z_][a-zA-Z0-9_]*)\??\}")


class _Drop:
    """Sentinel: remove this field from the rendered template."""


_DROP = _Drop()


class _UnsetOptionalError(Exception):
    """Internal: an unset ``{key?}`` drops the enclosing field."""


@dataclass
class EndpointPreset:
    """A bundled endpoint config: body/headers templates, env var names."""

    name: str
    endpoint_default: str
    endpoint_env: str
    body: dict[str, Any]
    headers: dict[str, str]
    response_field: str | None
    error_field: str | None
    vars_env: dict[str, str] = field(default_factory=dict)
    vars_default: dict[str, str] = field(default_factory=dict)


# Named endpoint configs. Each var may also be set via --var key=value or
# the env var listed in vars_env.
PRESETS: dict[str, EndpointPreset] = {
    # BrokerBot's V2 agent gateway POST /generate — the channel pipeline
    # Slack/SMS/web chat use. Auth: HS256 JWT signed with BETTER_AUTH_SECRET
    # (claims teamId + agentId, or userId+teamSlug+chatId) or a raw Better
    # Auth session token, sent as Bearer.
    "brokerbot": EndpointPreset(
        name="brokerbot",
        endpoint_default="http://localhost:4200/generate",
        endpoint_env="BROKERBOT_GATEWAY_URL",
        body={
            "teamId": "{team_id}",
            "userId": "{user_id}",
            "agentId": "{agent_id?}",
            "channel": "{channel}",
            "messageText": "{message}",
            "messageId": "{message_id}",
            "chatId": "{chat_id}",
        },
        headers={
            "Accept": "application/json",
            "Authorization": "Bearer {auth_token?}",
        },
        response_field="text",
        error_field="error",
        vars_env={
            "team_id": "BROKERBOT_TEAM_ID",
            "user_id": "BROKERBOT_USER_ID",
            "agent_id": "BROKERBOT_AGENT_ID",
            "channel": "BROKERBOT_CHANNEL",
            "auth_token": "BROKERBOT_AUTH_TOKEN",
        },
        vars_default={"channel": "web"},
    ),
}


def _resolve_template(obj: Any, ctx: dict[str, Any]) -> Any:
    """Fill ``{key}`` placeholders in a JSON-shaped template.

    ``{key}`` placeholders substitute inline; ``{key}?`` removes the
    enclosing field when the key is unset (whether it is the whole value
    or embedded in a longer string, e.g. ``"Bearer {tok?}"``). Raises
    ``KeyError`` for an unset required placeholder.
    """
    if isinstance(obj, dict):
        out: dict[str, Any] = {}
        for k, v in obj.items():
            resolved = _resolve_template(v, ctx)
            if resolved is not _DROP:
                out[k] = resolved
        return out
    if isinstance(obj, list):
        return [r for v in obj if (r := _resolve_template(v, ctx)) is not _DROP]
    if isinstance(obj, str):
        obj = os.path.expandvars(obj)
        whole = _PLACEHOLDER_RE.fullmatch(obj)
        if whole:
            key = whole.group(1)
            if key in ctx:
                return ctx[key]
            if whole.group(0).endswith("?}"):
                return _DROP
            raise KeyError(f"missing required variable: {key}")

        def sub(match: re.Match[str]) -> str:
            key = match.group(1)
            if key in ctx:
                return str(ctx[key])
            if match.group(0).endswith("?}"):
                raise _UnsetOptionalError
            raise KeyError(f"missing required variable: {key}")

        try:
            return _PLACEHOLDER_RE.sub(sub, obj)
        except _UnsetOptionalError:
            return _DROP
    return obj


def _dig(data: Any, path: str) -> Any:
    """Walk a dotted path into nested dicts/lists (``a.0.b``)."""
    for part in path.split("."):
        if isinstance(data, list):
            data = data[int(part)]
        elif isinstance(data, dict):
            data = data[part]
        else:
            raise KeyError(f"cannot descend into {part!r} of {path!r}")
    return data


def _make_predict(
    endpoint: str,
    body_template: dict[str, Any],
    headers: dict[str, str],
    variables: dict[str, str],
    response_field: str | None,
    error_field: str | None,
    timeout: int,
) -> Callable[[Instance], str]:
    def predict(instance: Instance) -> str:
        ctx: dict[str, Any] = {
            **variables,
            "message": build_prompt(instance),
            "message_id": f"bench-{instance.instance_id}-{uuid.uuid4().hex[:8]}",
            "chat_id": str(uuid.uuid4()),
            "instance_id": instance.instance_id,
        }
        body = _resolve_template(body_template, ctx)
        resolved_headers = _resolve_template(headers, ctx)
        resolved_headers.setdefault("Content-Type", "application/json")

        req = Request(
            endpoint,
            data=json.dumps(body).encode("utf-8"),
            headers=resolved_headers,
            method="POST",
        )
        with urlopen(req, timeout=timeout) as resp:
            ctype = resp.headers.get("Content-Type", "")
            raw: str = resp.read().decode("utf-8")

        if "application/json" in ctype:
            data = json.loads(raw)
            if isinstance(data, dict):
                if error_field and data.get(error_field):
                    raise RuntimeError(str(data[error_field]))
                if response_field:
                    return str(_dig(data, response_field))
                if "text" in data:
                    return str(data["text"])
        return raw

    return predict


def run_http(
    instances: list[Instance],
    endpoint: str,
    output_path: Path,
    model_name: str,
    body_template: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
    variables: dict[str, str] | None = None,
    response_field: str | None = None,
    error_field: str | None = None,
    timeout: int = _REQUEST_TIMEOUT,
    max_concurrency: int = 8,
) -> list[Prediction]:
    """Run inference against an arbitrary agent HTTP endpoint."""
    return _run_instances(
        instances,
        model_name,
        output_path,
        _make_predict(
            endpoint,
            body_template or {"message": "{message}"},
            headers or {},
            variables or {},
            response_field,
            error_field,
            timeout,
        ),
        max_concurrency,
    )


def _parse_body_template(raw: str) -> dict[str, Any]:
    """Parse an inline JSON template or an @file reference."""
    text = Path(raw[1:]).read_text() if raw.startswith("@") else raw
    parsed = json.loads(text)
    if not isinstance(parsed, dict):
        raise ValueError("--body must be a JSON object")
    return parsed


def _parse_header(raw: str) -> tuple[str, str]:
    """Parse a ``Name: value`` header argument."""
    name, sep, value = raw.partition(":")
    if not sep or not name.strip():
        raise ValueError(f"invalid header {raw!r} — expected 'Name: value'")
    return name.strip(), value.strip()


def _parse_var(raw: str) -> tuple[str, str]:
    """Parse a ``key=value`` variable argument."""
    key, sep, value = raw.partition("=")
    if not sep or not key.strip():
        raise ValueError(f"invalid variable {raw!r} — expected 'key=value'")
    return key.strip(), value


def main() -> None:
    """CLI entry point for generic HTTP agent inference."""
    parser = argparse.ArgumentParser(
        description="Run any agent HTTP endpoint against the BrokerBench benchmark."
    )
    parser.add_argument(
        "--preset",
        type=str,
        choices=sorted(PRESETS),
        default=None,
        help="Named endpoint config (bundles body/headers/response field).",
    )
    parser.add_argument(
        "--endpoint",
        type=str,
        default=None,
        help="Agent endpoint URL (or BROKERBENCH_AGENT_URL / preset default).",
    )
    parser.add_argument(
        "--body",
        type=str,
        default=None,
        help="JSON body template, or @path/to/template.json. "
        "Placeholders: {message} {message_id} {chat_id} {instance_id} {var} {var?}.",
    )
    parser.add_argument(
        "--header",
        type=str,
        action="append",
        default=[],
        help="Request header as 'Name: value' (repeatable; $ENV vars expand).",
    )
    parser.add_argument(
        "--response_field",
        type=str,
        default=None,
        help="Dotted path to the answer text in a JSON response "
        "(e.g. text, choices.0.message.content).",
    )
    parser.add_argument(
        "--error_field",
        type=str,
        default=None,
        help="JSON field that marks an error when set (preset default: error).",
    )
    parser.add_argument(
        "--var",
        type=str,
        action="append",
        default=[],
        dest="variables",
        help="Template variable as 'key=value' (repeatable).",
    )
    parser.add_argument(
        "--name",
        type=str,
        default=None,
        help="Model name recorded on predictions (default: preset or 'http-agent').",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=_REQUEST_TIMEOUT,
        help="Per-request timeout in seconds.",
    )
    parser.add_argument(
        "--dataset",
        type=str,
        default="all",
        help="Dataset name or path, or 'all' for all built-in datasets.",
    )
    parser.add_argument(
        "--max_concurrency",
        type=int,
        default=None,
        help="Max concurrent requests (default 8, or BROKERBENCH_MAX_CONCURRENCY).",
    )
    parser.add_argument(
        "--output_file",
        type=Path,
        required=True,
        help="Path to write prediction JSONL file.",
    )
    args = parser.parse_args()

    preset = PRESETS[args.preset] if args.preset else None

    endpoint = (
        args.endpoint
        or os.environ.get("BROKERBENCH_AGENT_URL")
        or (preset and os.environ.get(preset.endpoint_env))
        or (preset and preset.endpoint_default)
    )
    if not endpoint:
        console.print("[red]--endpoint is required (or BROKERBENCH_AGENT_URL / a preset)[/red]")
        sys.exit(1)

    variables: dict[str, str] = {}
    if preset:
        variables.update(preset.vars_default)
        for key, env_name in preset.vars_env.items():
            if os.environ.get(env_name):
                variables[key] = os.environ[env_name]
    for raw in args.variables:
        key, value = _parse_var(raw)
        variables[key] = value

    body_template: dict[str, Any] | None = None
    try:
        if args.body:
            body_template = _parse_body_template(args.body)
        elif preset:
            body_template = preset.body
        if body_template is None:
            body_template = {"message": "{message}"}
    except (ValueError, OSError, json.JSONDecodeError) as e:
        console.print(f"[red]Invalid --body: {e}[/red]")
        sys.exit(1)

    headers = dict(preset.headers) if preset else {}
    for raw in args.header:
        key, value = _parse_header(raw)
        headers[key] = value

    response_field = args.response_field
    error_field = args.error_field
    if preset:
        response_field = response_field or preset.response_field
        error_field = error_field if error_field is not None else preset.error_field
    if error_field is None:
        error_field = "error"

    model_name = args.name or (preset.name if preset else "http-agent")

    instances = load_instances(args.dataset)
    console.print(f"Loaded {len(instances)} instances")

    try:
        run_http(
            instances,
            endpoint,
            args.output_file,
            model_name,
            body_template=body_template,
            headers=headers,
            variables=variables,
            response_field=response_field,
            error_field=error_field,
            timeout=args.timeout,
            max_concurrency=_max_concurrency(args.max_concurrency),
        )
    except (HTTPError, URLError) as e:
        console.print(f"[red]Fatal: {e}[/red]")
        sys.exit(1)
    except KeyError as e:
        console.print(f"[red]Template error: {e}[/red]")
        sys.exit(1)
    console.print(f"[green]Predictions written to {args.output_file}[/green]")


if __name__ == "__main__":
    main()
