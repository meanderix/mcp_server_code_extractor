#!/usr/bin/env python3

# Quick debug test to see what's happening
from code_extractor import CodeExtractor

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
    extractor = CodeExtractor('python')
    print("Extractor created successfully")
    
    symbols = extractor.extract_symbols(test_code)
    print(f"Found {len(symbols)} symbols:")
    
    for symbol in symbols:
        print(f"  {symbol.name} ({symbol.kind.value}) at lines {symbol.start_line}-{symbol.end_line}")
        if hasattr(symbol, 'parent') and symbol.parent:
            print(f"    Parent: {symbol.parent}")
            
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()