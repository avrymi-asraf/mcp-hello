# MCP Hello Server

A simple implementation of a Model Context Protocol (MCP) server for learning purposes.

## Features

- **Simple**: Uses only Python standard library - no external dependencies
- **Easy to understand**: Clear, synchronous code without complex async patterns
- **Minimal**: Stripped down to the essentials

## Installation

```bash
pip install .
```

## Usage

Run the server:

```bash
python -m mcp_hello.cli
```

Or if installed:

```bash
mcp-hello
```

## Testing

Run tests using Python's built-in unittest:

```bash
python -m unittest tests.test_server
```

## How it works

The server reads JSON requests from stdin and writes JSON responses to stdout:

**Ping request:**
```json
{"id": 1, "method": "ping"}
```

**Hello request:**
```json
{"id": 2, "method": "hello", "params": {"name": "Alice"}}
```

## Development

This project uses only the Python standard library - no external dependencies needed!
