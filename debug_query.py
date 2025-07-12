#!/usr/bin/env python3

from tree_sitter_languages import get_language, get_parser
import os

# Simple debug to see what tree-sitter finds
test_code = '''
class Calculator:
    """A simple calculator class."""
    
    def __init__(self, initial_value: int = 0):
        """Initialize with optional initial value."""
        self.value = initial_value
    
    def add(self, x: int, y: int = 5) -> int:
        """Add two numbers."""
        return x + y
'''

try:
    parser = get_parser('python')
    language = get_language('python')
    
    print("Parser and language loaded successfully")
    
    # Parse the code
    source_bytes = test_code.encode('utf-8')
    tree = parser.parse(source_bytes)
    
    print(f"Tree parsed successfully")
    print(f"Root node type: {tree.root_node.type}")
    print(f"Root node children: {len(tree.root_node.children)}")
    
    # Print tree structure
    def print_tree(node, depth=0):
        indent = "  " * depth
        print(f"{indent}{node.type}")
        for child in node.children:
            if depth < 3:  # Limit depth
                print_tree(child, depth + 1)
    
    print("\nTree structure:")
    print_tree(tree.root_node)
    
    # Test a simple query
    print("\nTesting simple class query...")
    query_text = "(class_definition) @class"
    query = language.query(query_text)
    captures = query.captures(tree.root_node)
    
    print(f"Simple query found {len(captures)} matches")
    for node, capture in captures:
        print(f"  Found {capture}: {node.type}")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()