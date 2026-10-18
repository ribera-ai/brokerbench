"""Run inference against any agent HTTP endpoint — agent-agnostic.

POSTs a templated JSON body per benchmark instance and extracts the answer
from the response. The body template comes from ``--body`` (inline JSON or
``@file``) and headers from repeatable ``--header`` flags — any
``{placeholder}`` in them is filled per request:

    {message}      benchmark prompt (question + options)
    {message_id}   unique id per request (``bench-<instance>-<uuid8>``)
    {chat_id}      unique conversation id per request
    {instance_id}  benchmark instance id
    {<key>}        required variable — pass ``--var key=value``
    {<key>?}       optional variable — the field is dropped when unset

``$VAR``/``${VAR}`` environment references in templates and headers are
expanded first, so secrets stay out of command lines.

Response handling is generic too: for JSON responses, ``--response_field``
is a dotted path to the answer text (e.g. ``choices.0.message.content``);
``--error_field`` (default ``error``) marks an error field that raises when
present; ``--metadata_field`` copies extra response fields into prediction
metadata. Non-JSON bodies are returned as-is.

Usage:

    python -m brokerbench.inference.run_http \
        --endpoint http://localhost:8080/chat \
        --body '{"input": "{message}"}' \
        --header 'Authorization: Bearer $MY_AGENT_TOKEN' \
        --response_field text \
        --dataset all --output_file predictions/my-agent.jsonl
"""

from __future__ import annotations

import argparse
import ipaddress
import json
import os
import re
import sys
import uuid
from collections.abc import Callable
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener

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


# Placeholders the runner generates per request; everything else in a
# template is a required or optional --var.
_BUILTIN_VARS = {"message", "message_id", "chat_id", "instance_id"}

_SENSITIVE_HEADERS = {"authorization", "cookie", "proxy-authorization"}


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


def _required_vars(*templates: Any) -> set[str]:
    """Required (non-optional) placeholder names in a template."""
    out: set[str] = set()

    def walk(obj: Any) -> None:
        if isinstance(obj, dict):
            for v in obj.values():
                walk(v)
        elif isinstance(obj, list):
            for v in obj:
                walk(v)
        elif isinstance(obj, str):
            # Env refs ($VAR/${VAR}) expand at render time — scan the
            # expanded text so they are not demanded as --var variables.
            for m in _PLACEHOLDER_RE.finditer(os.path.expandvars(obj)):
                if not m.group(0).endswith("?}") and m.group(1) not in _BUILTIN_VARS:
                    out.add(m.group(1))

    for t in templates:
        walk(t)
    return out


def _is_local_host(hostname: str) -> bool:
    """Whether a host is loopback-only (localhost, 127/8, ::1, localtest.me).

    Private-network addresses (10/8, 192.168/16, …) are not local: requests
    to them still cross a network in plaintext, so they require
    ``--allow_insecure_http`` like any remote host.
    """
    host = hostname.lower()
    if host in {"localhost", "ip6-localhost"} or host.endswith(".localtest.me"):
        return True
    try:
        ip = ipaddress.ip_address(host)
    except ValueError:
        return False
    return ip.is_loopback


class _SensitiveHeaderRedirectHandler(HTTPRedirectHandler):
    """Redirect handler that strips credentials when the host changes."""

    def redirect_request(
        self,
        req: Request,
        fp: Any,
        code: int,
        msg: str,
        headers: Any,
        newurl: str,
    ) -> Request | None:
        new_req = super().redirect_request(req, fp, code, msg, headers, newurl)
        if new_req is None:
            return None
        if urlparse(newurl).netloc.lower() != urlparse(req.full_url).netloc.lower():
            for name in list(new_req.headers):
                if name.lower() in _SENSITIVE_HEADERS:
                    del new_req.headers[name]
        return new_req


_opener = build_opener(_SensitiveHeaderRedirectHandler())


def _make_predict(
    endpoint: str,
    body_template: dict[str, Any],
    headers: dict[str, str],
    variables: dict[str, str],
    response_field: str | None,
    error_field: str | None,
    metadata_fields: list[str],
    timeout: int,
) -> Callable[[Instance], str | tuple[str, dict[str, str]]]:
    def predict(instance: Instance) -> str | tuple[str, dict[str, str]]:
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
        with _opener.open(req, timeout=timeout) as resp:
            ctype = resp.headers.get("Content-Type", "")
            raw: str = resp.read().decode("utf-8")

        metadata: dict[str, str] = {}
        if "json" in ctype.lower():
            data = json.loads(raw)
            if isinstance(data, dict) and error_field and data.get(error_field):
                raise RuntimeError(str(data[error_field]))
            for field_path in metadata_fields:
                try:
                    dug = _dig(data, field_path)
                    metadata[field_path] = dug if isinstance(dug, str) else json.dumps(dug)
                except (KeyError, IndexError, TypeError, ValueError):
                    pass
            if response_field:
                text = str(_dig(data, response_field))
            elif isinstance(data, dict) and "text" in data:
                text = str(data["text"])
            else:
                text = raw
            return (text, metadata) if metadata_fields else text
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
    metadata_fields: list[str] | None = None,
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
            metadata_fields or [],
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
        "--endpoint",
        type=str,
        default=None,
        help="Agent endpoint URL (or BROKERBENCH_AGENT_URL).",
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
        help="JSON field that marks an error when set (default: error).",
    )
    parser.add_argument(
        "--metadata_field",
        type=str,
        action="append",
        default=[],
        help="Dotted path to copy from the JSON response into prediction "
        "metadata (repeatable; e.g. usage, steps).",
    )
    parser.add_argument(
        "--allow_insecure_http",
        action="store_true",
        help="Allow http:// endpoints on non-local hosts (tokens go over "
        "plaintext). Local hosts are always allowed.",
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
        help="Model name recorded on predictions (default 'http-agent').",
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

    endpoint = args.endpoint or os.environ.get("BROKERBENCH_AGENT_URL")
    if not endpoint:
        console.print("[red]--endpoint is required (or BROKERBENCH_AGENT_URL)[/red]")
        sys.exit(1)

    variables: dict[str, str] = {}
    for raw in args.variables:
        key, value = _parse_var(raw)
        variables[key] = value

    try:
        body_template = _parse_body_template(args.body) if args.body else {"message": "{message}"}
    except (ValueError, OSError, json.JSONDecodeError) as e:
        console.print(f"[red]Invalid --body: {e}[/red]")
        sys.exit(1)

    headers: dict[str, str] = {}
    for raw in args.header:
        key, value = _parse_header(raw)
        headers[key] = value

    response_field = args.response_field
    error_field = args.error_field if args.error_field is not None else "error"
    metadata_fields = args.metadata_field
    model_name = args.name or "http-agent"

    parsed = urlparse(endpoint)
    if parsed.scheme == "http" and not (
        _is_local_host(parsed.hostname or "") or args.allow_insecure_http
    ):
        console.print(
            "[red]Refusing plaintext http:// endpoint on a non-local host "
            "(bearer tokens and prompts would go over the wire unencrypted). "
            "Use https:// or pass --allow_insecure_http.[/red]"
        )
        sys.exit(1)

    missing = _required_vars(body_template, headers) - set(variables)
    if missing:
        console.print(
            f"[red]Missing required template variables: "
            f"{', '.join(sorted(missing))} — pass --var key=value.[/red]"
        )
        sys.exit(1)

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
            metadata_fields=metadata_fields,
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
