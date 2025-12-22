# CAPL Version Guide

This guide helps you choose the right CAPL version for your needs.

## Available Versions

| Version | File | Authentication | Critical Thinking | Use Case |
|---------|------|----------------|-------------------|----------|
| **Basic SDK** | `capl.py` | API Keys | No | Simple tasks, creative work, API integration |
| **Enhanced SDK** | `capl_enhanced.py` | API Keys | Yes | Factual tasks, code review, complex analyses |
| **Basic CLI** | `capl_cli.py` | CLI Tools | No | Same as Basic SDK, but prefer CLI auth |
| **Enhanced CLI** | `capl_enhanced_cli.py` | CLI Tools | Yes | Same as Enhanced SDK, but prefer CLI auth |

## Decision Tree

```
┌─────────────────────────────────────────┐
│ What type of task do you have?         │
└─────────────────┬───────────────────────┘
                  │
        ┌─────────┴─────────┐
        │                   │
    Simple/              Complex/
    Creative             Factual
        │                   │
        │                   │
        ▼                   ▼
┌──────────────┐    ┌──────────────┐
│ Use Basic    │    │ Use Enhanced │
│ Version      │    │ Version      │
└──────┬───────┘    └──────┬───────┘
       │                   │
       │                   │
       ▼                   ▼
┌─────────────────────────────────────────┐
│ How do you prefer to authenticate?     │
└─────────────────┬───────────────────────┘
                  │
        ┌─────────┴─────────┐
        │                   │
    API Keys            CLI Tools
        │                   │
        ▼                   ▼
   Use .py             Use _cli.py
   version             version
```

## Detailed Comparison

### Basic vs Enhanced

**Basic Version:**
- Worker follows all critic feedback without question
- Critic reviews based on internal knowledge only
- Simpler, faster iterations
- **Good for:**
  - Creative writing (stories, poems)
  - Brainstorming sessions
  - Exploratory work
  - Non-factual tasks

**Enhanced Version:**
- Worker critically evaluates feedback (can accept/reject)
- Critic can identify claims needing verification
- More robust, thoughtful iterations
- **Good for:**
  - Factual content (science, history, technical)
  - Code review and debugging
  - Complex analyses
  - Controversial topics where bias matters
  - Tasks requiring defensible accuracy

### SDK vs CLI

**SDK Version (using API keys):**
- Direct API calls via Python SDKs
- Requires API keys in `.env` file
- More control over API parameters
- Better for integration into applications
- **Good for:**
  - Programmatic use
  - Custom applications
  - CI/CD pipelines
  - When you already manage API keys

**CLI Version (using command-line tools):**
- Uses subprocess to call CLI tools
- Leverages existing CLI authentication
- No API key management in code
- Requires CLI tools installed
- **Good for:**
  - Interactive use
  - Existing CLI workflows
  - When you prefer not to manage API keys
  - Testing with different CLI wrappers

## Quick Examples

### Example 1: Creative Writing
**Best choice:** Basic SDK (`capl.py`)

```bash
python capl.py "Write a short story about a robot learning to paint"
```

**Why:** Creative task, no need for critical evaluation, API SDK is simple.

### Example 2: Technical Documentation
**Best choice:** Enhanced SDK (`capl_enhanced.py`)

```bash
python capl_enhanced.py "Explain how HTTPS encryption works" --iterations 3 --save
```

**Why:** Factual content needs accuracy verification, critical thinking ensures quality.

### Example 3: Code Review
**Best choice:** Enhanced CLI (`capl_enhanced_cli.py`)

```bash
python capl_enhanced_cli.py "Review this Python function for bugs and improvements" --save
```

**Why:** Code review benefits from critical evaluation, CLI is convenient if already authenticated.

### Example 4: Quick Brainstorming
**Best choice:** Basic CLI (`capl_cli.py`)

```bash
python capl_cli.py "Generate 10 ideas for a mobile productivity app"
```

**Why:** Simple brainstorming, CLI is quick if already set up.

## Feature Matrix

| Feature | Basic SDK | Enhanced SDK | Basic CLI | Enhanced CLI |
|---------|-----------|--------------|-----------|--------------|
| Worker follows feedback blindly | ✓ | ✗ | ✓ | ✗ |
| Worker evaluates feedback critically | ✗ | ✓ | ✗ | ✓ |
| Critic fact-checking framework | ✗ | ✓ | ✗ | ✓ |
| Worker defends good work | ✗ | ✓ | ✗ | ✓ |
| Transparent reasoning | ✗ | ✓ | ✗ | ✓ |
| Requires API keys | ✓ | ✓ | ✗ | ✗ |
| Uses CLI tools | ✗ | ✗ | ✓ | ✓ |
| Configurable iterations | ✓ | ✓ | ✓ | ✓ |
| Session export | ✓ | ✓ | ✓ | ✓ |
| Custom models/CLIs | ✓ | ✓ | ✓ | ✓ |

## Migration Guide

### From Basic to Enhanced

If you're using basic version and need more accuracy:

```python
# Before (Basic)
from capl import create_capl_from_env
capl = create_capl_from_env(max_iterations=2)

# After (Enhanced)
from capl_enhanced import create_capl_enhanced
capl = create_capl_enhanced(max_iterations=2, enable_search=True)

# Everything else stays the same!
```

### From SDK to CLI

If you want to switch from API keys to CLI:

```bash
# Before (SDK)
python capl.py "Your task"

# After (CLI)
python capl_cli.py "Your task"

# Options work the same way
python capl_cli.py "Your task" --iterations 3 --save
```

## Installation Quick Reference

### For SDK Versions
```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
```

### For CLI Versions
```bash
pip install -r requirements.txt

# Install CLI tools
npm install -g @anthropic-ai/claude-cli  # or your preferred method
pip install openai

# Authenticate
claude auth login
export OPENAI_API_KEY=your_key_here
```

## Tips and Best Practices

1. **Start with Basic**: Try the basic version first, upgrade to enhanced if you need critical evaluation
2. **Use Enhanced for Facts**: Anything factual should use enhanced version
3. **CLI for Convenience**: If you already use CLI tools daily, CLI versions integrate better
4. **SDK for Integration**: If building an application, SDK versions give more control
5. **Save Important Sessions**: Use `--save` flag to keep records of valuable outputs
6. **Experiment with Iterations**: Start with 2, increase if needed (diminishing returns after 3-4)

## Common Issues

**Issue:** CLI version says command not found
**Solution:** Install the CLI tool and ensure it's in your PATH

**Issue:** SDK version says API key invalid
**Solution:** Check your `.env` file has correct keys with no extra spaces

**Issue:** Worker keeps accepting bad feedback (Basic version)
**Solution:** Switch to Enhanced version for critical evaluation

**Issue:** Too many iterations, getting expensive
**Solution:** Reduce `--iterations` or use haiku/cheaper models

## Getting Help

- Check the main [README.md](README.md) for comprehensive documentation
- See [example_usage.py](example_usage.py) for code examples
- See [example_enhanced_comparison.py](example_enhanced_comparison.py) for enhanced vs basic comparison
- Open an issue on GitHub for bugs or questions

---

**Quick Decision:**
- Creative work → `capl.py`
- Factual work → `capl_enhanced.py`
- Already use CLIs → Add `_cli` to the above
