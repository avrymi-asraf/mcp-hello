"""Tests for the minimal MCP hello server."""

from __future__ import annotations

import io
import json

import pytest
import asyncio

from mcp_hello.server import HelloServer


@pytest.mark.parametrize(
    "payload,expected",
    [
        ({"id": 1, "method": "ping"}, {"id": 1, "result": {"message": "pong"}}),
        ({"id": 2, "method": "hello"}, {"id": 2, "result": {"message": "Hello, world!"}}),
        ({"id": 3, "method": "hello", "params": {"name": "Alice"}}, {
            "id": 3,
            "result": {"message": "Hello, Alice!"},
        }),
    ],
)
def test_handle_request_success(payload, expected):
    server = HelloServer()
    assert server.handle_request(payload) == expected


def test_handle_request_unknown_method():
    server = HelloServer()
    response = server.handle_request({"id": 4, "method": "unknown"})
    assert response["error"]["code"] == "method-not-found"


def test_serve_flow():
    messages = "\n".join(
        [
            json.dumps({"id": 1, "method": "hello"}),
            "",  # ignored blank line
            json.dumps({"id": 2, "method": "ping"}),
        ]
    ) + "\n"

    input_buffer = io.StringIO(messages)
    output_buffer = io.StringIO()
    server = HelloServer(input_stream=input_buffer, output_stream=output_buffer)

    asyncio.run(server.serve())

    output_buffer.seek(0)
    lines = [json.loads(line) for line in output_buffer.read().splitlines() if line]
    assert lines[0]["type"] == "ready"
    assert {line.get("result", {}).get("message") for line in lines} >= {
        "Hello, world!",
        "pong",
    }
