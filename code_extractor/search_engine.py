"""
Semantic code search engine using tree-sitter parsing.

Provides sophisticated pattern matching beyond simple text search,
leveraging syntax tree structure for accurate code understanding.
"""

from typing import List, Optional, Dict, Any
from pathlib import Path
import os
from tree_sitter import Node, Query
from tree_sitter_languages import get_parser, get_language

from .models import SearchResult, SearchParameters
from .file_reader import get_file_content
from .languages import get_language_for_file


class SearchEngine:
    """
    Core search engine that executes tree-sitter queries against code files.
    
    Supports caching of parsed ASTs and compiled queries for performance.
    """
    
    def __init__(self):
        self._ast_cache: Dict[str, Any] = {}  # file_hash -> parsed_tree
        self._query_cache: Dict[str, Query] = {}  # (lang, pattern) -> compiled_query
    
    def search_file(self, file_path: str, params: SearchParameters) -> List[SearchResult]:
        """Search a single file for the specified pattern."""
        try:
            # Get language
            lang_name = params.language or get_language_for_file(file_path)
            if lang_name == 'text':
                return []  # Skip unsupported languages
            
            # Get file content
            source_code = get_file_content(file_path, params.git_revision)
            if not source_code.strip():
                return []
            
            # Get or create parser
            parser = get_parser(lang_name)
            tree = parser.parse(source_code.encode('utf-8'))
            
            # For Phase 1, we'll hardcode the function-calls pattern
            if params.search_type == "function-calls":
                return self._search_function_calls(file_path, source_code, tree, params, lang_name)
            
            return []
            
        except Exception as e:
            # Log error but don't crash
            print(f"Error searching {file_path}: {e}")
            return []
    
    def _search_function_calls(self, file_path: str, source_code: str, tree: Any, 
                             params: SearchParameters, lang_name: str) -> List[SearchResult]:
        """Search for function calls in the parsed tree."""
        results = []
        
        # Define query patterns for different languages
        patterns = {
            'python': '''
                ; Method calls like obj.method()
                (call
                  function: (attribute
                    (identifier) @module
                    (identifier) @function
                  )
                ) @call
                
                ; Simple function calls like func()
                (call
                  function: (identifier) @simple_function
                ) @simple_call
            ''',
            'javascript': '''
                (call_expression
                  function: (member_expression
                    object: (identifier) @module  
                    property: (property_identifier) @function
                  )
                ) @call
            ''',
            'typescript': '''
                (call_expression
                  function: (member_expression
                    object: (identifier) @module  
                    property: (property_identifier) @function
                  )
                ) @call
            '''
        }
        
        pattern = patterns.get(lang_name)
        if not pattern:
            return []
        
        # Compile and execute query
        query = self._get_compiled_query(lang_name, pattern)
        captures = query.captures(tree.root_node)
        
        source_lines = source_code.splitlines()
        
        for node, capture_name in captures:
            if capture_name in ['call', 'simple_call']:
                # Check if this matches our target
                call_text = source_code[node.start_byte:node.end_byte]
                if params.target in call_text:
                    start_line = node.start_point[0] + 1
                    end_line = node.end_point[0] + 1
                    
                    # Get context lines
                    context_before = []
                    context_after = []
                    if params.include_context:
                        start_ctx = max(0, start_line - 1 - params.context_lines)
                        end_ctx = min(len(source_lines), end_line + params.context_lines)
                        context_before = source_lines[start_ctx:start_line-1]
                        context_after = source_lines[end_line:end_ctx]
                    
                    result = SearchResult(
                        file_path=file_path,
                        start_line=start_line,
                        end_line=end_line,
                        match_text=call_text,
                        context_before=context_before,
                        context_after=context_after,
                        metadata={"search_type": params.search_type, "target": params.target},
                        language=lang_name
                    )
                    results.append(result)
                    
                    if len(results) >= params.max_results:
                        break
        
        return results
    
    def _get_compiled_query(self, language: str, pattern: str) -> Query:
        """Get or compile a tree-sitter query."""
        cache_key = f"{language}:{hash(pattern)}"
        if cache_key not in self._query_cache:
            language_obj = get_language(language)
            self._query_cache[cache_key] = language_obj.query(pattern)
        return self._query_cache[cache_key]