# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

**Testing:**
```bash
# Run all tests using pytest
uv run pytest

# Run individual test files  
uv run pytest tests/test_extractor.py
uv run pytest tests/test_languages.py
uv run pytest tests/test_models.py

# Quick functional test of core MCP server
python test_new_mcp.py
```

**Running the MCP Server:**
```bash
# Run as package with UV (recommended)
uv run mcp-server-code-extractor

# Run as Python module
uv run python -m code_extractor

# Test with MCP Inspector
npx @modelcontextprotocol/inspector uv run mcp-server-code-extractor

# For uvx usage (after publishing)
uvx mcp-server-code-extractor
```

**Development Dependencies:**
```bash
# Install development dependencies (testing, formatting, linting)
uv add --dev pytest black flake8 mypy
```

**Code Quality:**
```bash
# Format code with Black
uv run black .

# Lint with flake8
uv run flake8 .

# Type checking with mypy
uv run mypy .
```

## Architecture Overview

This is an MCP (Model Context Protocol) server that provides precise code extraction using tree-sitter parsing. The codebase has a **clean package structure**:

### Package Structure (`code_extractor/`)
- **MCP Server** (`server.py`) - FastMCP server with 5 extraction tools
- **Core Library** (`extractor.py`) - Query-driven extraction engine using tree-sitter
- **Data Models** (`models.py`) - Rich symbol representations with hierarchical relationships  
- **Language Support** (`languages.py`) - Detection and mapping for 30+ programming languages
- **Tree-sitter Queries** (`queries/`) - Language-specific syntax parsing patterns
- **Entry Points** (`__main__.py`) - Module execution support

### Entry Points
- **Console Script**: `mcp-server-code-extractor` - Direct execution via uvx/pip
- **Module Execution**: `python -m code_extractor` - Run as Python module
- **Package Import**: `from code_extractor import CodeExtractor` - Library usage

### Key Architectural Decisions

**Method vs Function Classification:**
The core innovation is distinguishing methods (functions inside classes) from top-level functions using tree-sitter query patterns. This solves the context problem where traditional parsers can't determine if a function is a class method without understanding the containment hierarchy.

**Two-Layer Symbol Processing:**
1. **Query capture phase**: Tree-sitter queries extract syntax nodes with semantic labels
2. **Symbol building phase**: Raw captures are processed into rich `CodeSymbol` objects with hierarchical relationships

**Clean MCP Interface:**
The server uses FastMCP for simple tool registration and exposes 5 core extraction tools with consistent function signatures and error handling.

## Working with Tree-Sitter Queries

Tree-sitter queries are stored in `code_extractor/queries/` and use the S-expression format:

```scheme
; Extract methods inside classes
(class_definition
  body: (block
    (function_definition
      name: (identifier) @method.name
      parameters: (parameters) @method.parameters) @method.definition))
```

**Query Structure:**
- Capture names use `category.type` format (e.g., `method.name`, `function.definition`)
- The extractor groups captures by their definition nodes to build complete symbols
- Parent-child relationships are determined by byte range containment

## Language Support

New languages require:
1. Adding language mapping in `code_extractor/languages.py`
2. Creating tree-sitter query file in `code_extractor/queries/`
3. Testing with language-specific syntax patterns

The system automatically detects language from file extensions and falls back gracefully for unsupported languages.

## MCP Tools Interface

The server exposes 5 tools to AI assistants:

1. **`get_symbols`** - Primary entry point for code discovery (uses modern core library)
2. **`get_function`** - Extract specific functions (legacy tree traversal)  
3. **`get_class`** - Extract specific classes (legacy tree traversal)
4. **`get_lines`** - Extract line ranges by number
5. **`get_signature`** - Get function signatures only

**Best Practice**: Always use `get_symbols` first for code exploration, then use specific extraction tools for detailed analysis.