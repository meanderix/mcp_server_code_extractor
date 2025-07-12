#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

# Test the new MCP server functions
from mcp_server_code_extractor_new import get_symbols, get_function, get_class

test_code = '''
class Calculator:
    """A simple calculator class."""
    
    def __init__(self, initial_value: int = 0):
        """Initialize with optional initial value."""
        self.value = initial_value
    
    @property
    def current_value(self) -> int:
        """Get the current value."""
        return self.value
    
    async def add(self, x: int, y: int = 5) -> int:
        """Add two numbers asynchronously."""
        return x + y
'''

# Write test code to a file
with open('/tmp/test_calculator.py', 'w') as f:
    f.write(test_code)

print("Testing new MCP server functions...")

print("\n1. Testing get_symbols:")
symbols = get_symbols('/tmp/test_calculator.py')
for symbol in symbols:
    if 'error' not in symbol:
        print(f"  - {symbol['name']} ({symbol['type']}) at lines {symbol['lines']}")
        if symbol.get('parent'):
            print(f"    Parent: {symbol['parent']}")

print("\n2. Testing get_function:")
add_method = get_function('/tmp/test_calculator.py', 'add')
if 'error' not in add_method:
    print(f"  Function: {add_method['function']}")
    print(f"  Parent: {add_method.get('parent', 'None')}")
    print(f"  Async: {add_method.get('is_async', False)}")
    print(f"  Parameters: {add_method.get('parameters', [])}")
    print(f"  Return type: {add_method.get('return_type', 'None')}")
else:
    print(f"  Error: {add_method['error']}")

print("\n3. Testing get_class:")
calc_class = get_class('/tmp/test_calculator.py', 'Calculator')
if 'error' not in calc_class:
    print(f"  Class: {calc_class['class']}")
    print(f"  Methods: {calc_class.get('methods', [])}")
    print(f"  Method count: {calc_class.get('method_count', 0)}")
else:
    print(f"  Error: {calc_class['error']}")

print("\n✅ Core functionality test complete!")