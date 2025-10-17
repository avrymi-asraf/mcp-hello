"""Command-line entrypoint for the MCP Hello server."""

from __future__ import annotations

import asyncio
import contextlib
from typing import NoReturn

from .server import HelloServer


async def _run_server() -> None:
    server = HelloServer()
    await server.serve()


def main() -> NoReturn:
    """Run the MCP Hello server."""

    with contextlib.suppress(KeyboardInterrupt):
        asyncio.run(_run_server())
