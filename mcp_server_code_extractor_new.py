#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "mcp[cli]",
#     "tree-sitter-languages",
#     "tree-sitter==0.21.3",
# ]
# ///
"""
MCP Extract - Simple code extraction using tree-sitter-languages

A single-file MCP server that extracts functions and classes from code files.
No more grep/sed/awk gymnastics - just clean, precise extraction.

🚨 **CRITICAL WORKFLOW GUIDANCE FOR CLAUDE** 🚨

**STOP USING READ/SEARCH/GREP FOR CODE INVESTIGATION!**

❌ **WRONG**: Read(file) → Search(pattern) → Edit
✅ **CORRECT**: get_symbols(file) → get_function(file, name) → Edit

**MANDATORY STEPS**:
1. ALWAYS start with get_symbols(file) to see what's in the file
2. Use get_function(file, name) to extract specific functions
3. Use get_class(file, name) for class definitions
4. NEVER use Read() to "examine" or "investigate" code files

**🚫 Using Read() on code files wastes context and misses structure**

**COMMON SCENARIOS**:
- Testing: get_symbols(test_file) → get_function(test_file, "test_method_name")
- Debugging: get_symbols(file) → get_function(file, "problematic_function")
- Refactoring: get_symbols(file) → get_class(file, "ClassName")
- Investigation: get_symbols(file) → get_lines(file, start, end)

Usage with uv:
  1. Install uv: curl -LsSf https://astral.sh/uv/install.sh | sh
  2. Run directly: uv run mcp-extract.py
  3. Configure in Claude Desktop with: uv run /path/to/mcp-extract.py

Or traditional install:
  pip install mcp[cli] tree-sitter-languages
"""

import os
import sys
from pathlib import Path

# Add current directory to path for local imports
sys.path.insert(0, os.path.dirname(__file__))

try:
    from code_extractor import CodeExtractor, create_extractor
    from code_extractor.models import SymbolKind
    from code_extractor.languages import get_language_for_file, is_language_supported
except ImportError as e:
    print(f"Error: Code extractor library not found: {e}")
    print("Make sure it's installed or run from the correct directory.")
    exit(1)

try:
    from mcp.server import Server
    from mcp.types import Tool, TextContent
    import mcp.server.stdio
except ImportError:
    print("Error: MCP library not found. Install with: pip install mcp[cli]")
    exit(1)


# Global server instance
server = Server("code-extractor")


def get_function(file_path: str, function_name: str) -> dict:
    """
    Extract a complete function definition - USE THIS INSTEAD OF Read() for specific functions!
    
    🎯 **PRECISE EXTRACTION** - Gets exact function boundaries with line numbers using tree-sitter.
    ⚠️ **REPLACES Read() + manual parsing** - No need to read entire files and search manually.
    
    Args:
        file_path: Path to the source file
        function_name: Exact name of the function to extract
        
    Returns:
        dict with code, start_line, end_line, lines, function, file, language
        
    **WORKFLOW**: get_symbols() first → get_function() for specific extraction → Edit
    """
    if not os.path.exists(file_path):
        return {"error": f"File not found: {file_path}"}
    
    try:
        extractor = create_extractor(file_path)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        symbol = extractor.extract_function(source_code, function_name)
        
        if symbol is None:
            return {"error": f"Function '{function_name}' not found in {file_path}"}
        
        # Extract the actual code for the function
        lines = source_code.split('\n')
        function_lines = lines[symbol.start_line-1:symbol.end_line]
        code = '\n'.join(function_lines)
        
        return {
            "code": code,
            "start_line": symbol.start_line,
            "end_line": symbol.end_line,
            "lines": symbol.lines,
            "function": symbol.name,
            "file": file_path,
            "language": extractor.language,
            # Enhanced details from new extractor
            "parameters": [str(p) for p in symbol.parameters],
            "return_type": symbol.return_type,
            "is_async": symbol.is_async,
            "parent": symbol.parent,
            "docstring": symbol.docstring
        }
        
    except Exception as e:
        return {"error": f"Failed to extract function '{function_name}' from '{file_path}': {str(e)}"}


def get_class(file_path: str, class_name: str) -> dict:
    """
    Extract a complete class definition - USE THIS INSTEAD OF Read() for specific classes!
    
    🎯 **PRECISE EXTRACTION** - Gets exact class boundaries with all methods using tree-sitter.
    ⚠️ **REPLACES Read() + manual parsing** - No need to read entire files and search manually.
    
    Args:
        file_path: Path to the source file
        class_name: Exact name of the class to extract
        
    Returns:
        dict with code, start_line, end_line, lines, class, file, language
        
    **WORKFLOW**: get_symbols() first → get_class() for specific extraction → Edit
    """
    if not os.path.exists(file_path):
        return {"error": f"File not found: {file_path}"}
    
    try:
        extractor = create_extractor(file_path)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        symbol = extractor.extract_class(source_code, class_name)
        
        if symbol is None:
            return {"error": f"Class '{class_name}' not found in {file_path}"}
        
        # Extract the actual code for the class
        lines = source_code.split('\n')
        class_lines = lines[symbol.start_line-1:symbol.end_line]
        code = '\n'.join(class_lines)
        
        # Get all methods in this class
        all_symbols = extractor.extract_symbols(source_code)
        methods = [s for s in all_symbols if s.kind == SymbolKind.METHOD and s.parent == class_name]
        
        return {
            "code": code,
            "start_line": symbol.start_line,
            "end_line": symbol.end_line,
            "lines": symbol.lines,
            "class": symbol.name,
            "file": file_path,
            "language": extractor.language,
            # Enhanced details from new extractor
            "docstring": symbol.docstring,
            "methods": [m.name for m in methods],
            "method_count": len(methods)
        }
        
    except Exception as e:
        return {"error": f"Failed to extract class '{class_name}' from '{file_path}': {str(e)}"}


def get_symbols(file_path: str) -> list:
    """
    🚨 **ALWAYS USE THIS FIRST** for code investigation - DO NOT use Read() on code files!
    
    List all functions, classes, and other symbols in a file with their line numbers.
    This is the CORRECT way to explore code structure instead of reading entire files.
    
    ⚠️ **REPLACES Read() for code files** - More efficient and structured than reading entire files.
    
    Args:
        file_path: Path to the source file to analyze
        
    Returns:
        List of symbols with name, type, start_line, end_line, lines, and preview
        
    **WORKFLOW**: get_symbols() → get_function()/get_class() → Edit (NOT Read → Search → Edit)
    """
    if not os.path.exists(file_path):
        return [{"error": f"File not found: {file_path}"}]

    try:
        extractor = create_extractor(file_path)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        symbols = extractor.extract_symbols(source_code)
        
        # Convert to dict format for MCP compatibility
        result = []
        for symbol in symbols:
            result.append(symbol.to_dict())
        
        return result
        
    except Exception as e:
        return [{"error": f"Failed to parse '{file_path}': {str(e)}"}]


def get_lines(file_path: str, start_line: int, end_line: int) -> dict:
    """
    Get specific lines from a file using precise line range control.
    
    Use this when you know exact line numbers you need (e.g., from get_symbols output) and 
    want to extract specific code sections without reading the entire file.
    
    Args:
        file_path: Path to the source file
        start_line: Starting line number (1-based, inclusive)
        end_line: Ending line number (1-based, inclusive)
        
    Returns:
        dict with code, start_line, end_line, lines, file, total_lines
        
    **WORKFLOW**: get_symbols() first → get_lines() for specific ranges → Edit
    """
    if not os.path.exists(file_path):
        return {"error": f"File not found: {file_path}"}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            all_lines = f.readlines()
        
        total_lines = len(all_lines)
        
        # Validate line numbers
        if start_line < 1 or end_line < 1:
            return {"error": "Line numbers must be >= 1"}
        if start_line > total_lines:
            return {"error": f"Start line {start_line} exceeds file length {total_lines}"}
        
        # Adjust end_line if it exceeds file length
        end_line = min(end_line, total_lines)
        
        # Extract lines (convert to 0-based indexing)
        selected_lines = all_lines[start_line-1:end_line]
        code = ''.join(selected_lines)
        
        return {
            "code": code,
            "start_line": start_line,
            "end_line": end_line,
            "lines": f"{start_line}-{end_line}",
            "file": file_path,
            "total_lines": total_lines
        }
        
    except Exception as e:
        return {"error": f"Failed to read lines from '{file_path}': {str(e)}"}


def get_signature(file_path: str, function_name: str) -> dict:
    """
    Get just the signature/declaration of a function without the full implementation.
    
    Use this when you only need to see function interfaces, parameters, and return types 
    for API exploration or documentation. Lighter weight than get_function.
    
    Args:
        file_path: Path to the source file
        function_name: Exact name of the function
        
    Returns:
        dict with signature, name, file, start_line, lines
        
    **WORKFLOW**: get_symbols() first → get_signature() for interface info → Edit
    """
    if not os.path.exists(file_path):
        return {"error": f"File not found: {file_path}"}
    
    try:
        extractor = create_extractor(file_path)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        symbol = extractor.extract_function(source_code, function_name)
        
        if symbol is None:
            return {"error": f"Function '{function_name}' not found in {file_path}"}
        
        return {
            "signature": symbol.signature,
            "name": symbol.name,
            "file": file_path,
            "start_line": symbol.start_line,
            "lines": symbol.lines,
            "parameters": [str(p) for p in symbol.parameters],
            "return_type": symbol.return_type,
            "is_async": symbol.is_async,
            "parent": symbol.parent
        }
        
    except Exception as e:
        return {"error": f"Failed to get signature for '{function_name}' from '{file_path}': {str(e)}"}


# MCP Server Tools
@server.list_tools()
async def list_tools():
    """List available tools for code extraction."""
    return [
        Tool(
            name="get_function",
            description="""Extract a complete function definition - USE THIS INSTEAD OF Read() for specific functions!

🎯 **PRECISE EXTRACTION** - Gets exact function boundaries with line numbers using tree-sitter.
⚠️ **REPLACES Read() + manual parsing** - No need to read entire files and search manually.

Args:
    file_path: Path to the source file
    function_name: Exact name of the function to extract
    
Returns:
    dict with code, start_line, end_line, lines, function, file, language

**WORKFLOW**: get_symbols() first → get_function() for specific extraction → Edit""",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string"},
                    "function_name": {"type": "string"}
                },
                "required": ["file_path", "function_name"]
            }
        ),
        Tool(
            name="get_class",
            description="""Extract a complete class definition - USE THIS INSTEAD OF Read() for specific classes!

🎯 **PRECISE EXTRACTION** - Gets exact class boundaries with all methods using tree-sitter.
⚠️ **REPLACES Read() + manual parsing** - No need to read entire files and search manually.

Args:
    file_path: Path to the source file
    class_name: Exact name of the class to extract
    
Returns:
    dict with code, start_line, end_line, lines, class, file, language

**WORKFLOW**: get_symbols() first → get_class() for specific extraction → Edit""",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string"},
                    "class_name": {"type": "string"}
                },
                "required": ["file_path", "class_name"]
            }
        ),
        Tool(
            name="get_symbols",
            description="""🚨 **ALWAYS USE THIS FIRST** for code investigation - DO NOT use Read() on code files!

List all functions, classes, and other symbols in a file with their line numbers.
This is the CORRECT way to explore code structure instead of reading entire files.

⚠️ **REPLACES Read() for code files** - More efficient and structured than reading entire files.

Args:
    file_path: Path to the source file to analyze
    
Returns:
    List of symbols with name, type, start_line, end_line, lines, and preview

**WORKFLOW**: get_symbols() → get_function()/get_class() → Edit (NOT Read → Search → Edit)""",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string"}
                },
                "required": ["file_path"]
            }
        ),
        Tool(
            name="get_lines",
            description="""Get specific lines from a file using precise line range control.

Use this when you know exact line numbers you need (e.g., from get_symbols output) and 
want to extract specific code sections without reading the entire file.

Args:
    file_path: Path to the source file
    start_line: Starting line number (1-based, inclusive)
    end_line: Ending line number (1-based, inclusive)
    
Returns:
    dict with code, start_line, end_line, lines, file, total_lines

**WORKFLOW**: get_symbols() first → get_lines() for specific ranges → Edit""",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string"},
                    "start_line": {"type": "integer"},
                    "end_line": {"type": "integer"}
                },
                "required": ["file_path", "start_line", "end_line"]
            }
        ),
        Tool(
            name="get_signature",
            description="""Get just the signature/declaration of a function without the full implementation.

Use this when you only need to see function interfaces, parameters, and return types 
for API exploration or documentation. Lighter weight than get_function.

Args:
    file_path: Path to the source file
    function_name: Exact name of the function
    
Returns:
    dict with signature, name, file, start_line, lines

**WORKFLOW**: get_symbols() first → get_signature() for interface info → Edit""",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {"type": "string"},
                    "function_name": {"type": "string"}
                },
                "required": ["file_path", "function_name"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    """Handle tool calls."""
    try:
        if name == "get_function":
            result = get_function(arguments["file_path"], arguments["function_name"])
        elif name == "get_class":
            result = get_class(arguments["file_path"], arguments["class_name"])
        elif name == "get_symbols":
            result = get_symbols(arguments["file_path"])
        elif name == "get_lines":
            result = get_lines(arguments["file_path"], arguments["start_line"], arguments["end_line"])
        elif name == "get_signature":
            result = get_signature(arguments["file_path"], arguments["function_name"])
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
        
        return [TextContent(type="text", text=str(result))]
        
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


def main():
    """Run the MCP server."""
    mcp.server.stdio.run_server(server)


if __name__ == "__main__":
    main()