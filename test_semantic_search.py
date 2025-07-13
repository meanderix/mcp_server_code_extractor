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

def test_performance_benchmarks():
    """Test performance with larger file sets."""
    
    print("\n" + "=" * 50)
    print("Testing PERFORMANCE BENCHMARKS...")
    print("=" * 50)
    
    import time
    import tempfile
    from pathlib import Path
    
    engine = SearchEngine()
    
    # Create temporary directory with many files
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        
        print(f"\n1. Creating test directory with 100 Python files...")
        
        # Create 100 files with function calls
        for i in range(100):
            file_content = f"""
def function_{i}():
    '''Function {i} for testing.'''
    get_file_content('data_{i}.json')
    process_data({{'{i}': 'value_{i}'}})
    print(f'Processing item {{i}}')
    return True

class TestClass_{i}:
    def method_{i}(self):
        get_file_content('config_{i}.json')
        return self.value
"""
            (tmp_path / f"module_{i:03d}.py").write_text(file_content)
        
        print(f"Created 100 files in {tmp_dir}")
        
        # Test directory search performance
        print("\n2. Testing directory search performance...")
        
        params = SearchParameters(
            search_type="function-calls",
            target="get_file_content",
            scope=str(tmp_path),
            file_patterns=["*.py"],
            max_results=500
        )
        
        start_time = time.time()
        results = engine.search_directory(str(tmp_path), params)
        end_time = time.time()
        
        duration = end_time - start_time
        print(f"  Search completed in {duration:.2f} seconds")
        print(f"  Found {len(results)} results across 100 files")
        print(f"  Performance: {len(results)/duration:.1f} results/second")
        
        # Verify results quality
        file_count = len(set(r.file_path for r in results))
        print(f"  Results span {file_count} different files")
        
        # Test with different search targets
        print("\n3. Testing multiple search patterns...")
        
        search_targets = ["print", "process_data", "return"]
        for target in search_targets:
            params.target = target
            start_time = time.time()
            results = engine.search_directory(str(tmp_path), params)
            end_time = time.time()
            
            print(f"  '{target}': {len(results)} results in {end_time - start_time:.2f}s")

def test_memory_usage():
    """Test memory usage with large result sets."""
    
    print("\n" + "=" * 50)
    print("Testing MEMORY USAGE...")
    print("=" * 50)
    
    import tempfile
    import os
    from pathlib import Path
    
    try:
        import psutil
        has_psutil = True
    except ImportError:
        has_psutil = False
        print("  psutil not available, skipping detailed memory analysis")
    
    engine = SearchEngine()
    
    if has_psutil:
        # Get initial memory usage
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        print(f"\n1. Initial memory usage: {initial_memory:.1f} MB")
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        
        # Create files with many function calls each
        print("\n2. Creating files with high match density...")
        for i in range(20):
            lines = []
            for j in range(100):  # 100 function calls per file
                lines.append(f"    get_data('item_{i}_{j}')")
            
            content = f"def process_file_{i}():\n" + "\n".join(lines)
            (tmp_path / f"dense_{i:02d}.py").write_text(content)
        
        print("Created 20 files with ~2000 total function calls")
        
        params = SearchParameters(
            search_type="function-calls",
            target="get_data",
            scope=str(tmp_path),
            max_results=2000  # Allow many results
        )
        
        # Measure memory during search
        if has_psutil:
            before_search = process.memory_info().rss / 1024 / 1024
            
        results = engine.search_directory(str(tmp_path), params)
        
        if has_psutil:
            after_search = process.memory_info().rss / 1024 / 1024
            memory_increase = after_search - before_search
            
            print(f"\n3. Memory usage after search:")
            print(f"  Before search: {before_search:.1f} MB")
            print(f"  After search: {after_search:.1f} MB") 
            print(f"  Memory increase: {memory_increase:.1f} MB")
            print(f"  Results found: {len(results)}")
            print(f"  Memory per result: {memory_increase * 1024 / len(results):.1f} KB" if results else "N/A")
        else:
            print(f"\n3. Search completed with {len(results)} results")

def test_error_resilience():
    """Test error handling and resilience."""
    
    print("\n" + "=" * 50)
    print("Testing ERROR RESILIENCE...")
    print("=" * 50)
    
    import tempfile
    from pathlib import Path
    
    engine = SearchEngine()
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        
        # Create mix of valid and problematic files
        print("\n1. Creating mixed file types...")
        
        # Valid Python files
        (tmp_path / "valid1.py").write_text("print('valid')")
        (tmp_path / "valid2.py").write_text("get_data('test')")
        
        # Binary file
        (tmp_path / "binary.bin").write_bytes(b'\x00\x01\x02\x03Binary data\x00')
        
        # Empty file
        (tmp_path / "empty.py").touch()
        
        # Very large file (if memory allows)
        try:
            large_content = "print('line')\n" * 10000
            (tmp_path / "large.py").write_text(large_content)
            print("  Created large file with 10,000 lines")
        except MemoryError:
            print("  Skipped large file creation (memory limited)")
        
        # File with unicode
        (tmp_path / "unicode.py").write_text("print('Hello 世界 🌍')")
        
        print("  Created mix of valid, binary, empty, and unicode files")
        
        # Test search resilience
        print("\n2. Testing search across problematic files...")
        
        params = SearchParameters(
            search_type="function-calls",
            target="print",
            scope=str(tmp_path),
            file_patterns=["*"]  # Include all files to test filtering
        )
        
        try:
            results = engine.search_directory(str(tmp_path), params)
            print(f"  Search completed successfully with {len(results)} results")
            
            # Check that binary files were excluded
            binary_results = [r for r in results if "binary" in r.file_path]
            print(f"  Binary file results (should be 0): {len(binary_results)}")
            
            # Check that valid files were processed
            valid_results = [r for r in results if "valid" in r.file_path or "unicode" in r.file_path]
            print(f"  Valid file results: {len(valid_results)}")
            
        except Exception as e:
            print(f"  ERROR: Search failed with {e}")

def test_real_world_scenarios():
    """Test realistic code search scenarios."""
    
    print("\n" + "=" * 50)
    print("Testing REAL-WORLD SCENARIOS...")
    print("=" * 50)
    
    engine = SearchEngine()
    
    # Test 1: Search for error handling patterns in actual codebase
    print("\n1. Searching for error handling patterns in actual codebase...")
    
    params = SearchParameters(
        search_type="function-calls",
        target="Exception",
        scope="code_extractor",
        file_patterns=["*.py"],
        exclude_patterns=["test_*", "__pycache__/*"]
    )
    
    results = engine.search_directory("code_extractor", params)
    print(f"  Found {len(results)} Exception-related patterns")
    
    # Test 2: Search for import patterns
    print("\n2. Searching for import patterns...")
    
    params.target = "from "
    results = engine.search_directory("code_extractor", params)
    print(f"  Found {len(results)} import statements")
    
    # Test 3: Search for class definitions (simplified)
    print("\n3. Searching for class patterns...")
    
    params.target = "class "
    results = engine.search_directory("code_extractor", params)
    print(f"  Found {len(results)} class-related patterns")
    
    # Test 4: Cross-file dependency analysis
    print("\n4. Analyzing cross-file dependencies...")
    
    params.target = "SearchEngine"
    results = engine.search_directory("code_extractor", params)
    
    usage_files = set()
    for result in results:
        usage_files.add(os.path.basename(result.file_path))
    
    print(f"  SearchEngine used in {len(usage_files)} files: {', '.join(sorted(usage_files))}")
    
    # Test 5: Test with different file patterns
    print("\n5. Testing language-specific searches...")
    
    # Only Python files
    params = SearchParameters(
        search_type="function-calls",
        target="def ",
        scope="code_extractor",
        file_patterns=["*.py"],
        max_results=20
    )
    
    results = engine.search_directory("code_extractor", params)
    print(f"  Python function definitions: {len(results)}")
    
    # Check language consistency
    languages = {r.language for r in results}
    print(f"  Languages detected: {languages}")

if __name__ == "__main__":
    test_function_calls()
    test_directory_search()
    test_language_detection()
    test_performance_benchmarks()
    test_memory_usage()
    test_error_resilience()
    test_real_world_scenarios()
    
    print("\n" + "=" * 50)
    print("All comprehensive semantic search tests completed!")