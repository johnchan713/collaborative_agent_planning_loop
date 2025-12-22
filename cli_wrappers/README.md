# CLI Wrappers for CAPL

This directory contains wrapper scripts that make it easy to use CAPL CLI versions with the Anthropic and OpenAI APIs.

## Why Use These Wrappers?

The native OpenAI CLI has limited functionality and complex syntax. These wrappers provide a simple interface that works perfectly with CAPL's CLI versions while using the full API capabilities.

## Available Wrappers

### 1. `claude_wrapper.py` - Claude Opus Wrapper

Wraps the Anthropic API to work as a CLI tool.

**Requirements:**
- `ANTHROPIC_API_KEY` environment variable
- `anthropic` Python package (already in requirements.txt)

**Usage:**
```bash
# Via stdin
echo "Your prompt here" | ./claude_wrapper.py

# Via file
echo "Your prompt here" > prompt.txt
./claude_wrapper.py prompt.txt

# With --file flag (compatible with CAPL)
./claude_wrapper.py --file prompt.txt
```

### 2. `openai_wrapper.py` - GPT-4o Wrapper

Wraps the OpenAI API to work as a CLI tool.

**Requirements:**
- `OPENAI_API_KEY` environment variable
- `openai` Python package (already in requirements.txt)

**Usage:**
```bash
# Via stdin
echo "Your prompt here" | ./openai_wrapper.py

# Via file
echo "Your prompt here" > prompt.txt
./openai_wrapper.py prompt.txt
```

## Using with CAPL CLI

### Option 1: Set as Default (Recommended)

Create symbolic links or aliases:

```bash
# Make wrappers available system-wide
cd cli_wrappers
ln -s $(pwd)/claude_wrapper.py ~/bin/claude
ln -s $(pwd)/openai_wrapper.py ~/bin/openai

# Or add to your shell config (.bashrc, .zshrc):
alias claude='python3 /path/to/capl/cli_wrappers/claude_wrapper.py'
alias openai='python3 /path/to/capl/cli_wrappers/openai_wrapper.py'
```

Then use CAPL CLI normally:
```bash
python capl_cli.py "Your task here"
python capl_enhanced_cli.py "Your task here"
```

### Option 2: Specify Wrappers Directly

```bash
# Use wrappers with full paths
python capl_cli.py "Your task" \
  --worker-cli "./cli_wrappers/claude_wrapper.py" \
  --critic-cli "./cli_wrappers/openai_wrapper.py"

# Enhanced version
python capl_enhanced_cli.py "Your task" \
  --worker-cli "./cli_wrappers/claude_wrapper.py" \
  --critic-cli "./cli_wrappers/openai_wrapper.py" \
  --iterations 3
```

## Setup Instructions

### Quick Setup

1. **Set environment variables:**
```bash
export ANTHROPIC_API_KEY=your_anthropic_key_here
export OPENAI_API_KEY=your_openai_key_here

# Or add to your .env file
echo "ANTHROPIC_API_KEY=your_key" >> .env
echo "OPENAI_API_KEY=your_key" >> .env
```

2. **Test the wrappers:**
```bash
# Test Claude wrapper
echo "Say hello" | ./cli_wrappers/claude_wrapper.py

# Test OpenAI wrapper
echo "Say hello" | ./cli_wrappers/openai_wrapper.py
```

3. **Use with CAPL:**
```bash
python capl_cli.py "Explain quantum mechanics" \
  --worker-cli "./cli_wrappers/claude_wrapper.py" \
  --critic-cli "./cli_wrappers/openai_wrapper.py"
```

### Permanent Setup (Recommended)

Add to your `~/.bashrc` or `~/.zshrc`:

```bash
# CAPL CLI Wrappers
export CAPL_HOME="/path/to/collaborative_agent_planning_loop"
alias capl-claude="python3 $CAPL_HOME/cli_wrappers/claude_wrapper.py"
alias capl-openai="python3 $CAPL_HOME/cli_wrappers/openai_wrapper.py"

# Use with CAPL
alias capl="python3 $CAPL_HOME/capl_cli.py --worker-cli capl-claude --critic-cli capl-openai"
alias capl-enhanced="python3 $CAPL_HOME/capl_enhanced_cli.py --worker-cli capl-claude --critic-cli capl-openai"
```

Then simply:
```bash
capl "Your task here"
capl-enhanced "Your complex task" --iterations 3
```

## Customizing Wrappers

You can modify these wrappers to:
- Use different models
- Add custom system prompts
- Implement caching
- Add logging
- Change timeout values
- Add retry logic

Example - Use GPT-4 Turbo instead:
```python
# In openai_wrapper.py, change:
model="gpt-4o"
# to:
model="gpt-4-turbo"
```

## Creating Your Own Wrapper

Your wrapper just needs to:
1. Accept input via stdin or file argument
2. Call your AI service
3. Print the response to stdout

Example template:
```python
#!/usr/bin/env python3
import sys

def main():
    # Read input
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            prompt = f.read()
    else:
        prompt = sys.stdin.read()

    # Call your AI service
    response = your_ai_call(prompt)

    # Output response
    print(response)

if __name__ == "__main__":
    main()
```

## Troubleshooting

**Error: "ANTHROPIC_API_KEY environment variable not set"**
- Solution: Set your API key: `export ANTHROPIC_API_KEY=your_key`

**Error: "No module named 'anthropic'"**
- Solution: Install dependencies: `pip install -r requirements.txt`

**Error: "Permission denied"**
- Solution: Make executable: `chmod +x cli_wrappers/*.py`

**Error: "API key invalid"**
- Solution: Check your API keys are correct and active

## Advantages Over Native CLIs

1. **Full API Access**: Use all API features, not limited CLI subset
2. **Consistent Interface**: Same simple interface for both services
3. **Easy Customization**: Modify Python code as needed
4. **Better Error Handling**: Clear error messages
5. **No Complex Flags**: Simple stdin/file input, stdout output

## See Also

- [Main README](../README.md) - Complete CAPL documentation
- [Version Guide](../VERSION_GUIDE.md) - Choosing the right CAPL version
- [Example Usage](../example_usage.py) - Python API examples
