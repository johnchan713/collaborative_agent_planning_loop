# CAPL - Collaborative Agent Planning Loop

**Using multiple AI models to form a critic loop to improve each other's thinking in the working process**

CAPL is a Python framework that orchestrates multiple AI models in a collaborative refinement loop. One model acts as a "worker" to complete tasks, while another acts as a "critic" to review and provide feedback, enabling iterative improvement of AI-generated outputs.

## Overview

The Collaborative Agent Planning Loop (CAPL) implements an iterative refinement process:

1. **Worker Agent** (Claude Opus) generates an initial response to your prompt
2. **Critic Agent** (ChatGPT/GPT-4) reviews the work and provides detailed feedback
3. **Worker Agent** refines its output based on the criticism
4. This cycle repeats for a configurable number of iterations or until the critic approves

This approach leverages the strengths of different AI models and produces higher-quality, more thoughtful outputs through collaborative refinement.

## Features

### Core Features
- **Multi-Model Collaboration**: Combine Claude Opus (worker) with ChatGPT/GPT-4 (critic)
- **Configurable Iterations**: Set maximum number of refinement cycles (default: 2)
- **Early Termination**: Stops when critic approves the work
- **Rich Console Output**: Beautiful formatted output with progress tracking
- **Session History**: Complete history of all iterations and feedback
- **Export Results**: Save session results to Markdown files
- **Flexible Configuration**: Use environment variables or pass API keys directly
- **Command-Line Interface**: Easy to use from terminal
- **Python API**: Integrate into your own applications

### Enhanced Version (`capl_enhanced.py`) - Advanced Critical Thinking

The enhanced version adds intelligent evaluation capabilities:

**Worker AI Critical Evaluation:**
- **Agency & Judgment**: Worker doesn't blindly follow feedback - it critically evaluates whether criticism is valid
- **Defend Good Work**: Can reject incorrect or misguided criticism with explanations
- **Selective Incorporation**: Accepts valid suggestions while explaining why it rejects others
- **Transparent Reasoning**: Includes "Response to Critic" sections explaining decisions

**Critic AI Fact-Checking:**
- **Verification Capability**: Critic can identify claims that need fact-checking
- **Web Search Integration**: Framework for searching information to verify facts (extensible)
- **Uncertainty Acknowledgment**: Critic states when it needs more information
- **Evidence-Based Review**: Grounds criticism in verifiable facts when possible

**Why This Matters:**
- Not all criticism is valid - the worker should have agency to evaluate it
- Prevents quality degradation from incorrect feedback
- Creates more robust, defensible outputs
- Mirrors real collaborative processes where both parties think critically

See `example_enhanced_comparison.py` for demonstrations of these capabilities.

## Installation

### Prerequisites

- Python 3.8 or higher
- Anthropic API key (for Claude)
- OpenAI API key (for ChatGPT/GPT-4)

### Setup

1. Clone this repository:
```bash
git clone https://github.com/yourusername/collaborative_agent_planning_loop.git
cd collaborative_agent_planning_loop
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure API keys:
```bash
cp .env.example .env
# Edit .env and add your API keys
```

Your `.env` file should look like:
```
ANTHROPIC_API_KEY=your_anthropic_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

## Quick Start

### Command Line Usage

```bash
# Basic usage with 2 critic iterations (default)
python capl.py "Write a Python function to calculate prime numbers"

# Specify number of iterations
python capl.py "Explain quantum computing" --iterations 3

# Save session results to file
python capl.py "Design a REST API for a blog" --save

# Use different models
python capl.py "Write a poem about AI" --worker-model claude-opus-4-5-20251101 --critic-model gpt-4o
```

### Python API Usage

```python
from capl import create_capl_from_env

# Create CAPL instance
capl = create_capl_from_env(max_iterations=2)

# Run with your prompt
prompt = "Write a Python function that implements binary search"
result = capl.run(prompt, verbose=True)

# Save results
capl.save_session(result)

# Check results
print(f"Approved: {result['approved']}")
print(f"Iterations: {result['total_iterations']}")
print(f"Final work: {result['final_work']}")
```

### Enhanced Version Usage (With Critical Thinking)

Use `capl_enhanced.py` for tasks requiring critical evaluation:

**Command Line:**
```bash
# Use enhanced version with critical evaluation
python capl_enhanced.py "Calculate the gravitational constant and explain its significance"

# With options
python capl_enhanced.py "Explain blockchain technology" --iterations 3 --save
```

**Python API:**
```python
from capl_enhanced import create_capl_enhanced

# Create enhanced CAPL instance
capl = create_capl_enhanced(
    max_iterations=2,
    enable_search=True  # Enable fact-checking capability
)

# Run with critical thinking enabled
prompt = "What is the speed of light and why is it constant?"
result = capl.run(prompt, verbose=True)

# The worker will:
# - Critically evaluate critic's feedback
# - Defend correct information if critic is wrong
# - Explain what feedback was accepted/rejected

# The critic will:
# - Identify claims that need verification
# - Request searches for fact-checking (when implemented)
# - Provide evidence-based criticism
```

**When to use Enhanced vs Basic:**
- **Use Enhanced** for: Factual tasks, controversial topics, code review, complex analyses
- **Use Basic** for: Simple tasks, creative writing, brainstorming, exploratory work

## Examples

### Basic CAPL Examples
See `example_usage.py` for comprehensive examples including:

- Basic usage with environment variables
- Custom API keys
- Custom model selection
- Manual agent setup
- Different types of tasks (code, analysis, creative)

Run examples:
```bash
python example_usage.py
```

### Enhanced CAPL Comparison
See `example_enhanced_comparison.py` to understand the differences:

- Side-by-side comparison of basic vs enhanced
- Demonstrations of critical thinking in action
- Scenarios where worker defends against invalid criticism
- Examples of critic fact-checking

Run comparison:
```bash
python example_enhanced_comparison.py
```

## How It Works

### The CAPL Process

```
┌─────────────────────────────────────────────────────────┐
│ 1. User provides prompt                                 │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│ 2. Worker AI (Claude) generates initial work            │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│ 3. Critic AI (GPT) reviews and provides feedback        │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
          ┌───────┴───────┐
          │ Approved?     │
          └───────┬───────┘
                  │
        ┌─────────┴─────────┐
        │                   │
       YES                 NO
        │                   │
        │                   ▼
        │         ┌──────────────────────┐
        │         │ 4. Worker refines    │
        │         │    based on feedback │
        │         └──────────┬───────────┘
        │                    │
        │                    │
        │         ┌──────────┴───────────┐
        │         │ Max iterations       │
        │         │ reached?             │
        │         └──────────┬───────────┘
        │                    │
        │              ┌─────┴─────┐
        │             NO          YES
        │              │            │
        │              └────────────┘
        │                    │
        ▼                    ▼
┌─────────────────────────────────────────────────────────┐
│ 5. Return final work and complete history               │
└─────────────────────────────────────────────────────────┘
```

### Architecture

- **`CAPLAgent`**: Base class for agents
- **`ClaudeWorkerAgent`**: Implements worker using Anthropic's Claude
- **`ChatGPTCriticAgent`**: Implements critic using OpenAI's GPT models
- **`CAPL`**: Orchestrator managing the refinement loop

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `ANTHROPIC_API_KEY` | Your Anthropic API key | Yes |
| `OPENAI_API_KEY` | Your OpenAI API key | Yes |

### Command Line Arguments

```
python capl.py [prompt] [options]

Arguments:
  prompt                Task prompt for AI agents

Options:
  --iterations N        Maximum critic iterations (default: 2)
  --save               Save session results to file
  --worker-model M     Worker model (default: claude-opus-4-5-20251101)
  --critic-model M     Critic model (default: gpt-4o)
```

### Available Models

**Worker (Claude):**
- `claude-opus-4-5-20251101` (recommended)
- `claude-sonnet-4-5-20250929`
- Other Claude models

**Critic (OpenAI):**
- `gpt-4o` (recommended)
- `gpt-4-turbo`
- `gpt-4`
- Other GPT models

## Advanced Usage

### Custom Agent Configuration

```python
from capl import ClaudeWorkerAgent, ChatGPTCriticAgent, CAPL

# Create custom agents
worker = ClaudeWorkerAgent(
    api_key="your_anthropic_key",
    model="claude-opus-4-5-20251101"
)

critic = ChatGPTCriticAgent(
    api_key="your_openai_key",
    model="gpt-4o"
)

# Create CAPL with custom settings
capl = CAPL(
    worker_agent=worker,
    critic_agent=critic,
    max_iterations=3
)

# Run
result = capl.run("Your prompt here")
```

### Accessing Session History

```python
result = capl.run("Your prompt")

# Iterate through history
for item in result['history']:
    print(f"Iteration: {item['iteration']}")
    print(f"Work: {item['work']}")
    print(f"Feedback: {item['feedback']}")
    print(f"Approved: {item['approved']}")
```

### Programmatic API Keys

```python
from capl import create_capl_from_env

capl = create_capl_from_env(
    anthropic_api_key="sk-ant-...",
    openai_api_key="sk-...",
    max_iterations=2
)
```

## Use Cases

CAPL is ideal for tasks that benefit from iterative refinement:

- **Code Generation**: Generate well-tested, documented code
- **Technical Writing**: Create clear, accurate documentation
- **Analysis**: Develop thorough, balanced analyses
- **Design**: Refine system designs and architectures
- **Creative Writing**: Improve stories, articles, or content
- **Problem Solving**: Develop robust solutions to complex problems

## Output Format

CAPL provides rich console output with:
- Color-coded sections for worker and critic
- Formatted panels for work and feedback
- Progress indicators
- Clear approval status
- Iteration counts

Sessions can be saved to Markdown files containing:
- Complete iteration history
- All feedback and refinements
- Final approved work
- Metadata and timestamps

## Best Practices

1. **Start with 2 iterations**: Usually sufficient for most tasks
2. **Be specific in prompts**: Clear prompts lead to better results
3. **Review saved sessions**: Learn from the refinement process
4. **Experiment with models**: Different models excel at different tasks
5. **Use verbose mode**: Understand the refinement process
6. **Save important sessions**: Keep records of valuable outputs

## Troubleshooting

**API Key Errors:**
- Ensure `.env` file exists and contains valid keys
- Check that keys have proper permissions
- Verify no extra spaces or quotes in `.env`

**Model Errors:**
- Verify model names are correct
- Check API key has access to specified models
- Ensure sufficient API credits

**Import Errors:**
- Run `pip install -r requirements.txt`
- Check Python version (3.8+)

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## License

See LICENSE file for details.

## Acknowledgments

- Built with [Anthropic's Claude](https://www.anthropic.com/)
- Built with [OpenAI's GPT](https://openai.com/)
- Uses [Rich](https://github.com/Textualize/rich) for beautiful console output

## Contact

For questions or support, please open an issue on GitHub.

---

**CAPL** - Making AI better through collaboration
