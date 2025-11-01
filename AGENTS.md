## Project Goal

* **Description:** A minimal, educational implementation of a Model Context Protocol (MCP) server that responds to JSON-RPC-like requests over stdin/stdout. The server is executed as a command-line tool via `uvx mcp-hello` or `mcp-hello` (when installed) and runs as a persistent async service reading line-delimited JSON requests and writing JSON responses. Designed to run locally as a learning reference for MCP server development and can be published to PyPI test repository.

---

## Project Structure

* **Architecture:** Simple async stdin/stdout server with three main components:
  1. **CLI entrypoint** (`cli.py`) - Handles command execution and asyncio setup
  2. **Server core** (`server.py`) - Contains `HelloServer` class with request/response processing
  3. **Package exports** (`__init__.py`) - Exposes public API

* **Code Flow:**
  1. User invokes `mcp-hello` command (via `pyproject.toml` script definition)
  2. `cli.main()` initializes asyncio event loop and creates `HelloServer` instance
  3. Server writes initial `{"type": "ready"}` event to stdout
  4. Enters async loop reading line-delimited JSON from stdin
  5. For each request: parses JSON → routes to handler method (`ping`, `hello`) → writes response
  6. Continues until stdin closes or KeyboardInterrupt

---

## File Structure

```
/mcp-hello
├── mcp_hello/
│   ├── __init__.py      # Package exports (HelloServer, main)
│   ├── cli.py           # Command-line entrypoint with asyncio setup
│   └── server.py        # HelloServer implementation with request handlers
├── tests/
│   └── test_server.py   # Pytest unit tests with parametrized cases
├── main.py              # Simple standalone test script (legacy)
├── pyproject.toml       # Package metadata, dependencies, scripts
├── AGENTS.md            # This file
└── README.md            # Project documentation (empty)
```

* `mcp_hello/`: Core package containing the MCP server implementation
* `tests/`: Pytest test suite covering request handling and async flow
* `pyproject.toml`: Defines `mcp-hello` console script and Python >=3.12 requirement

---

## Building and Running

**Prerequisites:**
* Python 3.12+ (required by `pyproject.toml`)
* `uv` for package management (recommended)
* Dependencies: `anyio>=4` (installed automatically)

**Running the Application:**
1. **Development mode** (editable install):
   ```bash
   uv pip install -e .
   mcp-hello
   ```

2. **Direct execution** (no install):
   ```bash
   uvx mcp-hello
   ```

3. **Test JSON interaction**:
   ```bash
   echo '{"id":1,"method":"hello","params":{"name":"Alice"}}' | mcp-hello
   ```

**Running Tests:**
```bash
uv pip install pytest
pytest tests/
```

**Publishing to PyPI Test Repository:**
1. **Build the package**:
   ```bash
   uv build
   ```

2. **Upload to TestPyPI**:
   ```bash
   uv publish --index-url https://test.pypi.org/legacy/ --token <your-token>
   ```

3. **Test installation from TestPyPI**:
   ```bash
   uvx --index-url https://test.pypi.org/simple/ mcp-hello
   ```

---

## Extending the Server

To add a new method to the MCP server, follow this pattern:

**1. Add handler in `server.py`:**
```python
def handle_request(self, request: Request) -> Optional[Response]:
    request_id = request.get("id")
    method = request.get("method")
    params = request.get("params", {})
    
    # ... existing handlers ...
    
    if method == "add":
        a = params.get("a", 0)
        b = params.get("b", 0)
        return {
            "id": request_id,
            "result": {"sum": a + b},
        }
```

**2. Add test in `tests/test_server.py`:**
```python
@pytest.mark.parametrize(
    "payload,expected",
    [
        # ... existing cases ...
        ({"id": 4, "method": "add", "params": {"a": 5, "b": 3}}, {
            "id": 4,
            "result": {"sum": 8},
        }),
    ],
)
def test_handle_request_success(payload, expected):
    # test runs automatically
```

**3. Test interactively:**
```bash
echo '{"id":1,"method":"add","params":{"a":10,"b":20}}' | mcp-hello
```

---

## Code Writing Rules

* **Style Guide:** PEP 8 for Python code
* **Conventions:**
  - Async functions for I/O operations (stdin/stdout reading via `asyncio.run_in_executor`)
  - JSON-RPC-like structure: requests have `{id, method, params}`, responses have `{id, result}` or `{id, error}`
  - Error responses include `code` and `message` fields (e.g., `"method-not-found"`, `"invalid-json"`)
  - Line-delimited JSON protocol: each message is single line terminated by `\n`
  - Methods supported: `ping` (returns `{"message": "pong"}`), `hello` (returns greeting with optional `name` param)
  - Use `dataclass` with `field(default_factory=...)` for testable dependency injection (stdin/stdout)
  - Test with `io.StringIO` buffers to avoid actual I/O in unit tests
  - Package version auto-detected via `importlib.metadata` with fallback

