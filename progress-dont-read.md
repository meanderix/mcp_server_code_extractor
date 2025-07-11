# MCP Tool Description Refactoring Experiment

## Background
The MCP server tool descriptions were extremely verbose (100+ lines each) with excessive educational content, making them hard to use. We refactored them to be concise and clear.

## Changes Made
- **get_function()**: Reduced from 200+ lines to ~10 lines
- **get_class()**: Reduced from 100+ lines to ~10 lines  
- **get_symbols()**: Reduced from 150+ lines to ~10 lines
- **get_lines()**: Reduced from 100+ lines to ~10 lines
- **get_signature()**: Reduced from 50+ lines to ~10 lines

## New Description Format
Each tool now has:
- Clear purpose statement (1-2 sentences)
- When to use it (1-2 sentences)
- Parameters and return format
- Key advantages (1 sentence)

## Experiment Setup
We will now:
1. Restart Claude Code
2. Ask fresh Claude instance to investigate this repo
3. Observe if it uses the MCP tools properly
4. Document results here

## Hypothesis
The concise tool descriptions should make it easier for Claude to:
- Understand what each tool does
- Know when to use each tool
- Use the tools effectively for code investigation
- Avoid verbose Read operations on code files

## Results (to be filled after experiment)
- Did Claude use get_symbols() first for exploration?
- Did Claude use get_function()/get_class() for specific extraction?
- Did Claude avoid Read tool for code investigation?
- Overall tool usage quality:

---
Experiment started: 2025-07-11