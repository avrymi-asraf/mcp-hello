"""Minimal MCP Hello server package."""

from .cli import main
from .server import HelloServer

__all__ = ["HelloServer", "main"]
