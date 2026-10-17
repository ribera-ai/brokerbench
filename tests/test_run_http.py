"""Tests for the generic HTTP agent runner (run_http)."""

from __future__ import annotations

import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

import pytest

from brokerbench.harness.constants import Domain
from brokerbench.harness.types import Instance
from brokerbench.inference.run_http import (
    PRESETS,
    _dig,
    _make_predict,
    _parse_body_template,
    _parse_header,
    _parse_var,
    _resolve_template,
    run_http,
)


def _instance(i: int = 1) -> Instance:
    return Instance(
        instance_id=f"test-{i:03d}",
        domain=Domain.LICENSING,
        question=f"Question {i}?",
        choices=["A. a", "B. b"],
        expected_answer="A",
    )


class TestResolveTemplate:
    def test_full_value_placeholder(self) -> None:
        out = _resolve_template({"a": "{team_id}"}, {"team_id": "t-1"})
        assert out == {"a": "t-1"}

    def test_inline_substitution(self) -> None:
        out = _resolve_template({"a": "Bearer {tok}"}, {"tok": "xyz"})
        assert out == {"a": "Bearer xyz"}

    def test_unset_required_inline_raises(self) -> None:
        with pytest.raises(KeyError, match="missing required variable: nope"):
            _resolve_template({"a": "x {nope} y"}, {})

    def test_optional_embedded_in_string_drops_field(self) -> None:
        out = _resolve_template({"auth": "Bearer {tok?}"}, {})
        assert out == {}

    def test_optional_field_dropped_when_unset(self) -> None:
        out = _resolve_template({"a": "{opt?}", "b": "keep"}, {})
        assert out == {"b": "keep"}

    def test_optional_field_kept_when_set(self) -> None:
        out = _resolve_template({"a": "{opt?}"}, {"opt": "v"})
        assert out == {"a": "v"}

    def test_required_missing_raises(self) -> None:
        with pytest.raises(KeyError, match="missing required variable: req"):
            _resolve_template({"a": "{req}"}, {})

    def test_nested_and_list(self) -> None:
        tpl = {"outer": {"inner": "{v}", "gone": "{opt?}"}, "l": ["{v}", "{opt?}"]}
        assert _resolve_template(tpl, {"v": 1}) == {"outer": {"inner": 1}, "l": [1]}

    def test_env_expansion(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("MY_SECRET", "s3cret")
        out = _resolve_template({"h": "Bearer $MY_SECRET"}, {})
        assert out == {"h": "Bearer s3cret"}

    def test_non_string_passthrough(self) -> None:
        assert _resolve_template({"n": 5, "f": 1.5, "b": True}, {}) == {
            "n": 5,
            "f": 1.5,
            "b": True,
        }


class TestDig:
    def test_dotted_path(self) -> None:
        data = {"choices": [{"message": {"content": "hi"}}]}
        assert _dig(data, "choices.0.message.content") == "hi"

    def test_missing_key_raises(self) -> None:
        with pytest.raises(KeyError):
            _dig({"a": {}}, "a.b")


class TestParseHelpers:
    def test_header(self) -> None:
        assert _parse_header("Authorization: Bearer x") == ("Authorization", "Bearer x")

    def test_header_bad(self) -> None:
        with pytest.raises(ValueError):
            _parse_header("no-colon-here")

    def test_var(self) -> None:
        assert _parse_var("k=v=with=equals") == ("k", "v=with=equals")

    def test_body_inline_json(self) -> None:
        assert _parse_body_template('{"a": "{message}"}') == {"a": "{message}"}

    def test_body_at_file(self, tmp_path: Path) -> None:
        f = tmp_path / "tpl.json"
        f.write_text('{"x": "{message}"}')
        assert _parse_body_template(f"@{f}") == {"x": "{message}"}

    def test_body_non_object_rejected(self) -> None:
        with pytest.raises(ValueError):
            _parse_body_template('["not", "an", "object"]')


class _EchoHandler(BaseHTTPRequestHandler):
    """Captures the request and replies {text: <body.message>} or an error."""

    seen: list[dict[str, Any]] = []
    mode = "ok"

    def do_POST(self) -> None:  # noqa: N802
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length))
        _EchoHandler.seen.append({"body": body, "auth": self.headers.get("Authorization")})
        if _EchoHandler.mode == "error":
            payload = {"error": "agent exploded"}
        else:
            payload = {"text": "A"}
        raw = json.dumps(payload).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def log_message(self, *args: Any) -> None:
        pass


@pytest.fixture()
def echo_server() -> Any:
    _EchoHandler.seen = []
    _EchoHandler.mode = "ok"
    server = ThreadingHTTPServer(("127.0.0.1", 0), _EchoHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{server.server_address[1]}"
    server.shutdown()


class TestPredict:
    def test_posts_rendered_body_and_extracts_field(self, echo_server: str) -> None:
        predict = _make_predict(
            endpoint=f"{echo_server}/chat",
            body_template={"input": "{message}", "mid": "{message_id}", "opt": "{opt?}"},
            headers={"Authorization": "Bearer {tok?}"},
            variables={"opt": "set", "tok": "t"},
            response_field="text",
            error_field="error",
            timeout=30,
        )
        assert predict(_instance()) == "A"
        sent = _EchoHandler.seen[0]
        assert sent["auth"] == "Bearer t"
        assert "Question 1?" in sent["body"]["input"]
        assert sent["body"]["mid"].startswith("bench-test-001-")
        assert sent["body"]["opt"] == "set"

    def test_optional_auth_header_dropped(self, echo_server: str) -> None:
        predict = _make_predict(
            endpoint=f"{echo_server}/chat",
            body_template={"input": "{message}"},
            headers={"Authorization": "Bearer {tok?}"},
            variables={},
            response_field="text",
            error_field="error",
            timeout=30,
        )
        predict(_instance())
        assert _EchoHandler.seen[0]["auth"] is None

    def test_error_field_raises(self, echo_server: str) -> None:
        _EchoHandler.mode = "error"
        predict = _make_predict(
            endpoint=f"{echo_server}/chat",
            body_template={"input": "{message}"},
            headers={},
            variables={},
            response_field="text",
            error_field="error",
            timeout=30,
        )
        with pytest.raises(RuntimeError, match="agent exploded"):
            predict(_instance())


class TestRunHttp:
    def test_end_to_end_writes_predictions(self, echo_server: str, tmp_path: Path) -> None:
        out = tmp_path / "preds.jsonl"
        preds = run_http(
            [_instance(1), _instance(2)],
            f"{echo_server}/chat",
            out,
            "test-agent",
            body_template={"input": "{message}"},
            response_field="text",
            error_field="error",
            max_concurrency=2,
        )
        assert len(preds) == 2
        assert all(p.prediction == "A" for p in preds)
        assert all(p.model_name_or_path == "test-agent" for p in preds)
        lines = [json.loads(x) for x in out.read_text().splitlines()]
        assert [x["instance_id"] for x in lines] == ["test-001", "test-002"]


class TestBrokerbotPreset:
    def test_preset_shape(self) -> None:
        preset = PRESETS["brokerbot"]
        ctx = {
            "team_id": "t",
            "user_id": "u",
            "channel": "web",
            "message": "m",
            "message_id": "id",
            "chat_id": "c",
        }
        body = _resolve_template(preset.body, ctx)
        assert body == {
            "teamId": "t",
            "userId": "u",
            "channel": "web",
            "messageText": "m",
            "messageId": "id",
            "chatId": "c",
        }
        headers = _resolve_template(preset.headers, ctx)
        assert headers == {"Accept": "application/json"}

    def test_preset_optional_fields(self) -> None:
        preset = PRESETS["brokerbot"]
        ctx = {
            "team_id": "t",
            "user_id": "u",
            "agent_id": "a",
            "channel": "web",
            "auth_token": "jwt",
            "message": "m",
            "message_id": "id",
            "chat_id": "c",
        }
        body = _resolve_template(preset.body, ctx)
        headers = _resolve_template(preset.headers, ctx)
        assert body["agentId"] == "a"
        assert headers["Authorization"] == "Bearer jwt"
