# CAPL - Collaborative Agent Planning Loop

**Multi-AI critic loop for improved thinking and output quality**

CAPL orchestrates multiple AI models in a collaborative refinement loop. Claude Opus acts as a "worker" to complete tasks, while ChatGPT/Codex acts as a "critic" to review and provide feedback, enabling iterative improvement through multiple rounds of refinement.

## Overview

The Collaborative Agent Planning Loop (CAPL) implements an iterative refinement process:

1. **Worker AI** (Claude) generates an initial response to your prompt
2. **Critic AI** (Codex/ChatGPT) reviews the work and provides detailed feedback
3. **Worker AI** critically evaluates the feedback and refines its output
4. **Critic AI** reviews again
5. This cycle repeats for a configurable number of iterations (default: 2)

Each iteration produces progressively better results through collaborative refinement.

## Key Features

### Critical Thinking & Agency

**Worker AI Intelligence:**
- **Critical Evaluation**: Worker doesn't blindly follow feedback - it evaluates whether criticism is valid
- **Defend Good Work**: Can reject incorrect or misguided criticism with explanations
- **Selective Incorporation**: Accepts valid suggestions while explaining why it rejects others
- **Transparent Reasoning**: Shows its thinking process when evaluating feedback

**Critic AI Capabilities:**
- **Fact-Checking**: Identifies claims that need verification
- **Evidence-Based Review**: Provides specific, actionable feedback
- **Constructive Criticism**: Balances what's done well with areas for improvement

### Technical Features

- **CLI-Based**: Uses `claude` and `codex` CLI tools - no API key management needed
- **Configurable Iterations**: Set max refinement cycles (default: 2)
- **Rich Console Output**: Beautiful formatted output with progress tracking
- **Final Work Display**: Clear presentation of the refined final result
- **Session History**: Complete history of all iterations and feedback
- **Export Results**: Save sessions to Markdown files

## Installation

### Prerequisites

- Python 3.8 or higher
- `claude` CLI tool installed and authenticated
- `codex` CLI tool installed and authenticated

### Setup

1. Clone this repository:
```bash
git clone https://github.com/yourusername/collaborative_agent_planning_loop.git
cd collaborative_agent_planning_loop
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Verify CLI tools are working:
```bash
# Test claude CLI
claude --version

# Test codex CLI
codex exec --full-auto "Say hello"
```

**Installing CLI Tools:**

For Claude CLI - check [Anthropic's official documentation](https://www.anthropic.com/)

For Codex CLI - check your CLI tool provider's documentation

## Usage

### Basic Usage

```bash
# Run CAPL with default settings (2 iterations)
python3 capl_enhanced_cli.py "Explain quantum mechanics in 100 words"

# Specify custom number of iterations
python3 capl_enhanced_cli.py "Write a sorting algorithm in Python" --iterations 3

# Save session results to file
python3 capl_enhanced_cli.py "Design a REST API" --save

# Use custom CLI commands
python3 capl_enhanced_cli.py "Your task" \
  --worker-cli "/path/to/claude" \
  --critic-cli "/path/to/codex"
```

### Command Line Options

```
python3 capl_enhanced_cli.py [prompt] [options]

Arguments:
  prompt                Task prompt for AI agents (or enter interactively)

Options:
  --iterations N        Maximum critic iterations (default: 2)
  --save               Save session results to Markdown file
  --worker-cli CMD     Worker CLI command (default: "claude")
  --critic-cli CMD     Critic CLI command (default: "codex")
  --no-search          Disable fact-checking capability
```

## How It Works

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
│ 3. Critic AI (Codex) reviews and provides feedback      │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│ 4. Worker critically evaluates feedback and refines     │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
          ┌───────┴───────┐
          │ Max iterations│
          │ reached?      │
          └───────┬───────┘
                  │
        ┌─────────┴─────────┐
       NO                  YES
        │                   │
        └─► Loop back       └─► Display final work
```

## Example Output

```bash
$ python3 capl_enhanced_cli.py "explain quantum mechanics in 100 words"

╭────────────────────────────────────────────────────╮
│ CAPL Enhanced CLI Session Started                  │
│ Worker: claude                                     │
│ Critic: codex                                      │
│ Max Iterations: 2                                  │
│ Enhanced with: Critical evaluation & Fact-checking │
╰────────────────────────────────────────────────────╯

>>> Worker AI: Generating initial work via CLI...
╭─────────────────────── Initial Work ───────────────────────╮
│ [Initial explanation of quantum mechanics]                 │
╰────────────────────────────────────────────────────────────╯

>>> Critic AI: Reviewing work via CLI (Iteration 1/2)...
╭────────────────── Critic Feedback - Iteration 1 ───────────╮
│ NEEDS WORK: [Detailed feedback with specific suggestions]  │
╰────────────────────────────────────────────────────────────╯

>>> Worker AI: Evaluating feedback and refining via CLI...
╭────────────────── Refined Work - Iteration 1 ──────────────╮
│ [Worker's analysis of feedback and improved version]       │
╰────────────────────────────────────────────────────────────╯

>>> Critic AI: Reviewing work via CLI (Iteration 2/2)...
╭────────────────── Critic Feedback - Iteration 2 ───────────╮
│ NEEDS WORK: [More refined feedback]                        │
╰────────────────────────────────────────────────────────────╯

>>> Worker AI: Evaluating feedback and refining via CLI...
╭────────────────── Refined Work - Iteration 2 ──────────────╮
│ [Final refined version with worker's reasoning]            │
╰────────────────────────────────────────────────────────────╯

╭──────────────────────── Final Work ────────────────────────╮
│ [Final polished explanation after 2 rounds of refinement]  │
╰────────────────────────────────────────────────────────────╯

╭─────────────────────────────────────╮
│ CAPL Enhanced CLI Session Completed │
╰─────────────────────────────────────╯
```

## Use Cases

CAPL is ideal for tasks that benefit from iterative refinement:

- **Technical Writing**: Create clear, accurate explanations and documentation
- **Code Generation**: Generate well-structured, commented code
- **Analysis**: Develop thorough, balanced analyses of complex topics
- **Problem Solving**: Refine solutions through critical evaluation
- **Creative Writing**: Improve content through constructive feedback
- **Learning**: Understand topics through multi-perspective refinement

## Session Files

When using `--save`, CAPL creates a Markdown file containing:

- Complete iteration history
- All feedback exchanges
- Worker's reasoning for accepting/rejecting feedback
- Final refined work
- Metadata and timestamps

Files are saved as: `capl_enhanced_cli_session_YYYYMMDD_HHMMSS.md`

## Best Practices

1. **Start with 2 iterations**: Usually sufficient for most tasks
2. **Be specific in prompts**: Clear prompts lead to better results
3. **Review the reasoning**: Pay attention to how worker evaluates feedback
4. **Save important sessions**: Keep records of valuable refinements
5. **Adjust iterations**: Use more iterations for complex tasks

## Troubleshooting

**CLI tool not found:**
- Verify `claude` and `codex` are installed and in your PATH
- Test with `claude --version` and `codex exec --full-auto "test"`

**Permission errors:**
- Ensure CLI tools are authenticated properly
- Check that tools can be executed from your terminal

**Slow responses:**
- Normal - AI generation takes time, especially for complex tasks
- Increase timeout if needed (edit `timeout` parameters in script)

**Import errors:**
- Run `pip install -r requirements.txt`
- Verify Python 3.8+ with `python3 --version`

## Technical Details

### Architecture

- **ClaudeWorkerAgentEnhancedCLI**: Worker agent with critical evaluation
- **CodexCriticAgentEnhancedCLI**: Critic agent with fact-checking
- **CAPLEnhancedCLI**: Orchestrator managing the refinement loop
- Uses `subprocess.run()` to execute CLI commands
- `codex exec --full-auto` for non-interactive critic execution

### Requirements

See `requirements.txt`:
- `anthropic>=0.40.0` (for types/reference)
- `openai>=1.54.0` (for types/reference)
- `python-dotenv>=1.0.0`
- `rich>=13.7.0` (console formatting)

## Contributing

Contributions are welcome! Please submit pull requests or open issues.

## License

See LICENSE file for details.

## Acknowledgments

- Built with [Anthropic's Claude](https://www.anthropic.com/)
- Built with [OpenAI's Codex/ChatGPT](https://openai.com/)
- Uses [Rich](https://github.com/Textualize/rich) for console output

---

**CAPL** - Better AI through collaborative refinement
