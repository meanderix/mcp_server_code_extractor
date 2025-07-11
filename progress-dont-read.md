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

## Results - Experiment 1: Concise Descriptions (FAILED)
- **Did Claude use get_symbols() first for exploration?** ❌ NO
- **Did Claude use get_function()/get_class() for specific extraction?** ❌ NO  
- **Did Claude avoid Read tool for code investigation?** ❌ NO
- **Overall tool usage quality:** COMPLETE FAILURE

### What Actually Happened
Claude was asked to "investigate this repo" and:
1. Used Read(mcp_code_extractor.py) to read the entire 640-line file
2. Completely ignored all available MCP tools
3. Never attempted get_symbols(), get_function(), or any MCP tool
4. Followed traditional Read → analyze workflow despite tool availability

### Key Insights
- **Concise descriptions alone are insufficient** to change behavior
- **Claude defaults to familiar Read workflow** regardless of better alternatives
- **Having tools available ≠ using tools** - need forcing mechanism
- **Tool descriptions need stronger guidance**, not just clarity

---
Experiment 1 completed: 2025-07-11 - FAILED

## Experiment 2: Enhanced Tool Descriptions with Workflow Guidance

### Hypothesis
Adding explicit workflow guidance and stronger language to tool descriptions will force Claude to use MCP tools instead of Read.

### Changes to Test
- Add WARNING sections about Read being inefficient for code
- Include explicit "INSTEAD OF Read" language in descriptions
- Add workflow examples in tool descriptions
- Make tools obviously superior with richer output

### Test Question
"Analyze this codebase and tell me about its main functionality and key components."

### Success Criteria
- Claude uses get_symbols() first for exploration
- Claude uses get_function()/get_class() for specific extraction
- Claude avoids Read tool entirely for code investigation
- Claude follows guided workflow patterns

---
Experiment 2 started: 2025-07-11