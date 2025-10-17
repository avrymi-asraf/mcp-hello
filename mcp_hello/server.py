"""Minimal implementation of an MCP-compatible hello server."""

from __future__ import annotations

import asyncio
import json
import sys
from dataclasses import dataclass, field
from typing import Any, Dict, IO, Optional


Request = Dict[str, Any]
Response = Dict[str, Any]


def _default_version() -> str:
    """Return the package version, falling back to the source version."""

    try:  # pragma: no cover - metadata lookup is trivial
        from importlib import metadata

        return metadata.version("mcp-hello")
    except Exception:  # pragma: no cover - used only in editable installs
        return "0.1.0"


@dataclass
class HelloServer:
    """A minimal, line-based MCP server implementation."""

    input_stream: IO[str] = field(default_factory=lambda: sys.stdin)
    output_stream: IO[str] = field(default_factory=lambda: sys.stdout)
    version: str = field(default_factory=_default_version)

    async def serve(self) -> None:
        """Read requests from the input stream and write responses."""

        self._write_event({"type": "ready", "version": self.version})
        loop = asyncio.get_running_loop()

        while True:
            line = await loop.run_in_executor(None, self.input_stream.readline)
            if not line:
                break

            data = line.strip()
            if not data:
                continue

            try:
                request: Request = json.loads(data)
            except json.JSONDecodeError as error:
                self._write_response({
                    "error": {
                        "code": "invalid-json",
                        "message": f"Failed to parse JSON: {error.msg}",
                    }
                })
                continue

            response = self.handle_request(request)
            if response is not None:
                self._write_response(response)

    def handle_request(self, request: Request) -> Optional[Response]:
        """Process a single MCP-like request."""

        request_id = request.get("id")
        method = request.get("method")
        params = request.get("params", {})

        if method == "ping":
            return {
                "id": request_id,
                "result": {"message": "pong"},
            }

        if method == "hello":
            name = params.get("name") or "world"
            return {
                "id": request_id,
                "result": {"message": f"Hello, {name}!"},
            }

        return {
            "id": request_id,
            "error": {
                "code": "method-not-found",
                "message": f"Unknown method: {method}",
            },
        }

    def _write_event(self, payload: Dict[str, Any]) -> None:
        self._write_json(payload)

    def _write_response(self, payload: Dict[str, Any]) -> None:
        self._write_json(payload)

    def _write_json(self, payload: Dict[str, Any]) -> None:
        json.dump(payload, self.output_stream)
        self.output_stream.write("\n")
        self.output_stream.flush()
