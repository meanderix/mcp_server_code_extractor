#!/usr/bin/env python3

from tree_sitter_languages import get_language, get_parser

# Test decorated function structure
test_code = '''
class Test:
    @property
    def value(self):
        return 1
    
    @staticmethod 
    def static_method():
        return 2
'''

try:
    parser = get_parser('python')
    source_bytes = test_code.encode('utf-8')
    tree = parser.parse(source_bytes)
    
    def print_tree(node, depth=0):
        indent = "  " * depth
        text = source_bytes[node.start_byte:node.end_byte].decode('utf-8')[:40].replace('\n', '\\n')
        print(f"{indent}{node.type}: {text}")
        for child in node.children:
            if depth < 5:
                print_tree(child, depth + 1)
    
    print("Tree structure for decorated methods:")
    print_tree(tree.root_node)
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()