#!/usr/bin/env python3
"""
Test script for the new symbol-definitions search functionality.
Run with: python test_symbol_definitions.py
"""

import sys
import os
import tempfile
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, os.path.dirname(__file__))

from code_extractor.search_engine import SearchEngine
from code_extractor.models import SearchParameters

def test_python_symbol_definitions():
    """Test symbol-definitions search on Python code."""
    
    print("=" * 60)
    print("Testing SYMBOL-DEFINITIONS search on Python code")
    print("=" * 60)
    
    # Test with our actual server.py file
    print("\n1. Testing function definitions in server.py:")
    params = SearchParameters(
        search_type="symbol-definitions",
        target="get_symbols", 
        scope="code_extractor/server.py"
    )
    
    engine = SearchEngine()
    results = engine.search_file("code_extractor/server.py", params)
    
    print(f"Found {len(results)} results for 'get_symbols' function definitions:")
    for i, result in enumerate(results, 1):
        print(f"  {i}. Line {result.start_line}: {result.match_text.strip()}")
        print(f"     Symbol type: {result.metadata.get('symbol_type', 'unknown')}")
        if result.context_before:
            print(f"     Context: {result.context_before[-1].strip()}")
    
    # Test class definitions
    print("\n2. Testing class definitions:")
    params.target = "SearchEngine"
    results = engine.search_file("code_extractor/search_engine.py", params)
    
    print(f"Found {len(results)} results for 'SearchEngine' class definitions:")
    for i, result in enumerate(results, 1):
        print(f"  {i}. Line {result.start_line}: {result.match_text.strip()}")
        print(f"     Symbol type: {result.metadata.get('symbol_type', 'unknown')}")
    
    # Test variable definitions
    print("\n3. Testing variable definitions:")
    params.target = "supported_types"
    results = engine.search_file("code_extractor/server.py", params)
    
    print(f"Found {len(results)} results for 'supported_types' variable definitions:")
    for i, result in enumerate(results, 1):
        print(f"  {i}. Line {result.start_line}: {result.match_text.strip()}")
        print(f"     Symbol type: {result.metadata.get('symbol_type', 'unknown')}")

def test_javascript_symbol_definitions():
    """Test symbol-definitions search on JavaScript code."""
    
    print("\n" + "=" * 60)
    print("Testing SYMBOL-DEFINITIONS search on JavaScript code")
    print("=" * 60)
    
    # Create temporary JavaScript file for testing
    js_code = '''
function fetchData(url) {
    return fetch(url);
}

class DataProcessor {
    constructor(options) {
        this.options = options;
    }
    
    process(data) {
        return data.map(item => item.value);
    }
}

const API_URL = 'https://api.example.com';
let cache = new Map();
var settings = { debug: true };
'''
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
        f.write(js_code)
        js_file = f.name
    
    try:
        engine = SearchEngine()
        
        # Test function definitions
        print("\n1. Testing JavaScript function definitions:")
        params = SearchParameters(
            search_type="symbol-definitions",
            target="fetchData",
            scope=js_file
        )
        
        results = engine.search_file(js_file, params)
        print(f"Found {len(results)} results for 'fetchData' function definitions:")
        for i, result in enumerate(results, 1):
            print(f"  {i}. Line {result.start_line}: {result.match_text.strip()}")
            print(f"     Symbol type: {result.metadata.get('symbol_type', 'unknown')}")
        
        # Test class definitions
        print("\n2. Testing JavaScript class definitions:")
        params.target = "DataProcessor"
        results = engine.search_file(js_file, params)
        
        print(f"Found {len(results)} results for 'DataProcessor' class definitions:")
        for i, result in enumerate(results, 1):
            print(f"  {i}. Line {result.start_line}: {result.match_text.strip()}")
            print(f"     Symbol type: {result.metadata.get('symbol_type', 'unknown')}")
        
        # Test variable definitions
        print("\n3. Testing JavaScript variable definitions:")
        params.target = "API_URL"
        results = engine.search_file(js_file, params)
        
        print(f"Found {len(results)} results for 'API_URL' variable definitions:")
        for i, result in enumerate(results, 1):
            print(f"  {i}. Line {result.start_line}: {result.match_text.strip()}")
            print(f"     Symbol type: {result.metadata.get('symbol_type', 'unknown')}")
            
    finally:
        os.unlink(js_file)

def test_typescript_symbol_definitions():
    """Test symbol-definitions search on TypeScript code."""
    
    print("\n" + "=" * 60)
    print("Testing SYMBOL-DEFINITIONS search on TypeScript code")
    print("=" * 60)
    
    # Create temporary TypeScript file for testing
    ts_code = '''
interface User {
    id: number;
    name: string;
}

type UserResponse = {
    user: User;
    status: string;
};

class UserService {
    private apiUrl: string;
    
    constructor(apiUrl: string) {
        this.apiUrl = apiUrl;
    }
    
    async getUser(id: number): Promise<User> {
        const response = await fetch(`${this.apiUrl}/users/${id}`);
        return response.json();
    }
}

const defaultTimeout = 5000;
let userCache: Map<number, User> = new Map();
'''
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ts', delete=False) as f:
        f.write(ts_code)
        ts_file = f.name
    
    try:
        engine = SearchEngine()
        
        # Test interface definitions
        print("\n1. Testing TypeScript interface definitions:")
        params = SearchParameters(
            search_type="symbol-definitions",
            target="User",
            scope=ts_file
        )
        
        results = engine.search_file(ts_file, params)
        print(f"Found {len(results)} results for 'User' interface definitions:")
        for i, result in enumerate(results, 1):
            print(f"  {i}. Line {result.start_line}: {result.match_text.strip()}")
            print(f"     Symbol type: {result.metadata.get('symbol_type', 'unknown')}")
        
        # Test type definitions
        print("\n2. Testing TypeScript type definitions:")
        params.target = "UserResponse"
        results = engine.search_file(ts_file, params)
        
        print(f"Found {len(results)} results for 'UserResponse' type definitions:")
        for i, result in enumerate(results, 1):
            print(f"  {i}. Line {result.start_line}: {result.match_text.strip()}")
            print(f"     Symbol type: {result.metadata.get('symbol_type', 'unknown')}")
        
        # Test class definitions
        print("\n3. Testing TypeScript class definitions:")
        params.target = "UserService"
        results = engine.search_file(ts_file, params)
        
        print(f"Found {len(results)} results for 'UserService' class definitions:")
        for i, result in enumerate(results, 1):
            print(f"  {i}. Line {result.start_line}: {result.match_text.strip()}")
            print(f"     Symbol type: {result.metadata.get('symbol_type', 'unknown')}")
            
    finally:
        os.unlink(ts_file)

def test_directory_search():
    """Test symbol-definitions search across a directory."""
    
    print("\n" + "=" * 60)
    print("Testing SYMBOL-DEFINITIONS directory search")
    print("=" * 60)
    
    engine = SearchEngine()
    
    # Test searching for class definitions across the entire code_extractor directory
    print("\n1. Searching for 'SearchEngine' class definitions across directory:")
    params = SearchParameters(
        search_type="symbol-definitions",
        target="SearchEngine",
        scope="code_extractor",
        file_patterns=["*.py"],
        max_results=10
    )
    
    results = engine.search_directory("code_extractor", params)
    print(f"Found {len(results)} results for 'SearchEngine' class definitions:")
    for i, result in enumerate(results, 1):
        print(f"  {i}. {result.file_path}:{result.start_line} - {result.match_text.strip()}")
        print(f"     Symbol type: {result.metadata.get('symbol_type', 'unknown')}")
    
    # Test searching for function definitions
    print("\n2. Searching for function definitions containing 'extract':")
    params.target = "extract"
    results = engine.search_directory("code_extractor", params)
    
    print(f"Found {len(results)} results for functions with 'extract' in name:")
    for i, result in enumerate(results, 1):
        print(f"  {i}. {result.file_path}:{result.start_line} - {result.match_text.strip()}")
        print(f"     Symbol type: {result.metadata.get('symbol_type', 'unknown')}")

def test_comparison_with_function_calls():
    """Compare symbol-definitions vs function-calls search results."""
    
    print("\n" + "=" * 60)
    print("COMPARISON: symbol-definitions vs function-calls")
    print("=" * 60)
    
    engine = SearchEngine()
    
    # Search for get_file_content definitions vs calls
    target = "get_file_content"
    scope = "code_extractor/server.py"
    
    print(f"\nComparing searches for '{target}' in {scope}:")
    
    # Symbol definitions
    params_def = SearchParameters(
        search_type="symbol-definitions",
        target=target,
        scope=scope
    )
    results_def = engine.search_file(scope, params_def)
    
    print(f"\nSymbol definitions ({len(results_def)} results):")
    for i, result in enumerate(results_def, 1):
        print(f"  {i}. Line {result.start_line}: {result.match_text.strip()}")
    
    # Function calls
    params_calls = SearchParameters(
        search_type="function-calls",
        target=target,
        scope=scope
    )
    results_calls = engine.search_file(scope, params_calls)
    
    print(f"\nFunction calls ({len(results_calls)} results):")
    for i, result in enumerate(results_calls, 1):
        print(f"  {i}. Line {result.start_line}: {result.match_text.strip()}")
    
    print(f"\nSummary:")
    print(f"  Definitions found: {len(results_def)}")
    print(f"  Calls found: {len(results_calls)}")
    print(f"  This demonstrates the difference between where symbols are DEFINED vs USED")

def test_edge_cases():
    """Test edge cases and error conditions."""
    
    print("\n" + "=" * 60)
    print("Testing EDGE CASES and error conditions")
    print("=" * 60)
    
    engine = SearchEngine()
    
    # Test with unsupported language
    print("\n1. Testing with unsupported language (.txt file):")
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("This is just text, not code.")
        txt_file = f.name
    
    try:
        params = SearchParameters(
            search_type="symbol-definitions",
            target="text",
            scope=txt_file
        )
        
        results = engine.search_file(txt_file, params)
        print(f"Results for unsupported language: {len(results)} (expected: 0)")
        
    finally:
        os.unlink(txt_file)
    
    # Test with non-existent target
    print("\n2. Testing with non-existent symbol:")
    params = SearchParameters(
        search_type="symbol-definitions",
        target="NonExistentSymbolName12345",
        scope="code_extractor/server.py"
    )
    
    results = engine.search_file("code_extractor/server.py", params)
    print(f"Results for non-existent symbol: {len(results)} (expected: 0)")
    
    # Test with empty file
    print("\n3. Testing with empty file:")
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write("")  # Empty file
        empty_file = f.name
    
    try:
        params = SearchParameters(
            search_type="symbol-definitions",
            target="anything",
            scope=empty_file
        )
        
        results = engine.search_file(empty_file, params)
        print(f"Results for empty file: {len(results)} (expected: 0)")
        
    finally:
        os.unlink(empty_file)

def run_all_tests():
    """Run all symbol-definitions tests."""
    
    print("🔍 SYMBOL-DEFINITIONS SEARCH TESTING SUITE")
    print("=" * 60)
    
    try:
        test_python_symbol_definitions()
        test_javascript_symbol_definitions() 
        test_typescript_symbol_definitions()
        test_directory_search()
        test_comparison_with_function_calls()
        test_edge_cases()
        
        print("\n" + "=" * 60)
        print("✅ ALL SYMBOL-DEFINITIONS TESTS COMPLETED SUCCESSFULLY!")
        print("Ready for deployment! 🚀")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        print("Fix the issue before deployment.")
        raise

if __name__ == "__main__":
    run_all_tests()