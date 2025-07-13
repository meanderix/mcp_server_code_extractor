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
    print("\n1. Testing search for 'get_file_content' calls in server.py (single file):")
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

def test_directory_search():
    """Test directory search functionality."""
    
    print("\n" + "=" * 50)
    print("Testing DIRECTORY SEARCH functionality...")
    print("=" * 50)
    
    engine = SearchEngine()
    
    # Test 1: Search for get_file_content calls across the entire code_extractor directory
    print("\n1. Testing directory search for 'get_file_content' calls in code_extractor/:")
    params = SearchParameters(
        search_type="function-calls",
        target="get_file_content", 
        scope="code_extractor",
        file_patterns=["*.py"],  # Only Python files
        max_results=50
    )
    
    results = engine.search_directory("code_extractor", params)
    print(f"Found {len(results)} results for 'get_file_content' calls across directory:")
    for i, result in enumerate(results, 1):
        print(f"  {i}. {result.file_path}:{result.start_line} - {result.match_text}")
    
    # Test 2: Search for SearchEngine calls (should find imports and instantiations)
    print("\n2. Testing directory search for 'SearchEngine' usage:")
    params.target = "SearchEngine"
    results = engine.search_directory("code_extractor", params)
    print(f"Found {len(results)} results for 'SearchEngine' usage:")
    for i, result in enumerate(results, 1):
        print(f"  {i}. {result.file_path}:{result.start_line} - {result.match_text}")
    
    # Test 3: Search with file pattern restrictions
    print("\n3. Testing directory search with pattern filtering (only search_engine.py):")
    params = SearchParameters(
        search_type="function-calls",
        target="get_language_for_file",
        scope="code_extractor",
        file_patterns=["search_engine.py"],  # Only search_engine.py
        max_results=10
    )
    results = engine.search_directory("code_extractor", params)
    print(f"Found {len(results)} results for 'get_language_for_file' in search_engine.py only:")
    for i, result in enumerate(results, 1):
        print(f"  {i}. {result.file_path}:{result.start_line} - {result.match_text}")
    
    # Test 4: Test exclusion patterns
    print("\n4. Testing exclusion patterns (exclude __pycache__ and .pyc files):")
    params = SearchParameters(
        search_type="function-calls",
        target="print",
        scope="code_extractor",
        file_patterns=["*.py"],
        exclude_patterns=["__pycache__/*", "*.pyc", "test_*"],  # Exclude test files too
        max_results=20
    )
    results = engine.search_directory("code_extractor", params)
    print(f"Found {len(results)} results for 'print' calls (excluding test files):")
    for i, result in enumerate(results, 1):
        print(f"  {i}. {result.file_path}:{result.start_line} - {result.match_text}")

def test_language_detection():
    """Test language detection functionality."""
    
    print("\n" + "=" * 30)
    print("Testing language detection:")
    print("=" * 30)
    
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

if __name__ == "__main__":
    test_function_calls()
    test_directory_search()
    test_language_detection()
    
    print("\n" + "=" * 50)
    print("All semantic search tests completed!")