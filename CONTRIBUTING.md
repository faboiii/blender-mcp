# Contributing to BlenderMCP

Thank you for your interest in contributing to BlenderMCP! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Adding New Features](#adding-new-features)

## Code of Conduct

Please be respectful and constructive in all interactions. We aim to foster an inclusive and welcoming community.

## Getting Started

Before contributing, please:

1. Join our [Discord community](https://discord.gg/z5apgR8TFU) to discuss your ideas
2. Check existing [issues](https://github.com/ahujasid/blender-mcp/issues) and pull requests
3. Read through this contributing guide

## Development Setup

### Prerequisites

- Python 3.10 or newer
- Blender 3.0 or newer
- UV package manager ([installation instructions](https://docs.astral.sh/uv/getting-started/installation/))
- Git

### Local Development Environment

1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/blender-mcp.git
   cd blender-mcp
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -e .
   ```

4. **Install the Blender addon:**
   - Copy `addon.py` to Blender's addon directory
   - Enable it in Blender's preferences

## Project Structure

```
blender-mcp/
├── addon.py                    # Blender addon (socket server)
├── main.py                     # Entry point for MCP server
├── src/blender_mcp/
│   ├── __init__.py            # Package initialization
│   └── server.py              # MCP server implementation
├── pyproject.toml             # Python project configuration
├── README.md                  # User-facing documentation
└── CONTRIBUTING.md            # This file
```

### Key Components

- **addon.py**: Runs inside Blender, handles socket communication and executes commands
- **server.py**: MCP server that connects Claude AI to the Blender addon
- Communication happens via TCP sockets on localhost:9876 using JSON protocol

## How to Contribute

### Types of Contributions

We welcome various types of contributions:

1. **Bug Reports**: Report issues with clear reproduction steps
2. **Feature Requests**: Suggest new features or improvements
3. **Code Contributions**: Bug fixes, new features, or improvements
4. **Documentation**: Improve README, add examples, or write tutorials
5. **Testing**: Add tests or improve test coverage
6. **Community Support**: Help others in Discord or GitHub discussions

### Reporting Bugs

When reporting bugs, please include:

- Blender version
- Python version
- Operating system
- Steps to reproduce
- Expected behavior
- Actual behavior
- Error messages or logs
- Screenshots if applicable

### Suggesting Features

For feature requests, please describe:

- The problem you're trying to solve
- Your proposed solution
- Alternative solutions you've considered
- How it fits with BlenderMCP's goals

## Coding Standards

### Python Style Guide

- Follow [PEP 8](https://pep8.org/) style guide
- Use type hints where appropriate
- Write docstrings for all functions and classes
- Keep functions focused and single-purpose
- Maximum line length: 100 characters

### Code Examples

**Good:**
```python
@mcp.tool()
def get_scene_info(ctx: Context) -> str:
    """
    Get detailed information about the current Blender scene.

    Returns:
        str: JSON-formatted scene information

    Raises:
        Exception: If connection to Blender fails
    """
    try:
        blender = get_blender_connection()
        result = blender.send_command("get_scene_info")
        return json.dumps(result, indent=2)
    except Exception as e:
        logger.error(f"Error getting scene info: {str(e)}")
        return f"Error getting scene info: {str(e)}"
```

**Avoid:**
```python
def do_stuff(x):  # No type hints, unclear name, no docstring
    return x.send("thing")  # No error handling
```

### Logging

- Use the `logging` module, not `print()`
- Log levels:
  - `DEBUG`: Detailed diagnostic information
  - `INFO`: General informational messages
  - `WARNING`: Warning messages for recoverable issues
  - `ERROR`: Error messages for failures

Example:
```python
logger.info(f"Connecting to Blender at {host}:{port}")
logger.error(f"Failed to parse response: {str(e)}")
```

### Error Handling

Always handle errors gracefully:

```python
try:
    result = risky_operation()
    return result
except SpecificException as e:
    logger.error(f"Specific error occurred: {str(e)}")
    raise
except Exception as e:
    logger.error(f"Unexpected error: {str(e)}")
    return f"Error: {str(e)}"
```

## Testing

### Manual Testing

Before submitting a PR, test your changes:

1. **Start Blender** with the addon enabled
2. **Start the MCP server** via Claude Desktop or manually
3. **Test all affected features** through Claude
4. **Check logs** for errors or warnings
5. **Test edge cases** (disconnections, invalid inputs, etc.)

### Test Checklist

- [ ] Connection to Blender works
- [ ] All existing tools still function
- [ ] New features work as expected
- [ ] Error handling works correctly
- [ ] No regression in existing functionality
- [ ] Logs are informative and not excessive

### Integration Testing

Test the full workflow:

```
Claude AI → MCP Server → Socket → Blender Addon → Blender API
```

Verify:
- Commands are sent correctly
- Responses are received and parsed
- Blender executes operations
- Results are returned to Claude

## Pull Request Process

### Before Submitting

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following coding standards

3. **Test thoroughly** using the testing checklist

4. **Update documentation** if needed (README.md, docstrings)

5. **Commit with clear messages:**
   ```bash
   git commit -m "feat: add screenshot capability to viewport tool"
   ```

### Commit Message Format

Use conventional commits:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

Examples:
```
feat: add Sketchfab model search integration
fix: resolve socket timeout issues during large downloads
docs: update installation instructions for Windows
refactor: improve error handling in send_command
```

### Submitting the Pull Request

1. **Push your branch:**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create a PR** on GitHub with:
   - Clear title describing the change
   - Detailed description of what and why
   - Screenshots/demos if applicable
   - Reference to related issues

3. **Respond to feedback** from reviewers

4. **Update your PR** based on review comments

### PR Checklist

- [ ] Code follows project style guidelines
- [ ] Changes are well-tested
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] No merge conflicts
- [ ] PR description is detailed

## Adding New Features

### Adding a New Tool

To add a new MCP tool:

1. **In `server.py`, create the tool:**
   ```python
   @mcp.tool()
   def your_new_tool(ctx: Context, param: str) -> str:
       """
       Brief description of what the tool does.

       Parameters:
       - param: Description of the parameter

       Returns description.
       """
       try:
           blender = get_blender_connection()
           result = blender.send_command("your_command", {"param": param})
           return json.dumps(result, indent=2)
       except Exception as e:
           logger.error(f"Error in your_new_tool: {str(e)}")
           return f"Error: {str(e)}"
   ```

2. **In `addon.py`, add the command handler:**
   ```python
   def handle_command(self, command):
       cmd_type = command.get("type")
       params = command.get("params", {})

       if cmd_type == "your_command":
           return self.your_command_handler(params)

   def your_command_handler(self, params):
       try:
           param = params.get("param")
           # Implement your logic here
           return {"status": "success", "result": {...}}
       except Exception as e:
           return {"status": "error", "message": str(e)}
   ```

3. **Update documentation** in README.md

### Adding External API Integrations

When integrating new APIs (like PolyHaven, Sketchfab):

1. **Add configuration UI** in the addon's panel
2. **Implement API client** with proper error handling
3. **Add status check tool** (e.g., `get_service_status()`)
4. **Add search/browse tools** if applicable
5. **Add download/import tools**
6. **Update the asset_creation_strategy prompt** if needed

### Architecture Considerations

- **Keep socket communication simple**: Use JSON for all messages
- **Handle timeouts gracefully**: Large downloads may take time
- **Validate inputs**: Check parameters before sending to Blender
- **Log appropriately**: Help debugging without overwhelming logs
- **Consider async operations**: Some operations may be long-running

## Communication Protocol

### Command Format (MCP → Blender)

```json
{
  "type": "command_name",
  "params": {
    "param1": "value1",
    "param2": "value2"
  }
}
```

### Response Format (Blender → MCP)

Success:
```json
{
  "status": "success",
  "result": {
    "data": "..."
  }
}
```

Error:
```json
{
  "status": "error",
  "message": "Error description"
}
```

## Resources

- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [Blender Python API Documentation](https://docs.blender.org/api/current/)
- [Discord Community](https://discord.gg/z5apgR8TFU)

## Questions?

If you have questions:

1. Check existing documentation
2. Search closed issues and PRs
3. Ask in Discord
4. Open a discussion on GitHub

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to BlenderMCP! Your contributions help make 3D creation with AI more accessible to everyone.
