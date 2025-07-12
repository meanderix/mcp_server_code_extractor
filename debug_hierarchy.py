#!/usr/bin/env python3

from code_extractor import CodeExtractor

test_code = '''
class Calculator:
    def __init__(self):
        pass
    
    def add(self, x, y):
        return x + y
'''

try:
    extractor = CodeExtractor('python')
    symbols = extractor.extract_symbols(test_code)
    
    print(f"Found {len(symbols)} symbols:")
    for symbol in symbols:
        print(f"  {symbol.name} ({symbol.kind.value}) at bytes {symbol.start_byte}-{symbol.end_byte}")
        print(f"    Parent: {symbol.parent}")
        
    # Check sorting order for hierarchy detection
    symbols.sort(key=lambda s: s.start_byte)
    print("\nSorted by start_byte:")
    for symbol in symbols:
        print(f"  {symbol.name}: {symbol.start_byte}-{symbol.end_byte}")
            
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()