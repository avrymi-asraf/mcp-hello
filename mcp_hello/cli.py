"""Command-line entrypoint for the MCP Hello server."""

from .server import HelloServer


def main():
    """Run the MCP Hello server."""
    try:
        server = HelloServer()
        server.serve()
    except KeyboardInterrupt:
        pass
