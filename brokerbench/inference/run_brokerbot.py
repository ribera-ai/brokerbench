"""Run inference against BrokerBot's V2 agent gateway POST /generate endpoint.

The gateway speaks the channel pipeline (the same path Slack/SMS/web chat use).
Auth is either an HS256 JWT signed with the deployment's BETTER_AUTH_SECRET
(claims: teamId, agentId, userId, optional teamSlug) or a raw Better Auth
session token sent as Bearer alongside an x-team-id header.

Usage:
    python -m brokerbench.inference.run_brokerbot \
        --agent_url http://localhost:4200/generate \
        --team_id <team-uuid> \
        --user_id <user-id> \
        --agent_id <agent-uuid> \
        --auth_token <jwt-or-session-token> \
        --dataset all \
        --output_file predictions/brokerbot.jsonl
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import uuid
from collections.abc import Callable
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from rich.console import Console

from brokerbench.harness.types import Instance, Prediction
from brokerbench.inference import build_prompt, load_instances
from brokerbench.inference.run_api import _max_concurrency, _run_instances

console = Console()

_REQUEST_TIMEOUT = 300  # channel turns can run multi-step tool loops


def _make_predict(
    agent_url: str,
    team_id: str,
    user_id: str,
    agent_id: str | None,
    channel: str,
    auth_token: str | None,
) -> Callable[[Instance], str]:
    def predict(instance: Instance) -> str:
        prompt = build_prompt(instance)
        body: dict[str, object] = {
            "teamId": team_id,
            "userId": user_id,
            "channel": channel,
            "messageText": prompt,
            "messageId": f"bench-{instance.instance_id}-{uuid.uuid4().hex[:8]}",
            "chatId": str(uuid.uuid4()),
        }
        if agent_id:
            body["agentId"] = agent_id

        headers: dict[str, str] = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if auth_token:
            headers["Authorization"] = f"Bearer {auth_token}"

        def call() -> str:
            req = Request(
                agent_url,
                data=json.dumps(body).encode("utf-8"),
                headers=headers,
                method="POST",
            )
            with urlopen(req, timeout=_REQUEST_TIMEOUT) as resp:
                ctype = resp.headers.get("Content-Type", "")
                raw: str = resp.read().decode("utf-8")
            if "application/json" in ctype:
                data = json.loads(raw)
                if isinstance(data, dict) and "error" in data:
                    raise RuntimeError(str(data["error"]))
                return str(data.get("text", raw))
            return raw

        return call()

    return predict


def run_brokerbot(
    instances: list[Instance],
    agent_url: str,
    team_id: str,
    user_id: str,
    output_path: Path,
    agent_id: str | None = None,
    channel: str = "web",
    auth_token: str | None = None,
    max_concurrency: int = 8,
) -> list[Prediction]:
    """Run inference against the agent gateway /generate endpoint."""
    return _run_instances(
        instances,
        "brokerbot",
        output_path,
        _make_predict(agent_url, team_id, user_id, agent_id, channel, auth_token),
        max_concurrency,
    )


def main() -> None:
    """CLI entry point for BrokerBot inference."""
    parser = argparse.ArgumentParser(
        description="Run BrokerBot (V2 agent gateway) against the BrokerBench benchmark."
    )
    parser.add_argument(
        "--agent_url",
        type=str,
        default=os.environ.get("BROKERBOT_GATEWAY_URL", "http://localhost:4200/generate"),
        help="Agent gateway /generate URL (or set BROKERBOT_GATEWAY_URL).",
    )
    parser.add_argument(
        "--team_id",
        type=str,
        default=os.environ.get("BROKERBOT_TEAM_ID", ""),
        help="Team ID (or set BROKERBOT_TEAM_ID).",
    )
    parser.add_argument(
        "--user_id",
        type=str,
        default=os.environ.get("BROKERBOT_USER_ID", ""),
        help="User ID the turn runs as (or set BROKERBOT_USER_ID).",
    )
    parser.add_argument(
        "--agent_id",
        type=str,
        default=os.environ.get("BROKERBOT_AGENT_ID", ""),
        help="Agent ID — required when the JWT carries an agentId claim "
        "(or set BROKERBOT_AGENT_ID).",
    )
    parser.add_argument(
        "--channel",
        type=str,
        default="web",
        help="Channel to run the turn as (default: web).",
    )
    parser.add_argument(
        "--auth_token",
        type=str,
        default=os.environ.get("BROKERBOT_AUTH_TOKEN", ""),
        help="Bearer JWT or Better Auth session token (or set BROKERBOT_AUTH_TOKEN).",
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

    if not args.team_id:
        console.print("[red]--team_id is required (or BROKERBOT_TEAM_ID)[/red]")
        sys.exit(1)
    if not args.user_id:
        console.print("[red]--user_id is required (or BROKERBOT_USER_ID)[/red]")
        sys.exit(1)

    auth_token = args.auth_token or None
    if not auth_token:
        console.print(
            "[yellow]Warning: no auth token — requests will fail unless the "
            "gateway is unauthenticated.[/yellow]"
        )

    instances = load_instances(args.dataset)
    console.print(f"Loaded {len(instances)} instances")

    try:
        run_brokerbot(
            instances,
            args.agent_url,
            args.team_id,
            args.user_id,
            args.output_file,
            agent_id=args.agent_id or None,
            channel=args.channel,
            auth_token=auth_token,
            max_concurrency=_max_concurrency(args.max_concurrency),
        )
    except (HTTPError, URLError) as e:
        console.print(f"[red]Fatal: {e}[/red]")
        sys.exit(1)
    console.print(f"[green]Predictions written to {args.output_file}[/green]")


if __name__ == "__main__":
    main()
