"""Tests for the minimal MCP hello server."""

import io
import json
import unittest

from mcp_hello.server import HelloServer


class TestHelloServer(unittest.TestCase):
    """Test cases for HelloServer."""

    def test_handle_request_ping(self):
        server = HelloServer()
        payload = {"id": 1, "method": "ping"}
        expected = {"id": 1, "result": {"message": "pong"}}
        self.assertEqual(server.handle_request(payload), expected)

    def test_handle_request_hello_default(self):
        server = HelloServer()
        payload = {"id": 2, "method": "hello"}
        expected = {"id": 2, "result": {"message": "Hello, world!"}}
        self.assertEqual(server.handle_request(payload), expected)

    def test_handle_request_hello_with_name(self):
        server = HelloServer()
        payload = {"id": 3, "method": "hello", "params": {"name": "Alice"}}
        expected = {"id": 3, "result": {"message": "Hello, Alice!"}}
        self.assertEqual(server.handle_request(payload), expected)

    def test_handle_request_unknown_method(self):
        server = HelloServer()
        response = server.handle_request({"id": 4, "method": "unknown"})
        self.assertEqual(response["error"]["code"], "method-not-found")

    def test_serve_flow(self):
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

        server.serve()

        output_buffer.seek(0)
        lines = [json.loads(line) for line in output_buffer.read().splitlines() if line]
        self.assertEqual(lines[0]["type"], "ready")

        messages_received = {line.get("result", {}).get("message") for line in lines}
        self.assertIn("Hello, world!", messages_received)
        self.assertIn("pong", messages_received)


if __name__ == "__main__":
    unittest.main()
