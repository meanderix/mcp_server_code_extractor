#!/usr/bin/env python3
"""
Quick test script for semantic search functionality.
Run with: python test_semantic_search.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from code_extractor.search_engine import SearchEngine
from code_extractor.models import SearchParameters

def test_function_calls():
    """Test function call search on our own codebase."""
    
    print("Testing semantic search functionality...")
    print("=" * 50)
    
    # Test searching for get_file_content calls in our server.py
    print("\n1. Testing search for 'get_file_content' calls in server.py:")
    params = SearchParameters(
        search_type="function-calls",
        target="get_file_content", 
        scope="code_extractor/server.py"
    )
    
    engine = SearchEngine()
    results = engine.search_file("code_extractor/server.py", params)
    
    print(f"Found {len(results)} results for 'get_file_content' calls:")
    for i, result in enumerate(results, 1):
        print(f"  {i}. Line {result.start_line}: {result.match_text}")
        if result.context_before:
            print(f"     Context before: {result.context_before[-1] if result.context_before else 'None'}")
    
    # Test searching for requests calls (should find none in our codebase)
    print("\n2. Testing search for 'requests.get' calls (should find 0):")
    params.target = "requests.get"
    results = engine.search_file("code_extractor/server.py", params)
    print(f"Found {len(results)} results for 'requests.get' calls (expected: 0)")
    
    # Test with a Python file that has function calls
    print("\n3. Testing search for 'get_symbols' calls in server.py:")
    params.target = "get_symbols"
    results = engine.search_file("code_extractor/server.py", params)
    print(f"Found {len(results)} results for 'get_symbols' calls:")
    for i, result in enumerate(results, 1):
        print(f"  {i}. Line {result.start_line}: {result.match_text}")
    
    # Test language detection
    print("\n4. Testing language detection:")
    from code_extractor.languages import get_language_for_file
    test_files = [
        "server.py",
        "models.py", 
        "search_engine.py",
        "README.md"
    ]
    for file in test_files:
        lang = get_language_for_file(f"code_extractor/{file}")
        print(f"  {file}: {lang}")
    
    print("\n" + "=" * 50)
    print("Semantic search test completed!")

if __name__ == "__main__":
    test_function_calls()