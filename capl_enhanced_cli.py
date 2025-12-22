#!/usr/bin/env python3
"""
CAPL Enhanced CLI Version - Using CLI tools with critical thinking
Works with claude CLI and openai CLI (or custom CLI wrappers)
"""

import subprocess
import os
from typing import Optional, Dict, List, Tuple
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
import tempfile


class CAPLAgentCLI:
    """Base class for CLI-based CAPL agents."""

    def __init__(self, cli_command: str, role: str):
        self.cli_command = cli_command
        self.role = role

    def generate(self, prompt: str, context: Optional[str] = None) -> str:
        """Generate a response using CLI tool."""
        raise NotImplementedError


class ClaudeWorkerAgentEnhancedCLI(CAPLAgentCLI):
    """Enhanced Claude worker agent using CLI with critical evaluation."""

    def __init__(self, cli_command: str = "claude"):
        super().__init__(cli_command, "Worker")

    def generate(self, prompt: str, feedback: Optional[str] = None, previous_work: Optional[str] = None) -> str:
        """Generate or refine work with critical evaluation using Claude CLI."""
        if feedback:
            full_prompt = f"""You are an intelligent working AI agent. You previously worked on this task:

ORIGINAL TASK:
{prompt}

YOUR PREVIOUS WORK:
{previous_work}

CRITIC'S FEEDBACK:
{feedback}

INSTRUCTIONS:
A critic AI has reviewed your work. Your job is to:

1. **Critically evaluate the feedback** - Don't blindly accept it. Consider:
   - Is the criticism valid and well-reasoned?
   - Does it accurately understand your work?
   - Are the suggested improvements actually improvements?
   - Does the critic have any misconceptions?

2. **Make informed decisions**:
   - If the feedback is valid and helpful, incorporate it thoughtfully
   - If the feedback is incorrect or misguided, defend your original approach and explain why
   - If the feedback is partially valid, accept the good parts and explain why you're rejecting other parts
   - You can disagree with the critic if you have good reasons

3. **Provide your refined response** with:
   - Your updated work (incorporating valid feedback)
   - A brief note explaining what feedback you accepted/rejected and why (in a "Response to Critic" section)

Remember: You have agency and judgment. The critic's role is to help you improve, but you are responsible for the final output quality."""
        else:
            full_prompt = f"""You are an intelligent working AI agent. Please complete the following task:

{prompt}

Provide a thorough, well-reasoned, and accurate response."""

        return self._call_cli(full_prompt)

    def _call_cli(self, prompt: str) -> str:
        """Call Claude CLI with prompt."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(prompt)
            temp_file = f.name

        try:
            # Try: claude --file input.txt
            result = subprocess.run(
                [self.cli_command, '--file', temp_file],
                capture_output=True,
                text=True,
                timeout=180
            )

            if result.returncode != 0:
                # Try: echo "prompt" | claude
                result = subprocess.run(
                    [self.cli_command],
                    input=prompt,
                    capture_output=True,
                    text=True,
                    timeout=180
                )

            if result.returncode != 0:
                raise RuntimeError(f"Claude CLI failed: {result.stderr}")

            return result.stdout.strip()

        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)


class ChatGPTCriticAgentEnhancedCLI(CAPLAgentCLI):
    """Enhanced ChatGPT critic agent using CLI with fact-checking capability."""

    def __init__(self, cli_command: str = "openai", enable_search: bool = True):
        super().__init__(cli_command, "Critic")
        self.enable_search = enable_search

    def generate(self, prompt: str, work: str) -> Tuple[str, bool, Optional[str]]:
        """Critique with fact-checking using OpenAI CLI."""
        critique_prompt = f"""You are a critical AI reviewer with high standards. Your job is to analyze work produced by another AI and provide constructive, well-reasoned feedback.

ORIGINAL TASK:
{prompt}

AI'S WORK:
{work}

INSTRUCTIONS:
Provide a thorough critique that includes:

1. **Accuracy Check**:
   - Verify factual claims where possible
   - Note if you would need to search for information to verify specific claims
   - Identify any statements that seem questionable or need verification
   - List specific facts that should be checked: [List them if needed]

2. **Quality Assessment**:
   - What was done well
   - What could be improved
   - Any errors, inconsistencies, or missing elements
   - How well it addresses the original task

3. **Constructive Feedback**:
   - Be specific about what to change and why
   - Provide clear reasoning for your criticism
   - Acknowledge if you might be wrong about something
   - Consider alternative perspectives

4. **Overall Assessment**:
   - If the work is excellent and requires no significant improvements: Start with "APPROVED:"
   - If the work needs improvement: Start with "NEEDS WORK:"
   - If you need to verify facts before making a judgment: Start with "NEEDS VERIFICATION:" and list what needs to be checked

Be thorough, fair, and constructive."""

        feedback = self._call_cli(critique_prompt)
        is_approved = feedback.startswith("APPROVED:")
        needs_verification = feedback.startswith("NEEDS VERIFICATION:")

        search_summary = None
        if needs_verification and self.enable_search:
            search_summary = "[Search capability framework ready - implement web search as needed]"

        return feedback, is_approved, search_summary

    def _call_cli(self, prompt: str) -> str:
        """Call OpenAI CLI or wrapper with prompt."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(prompt)
            temp_file = f.name

        try:
            # Method 1: Try openai api chat.completions.create with correct syntax
            result = subprocess.run(
                [self.cli_command, 'api', 'chat.completions.create',
                 '-m', 'gpt-4o', '-g', 'user', prompt],
                capture_output=True,
                text=True,
                timeout=180
            )

            if result.returncode != 0:
                # Method 2: Try reading from file (for custom wrappers)
                result = subprocess.run(
                    [self.cli_command, temp_file],
                    capture_output=True,
                    text=True,
                    timeout=180
                )

            if result.returncode != 0:
                # Method 3: Try piping via stdin (for custom wrappers)
                result = subprocess.run(
                    [self.cli_command],
                    input=prompt,
                    capture_output=True,
                    text=True,
                    timeout=180
                )

            if result.returncode != 0:
                error_msg = f"OpenAI CLI failed: {result.stderr}\n\n"
                error_msg += "Hint: The OpenAI CLI has limited functionality. Consider:\n"
                error_msg += "1. Using the SDK version: capl_enhanced.py\n"
                error_msg += "2. Creating a wrapper script (see cli_wrappers/ directory)\n"
                error_msg += "3. Use --critic-cli to specify your own wrapper script"
                raise RuntimeError(error_msg)

            return result.stdout.strip()

        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)


class CAPLEnhancedCLI:
    """Enhanced Collaborative Agent Planning Loop using CLI tools."""

    def __init__(
        self,
        worker_agent: CAPLAgentCLI,
        critic_agent: CAPLAgentCLI,
        max_iterations: int = 2,
        console: Optional[Console] = None
    ):
        self.worker = worker_agent
        self.critic = critic_agent
        self.max_iterations = max_iterations
        self.console = console or Console()
        self.history: List[Dict] = []

    def run(self, prompt: str, verbose: bool = True) -> Dict:
        """Run enhanced collaborative planning loop using CLI tools."""
        self.console.print(Panel.fit(
            f"[bold cyan]CAPL Enhanced CLI Session Started[/bold cyan]\n"
            f"Worker: {self.worker.cli_command}\n"
            f"Critic: {self.critic.cli_command}\n"
            f"Max Iterations: {self.max_iterations}\n"
            f"[yellow]Enhanced with: Critical evaluation & Fact-checking[/yellow]",
            border_style="cyan"
        ))

        self.console.print(f"\n[bold]Original Prompt:[/bold]\n{prompt}\n")

        # Initial work generation
        self.console.print("[bold yellow]>>> Worker AI: Generating initial work via CLI...[/bold yellow]")
        current_work = self.worker.generate(prompt)

        iteration_data = {
            "iteration": 0,
            "work": current_work,
            "feedback": None,
            "approved": False,
            "worker_response_to_critic": None
        }
        self.history.append(iteration_data)

        if verbose:
            self.console.print(Panel(
                Markdown(current_work),
                title="[bold green]Initial Work[/bold green]",
                border_style="green"
            ))

        # Iterative refinement loop
        for iteration in range(1, self.max_iterations + 1):
            self.console.print(f"\n[bold blue]>>> Critic AI: Reviewing work via CLI (Iteration {iteration}/{self.max_iterations})...[/bold blue]")

            # Get critique
            if isinstance(self.critic, ChatGPTCriticAgentEnhancedCLI):
                feedback, is_approved, search_summary = self.critic.generate(prompt, current_work)
                if search_summary and verbose:
                    self.console.print(f"[dim]{search_summary}[/dim]")
            else:
                feedback, is_approved = self.critic.generate(prompt, current_work)
                search_summary = None

            iteration_data = {
                "iteration": iteration,
                "work": None,
                "feedback": feedback,
                "approved": is_approved,
                "worker_response_to_critic": None,
                "search_summary": search_summary
            }

            if verbose:
                self.console.print(Panel(
                    Markdown(feedback),
                    title=f"[bold blue]Critic Feedback - Iteration {iteration}[/bold blue]",
                    border_style="blue"
                ))

            if is_approved:
                self.console.print(f"\n[bold green]✓ Work approved by critic after {iteration} iteration(s)![/bold green]")
                iteration_data["work"] = current_work
                self.history.append(iteration_data)
                break

            if iteration < self.max_iterations:
                self.console.print(f"[bold yellow]>>> Worker AI: Evaluating feedback and refining via CLI...[/bold yellow]")

                # Worker critically evaluates and refines
                if isinstance(self.worker, ClaudeWorkerAgentEnhancedCLI):
                    refined_work = self.worker.generate(prompt, feedback, current_work)
                else:
                    refined_work = self.worker.generate(prompt, feedback)

                current_work = refined_work
                iteration_data["work"] = current_work

                if verbose:
                    self.console.print(Panel(
                        Markdown(current_work),
                        title=f"[bold green]Refined Work - Iteration {iteration}[/bold green]",
                        border_style="green"
                    ))
            else:
                self.console.print(f"\n[bold red]Maximum iterations ({self.max_iterations}) reached.[/bold red]")
                iteration_data["work"] = current_work

            self.history.append(iteration_data)

        result = {
            "final_work": current_work,
            "history": self.history,
            "total_iterations": len([h for h in self.history if h.get("feedback")]),
            "approved": self.history[-1].get("approved", False),
            "timestamp": datetime.now().isoformat()
        }

        self.console.print("\n" + "="*80)
        self.console.print(Panel.fit(
            "[bold cyan]CAPL Enhanced CLI Session Completed[/bold cyan]",
            border_style="cyan"
        ))

        return result

    def save_session(self, result: Dict, filename: Optional[str] = None):
        """Save the session results to a file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"capl_enhanced_cli_session_{timestamp}.md"

        with open(filename, 'w') as f:
            f.write(f"# CAPL Enhanced CLI Session Results\n\n")
            f.write(f"**Timestamp:** {result['timestamp']}\n")
            f.write(f"**Total Iterations:** {result['total_iterations']}\n")
            f.write(f"**Approved:** {result['approved']}\n\n")
            f.write(f"---\n\n")

            for item in result['history']:
                iteration = item['iteration']
                if iteration == 0:
                    f.write(f"## Initial Work\n\n")
                    f.write(f"{item['work']}\n\n")
                else:
                    f.write(f"## Iteration {iteration}\n\n")
                    f.write(f"### Critic Feedback\n\n")
                    f.write(f"{item['feedback']}\n\n")
                    if item.get('search_summary'):
                        f.write(f"**Search:** {item['search_summary']}\n\n")
                    if item['work']:
                        f.write(f"### Worker's Response & Refined Work\n\n")
                        f.write(f"{item['work']}\n\n")

            f.write(f"---\n\n")
            f.write(f"## Final Result\n\n")
            f.write(f"{result['final_work']}\n")

        self.console.print(f"[green]Session saved to: {filename}[/green]")


def create_capl_enhanced_cli(
    max_iterations: int = 2,
    worker_cli: str = "claude",
    critic_cli: str = "openai",
    enable_search: bool = True
) -> CAPLEnhancedCLI:
    """
    Create enhanced CAPL instance using CLI tools.

    Args:
        max_iterations: Maximum number of critic iterations
        worker_cli: Command for worker CLI (default: "claude")
        critic_cli: Command for critic CLI (default: "openai")
        enable_search: Enable fact-checking capability

    Returns:
        CAPLEnhancedCLI instance
    """
    worker = ClaudeWorkerAgentEnhancedCLI(worker_cli)
    critic = ChatGPTCriticAgentEnhancedCLI(critic_cli, enable_search)

    return CAPLEnhancedCLI(worker, critic, max_iterations=max_iterations)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="CAPL Enhanced CLI - With Critical Thinking")
    parser.add_argument("prompt", nargs="?", help="The task prompt")
    parser.add_argument("--iterations", type=int, default=2, help="Max iterations (default: 2)")
    parser.add_argument("--save", action="store_true", help="Save session results")
    parser.add_argument("--worker-cli", default="claude", help="Worker CLI command (default: claude)")
    parser.add_argument("--critic-cli", default="openai", help="Critic CLI command (default: openai)")
    parser.add_argument("--no-search", action="store_true", help="Disable web search")

    args = parser.parse_args()

    if not args.prompt:
        console = Console()
        console.print("[yellow]Enter your task:[/yellow]")
        prompt = input("> ")
    else:
        prompt = args.prompt

    try:
        capl = create_capl_enhanced_cli(
            max_iterations=args.iterations,
            worker_cli=args.worker_cli,
            critic_cli=args.critic_cli,
            enable_search=not args.no_search
        )
        result = capl.run(prompt, verbose=True)

        if args.save:
            capl.save_session(result)

    except Exception as e:
        Console().print(f"[bold red]Error: {e}[/bold red]")
        raise
