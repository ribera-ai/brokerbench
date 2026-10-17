"""Run inference against BrokerBot's V2 agent gateway POST /generate endpoint.

Thin wrapper over the generic HTTP runner (:mod:`run_http`) pinned to the
``brokerbot`` preset — the channel pipeline Slack/SMS/web chat use. Auth is
an HS256 JWT signed with the deployment's BETTER_AUTH_SECRET (claims:
teamId + agentId, or userId+teamSlug+chatId) or a raw Better Auth session
token sent as Bearer.

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
import os
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError

from rich.console import Console

from brokerbench.harness.types import Instance, Prediction
from brokerbench.inference import load_instances
from brokerbench.inference.run_api import _max_concurrency
from brokerbench.inference.run_http import PRESETS, run_http

console = Console()

_PRESET = PRESETS["brokerbot"]


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
    variables: dict[str, str] = {
        "team_id": team_id,
        "user_id": user_id,
        "channel": channel,
    }
    if agent_id:
        variables["agent_id"] = agent_id
    if auth_token:
        variables["auth_token"] = auth_token
    return run_http(
        instances,
        agent_url,
        output_path,
        _PRESET.name,
        body_template=_PRESET.body,
        headers=_PRESET.headers,
        variables=variables,
        response_field=_PRESET.response_field,
        error_field=_PRESET.error_field,
        metadata_fields=_PRESET.metadata_fields,
        max_concurrency=max_concurrency,
    )


def main() -> None:
    """CLI entry point for BrokerBot inference."""
    parser = argparse.ArgumentParser(
        description="Run BrokerBot (V2 agent gateway) against the BrokerBench benchmark."
    )
    parser.add_argument(
        "--agent_url",
        type=str,
        default=os.environ.get("BROKERBOT_GATEWAY_URL", _PRESET.endpoint_default),
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
        default=os.environ.get("BROKERBOT_CHANNEL", "web"),
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

    if not args.auth_token:
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
            auth_token=args.auth_token or None,
            max_concurrency=_max_concurrency(args.max_concurrency),
        )
    except (HTTPError, URLError) as e:
        console.print(f"[red]Fatal: {e}[/red]")
        sys.exit(1)
    console.print(f"[green]Predictions written to {args.output_file}[/green]")


if __name__ == "__main__":
    main()
