"""Minimal implementation of an MCP-compatible hello server."""

import json
import sys


class HelloServer:
    """A minimal, line-based MCP server implementation."""

    def __init__(self, input_stream=None, output_stream=None):
        self.input_stream = input_stream or sys.stdin
        self.output_stream = output_stream or sys.stdout
        self.version = "0.1.0"

    def serve(self):
        """Read requests from the input stream and write responses."""
        self._write_event({"type": "ready", "version": self.version})

        while True:
            line = self.input_stream.readline()
            if not line:
                break

            data = line.strip()
            if not data:
                continue

            try:
                request = json.loads(data)
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

    def handle_request(self, request):
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

    def _write_event(self, payload):
        self._write_json(payload)

    def _write_response(self, payload):
        self._write_json(payload)

    def _write_json(self, payload):
        json.dump(payload, self.output_stream)
        self.output_stream.write("\n")
        self.output_stream.flush()
