#!/usr/bin/env python3

from tree_sitter_languages import get_language, get_parser

test_code = '''
class Calculator:
    def __init__(self):
        pass
    
    def add(self, x, y):
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
    
    query = language.query(query_text)
    captures = query.captures(tree.root_node)
    
    print("Query captures with ranges:")
    for node, capture_name in captures:
        text = source_bytes[node.start_byte:node.end_byte].decode('utf-8').replace('\n', '\\n')
        print(f"  {capture_name}: {node.start_byte}-{node.end_byte}: '{text}'")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()