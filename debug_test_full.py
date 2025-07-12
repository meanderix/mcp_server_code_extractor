#!/usr/bin/env python3

from code_extractor import CodeExtractor

# The actual test code from conftest.py
basic_class_code = '''
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
    
    @staticmethod
    def multiply(a: int, b: int) -> int:
        """Multiply two numbers."""
        return a * b
    
    @classmethod
    def from_string(cls, value_str: str) -> 'Calculator':
        """Create calculator from string."""
        return cls(int(value_str))
'''

try:
    extractor = CodeExtractor('python')
    symbols = extractor.extract_symbols(basic_class_code)
    
    print(f"Found {len(symbols)} symbols:")
    for symbol in symbols:
        print(f"  {symbol.name} ({symbol.kind.value}) at lines {symbol.start_line}-{symbol.end_line}")
        if symbol.parent:
            print(f"    Parent: {symbol.parent}")
        if symbol.is_async:
            print(f"    Async: {symbol.is_async}")
        if symbol.parameters:
            print(f"    Parameters: {[str(p) for p in symbol.parameters]}")
            
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()