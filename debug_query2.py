#!/usr/bin/env python3

from tree_sitter_languages import get_language, get_parser

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
    
    source_bytes = test_code.encode('utf-8')
    tree = parser.parse(source_bytes)
    
    # Test our exact query
    with open('code_extractor/queries/python.scm', 'r') as f:
        query_text = f.read()
    
    print("Query text:")
    print(query_text)
    print("\n" + "="*50 + "\n")
    
    query = language.query(query_text)
    captures = query.captures(tree.root_node)
    
    print(f"Query found {len(captures)} captures:")
    for node, capture_name in captures:
        text = source_bytes[node.start_byte:node.end_byte].decode('utf-8')[:50]
        print(f"  {capture_name}: {text}")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()