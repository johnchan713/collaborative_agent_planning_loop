#!/usr/bin/env python3
"""
CAPL CLI Version - Using command-line tools instead of API SDKs
Works with claude CLI and openai CLI (or custom CLI wrappers)
"""

import subprocess
import os
from typing import Optional, Dict, List, Tuple
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
import json
import tempfile


class CAPLAgentCLI:
    """Base class for CLI-based CAPL agents."""

    def __init__(self, cli_command: str, role: str):
        self.cli_command = cli_command
        self.role = role

    def generate(self, prompt: str, context: Optional[str] = None) -> str:
        """Generate a response using CLI tool."""
        raise NotImplementedError


class ClaudeWorkerAgentCLI(CAPLAgentCLI):
    """Claude worker agent using CLI."""

    def __init__(self, cli_command: str = "claude"):
        super().__init__(cli_command, "Worker")

    def generate(self, prompt: str, feedback: Optional[str] = None) -> str:
        """Generate or refine work using Claude CLI."""
        if feedback:
            full_prompt = f"""You are a working AI agent. You previously worked on this task:

{prompt}

A critic AI has reviewed your work and provided this feedback:

{feedback}

Please refine your work based on this feedback. Provide an improved version."""
        else:
            full_prompt = f"""You are a working AI agent. Please complete the following task:

{prompt}

Provide a thorough and well-reasoned response."""

        # Create temp file for prompt
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(full_prompt)
            temp_file = f.name

        try:
            # Call Claude CLI
            # Assuming: claude < input.txt or claude --file input.txt
            result = subprocess.run(
                [self.cli_command, '--file', temp_file],
                capture_output=True,
                text=True,
                timeout=120
            )

            if result.returncode != 0:
                # Try alternative: piping via stdin
                result = subprocess.run(
                    [self.cli_command],
                    input=full_prompt,
                    capture_output=True,
                    text=True,
                    timeout=120
                )

            if result.returncode != 0:
                raise RuntimeError(f"Claude CLI failed: {result.stderr}")

            return result.stdout.strip()

        finally:
            # Clean up temp file
            if os.path.exists(temp_file):
                os.unlink(temp_file)


class ChatGPTCriticAgentCLI(CAPLAgentCLI):
    """ChatGPT critic agent using OpenAI CLI."""

    def __init__(self, cli_command: str = "openai"):
        super().__init__(cli_command, "Critic")

    def generate(self, prompt: str, work: str) -> Tuple[str, bool]:
        """Critique using OpenAI CLI or wrapper."""
        critique_prompt = f"""You are a critical AI reviewer. Your job is to analyze work produced by another AI and provide constructive feedback.

Original Task:
{prompt}

AI's Work:
{work}

Please review this work critically and provide:
1. What was done well
2. What could be improved
3. Any errors, inconsistencies, or missing elements
4. Your overall assessment

If the work is excellent and requires no significant improvements, start your response with "APPROVED:"
If the work needs improvement, start your response with "NEEDS WORK:"

Be thorough but constructive in your criticism."""

        # Create temp file for prompt
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(critique_prompt)
            temp_file = f.name

        try:
            # Method 1: Try openai api chat.completions.create with correct syntax
            result = subprocess.run(
                [self.cli_command, 'api', 'chat.completions.create',
                 '-m', 'gpt-4o', '-g', 'user', critique_prompt],
                capture_output=True,
                text=True,
                timeout=120
            )

            if result.returncode != 0:
                # Method 2: Try reading from file (for custom wrappers)
                result = subprocess.run(
                    [self.cli_command, temp_file],
                    capture_output=True,
                    text=True,
                    timeout=120
                )

            if result.returncode != 0:
                # Method 3: Try piping via stdin (for custom wrappers)
                result = subprocess.run(
                    [self.cli_command],
                    input=critique_prompt,
                    capture_output=True,
                    text=True,
                    timeout=120
                )

            if result.returncode != 0:
                error_msg = f"OpenAI CLI failed: {result.stderr}\n\n"
                error_msg += "Hint: The OpenAI CLI has limited functionality. Consider:\n"
                error_msg += "1. Using the SDK version: capl.py\n"
                error_msg += "2. Creating a wrapper script (see cli_wrappers/ directory)\n"
                error_msg += "3. Use --critic-cli to specify your own wrapper script"
                raise RuntimeError(error_msg)

            feedback = result.stdout.strip()
            is_approved = feedback.startswith("APPROVED:")

            return feedback, is_approved

        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)


class CAPLCLI:
    """Collaborative Agent Planning Loop using CLI tools."""

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
        """Run the collaborative planning loop using CLI tools."""
        self.console.print(Panel.fit(
            f"[bold cyan]CAPL CLI Session Started[/bold cyan]\n"
            f"Worker: {self.worker.cli_command}\n"
            f"Critic: {self.critic.cli_command}\n"
            f"Max Iterations: {self.max_iterations}",
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
            "approved": False
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

            feedback, is_approved = self.critic.generate(prompt, current_work)

            iteration_data = {
                "iteration": iteration,
                "work": None,
                "feedback": feedback,
                "approved": is_approved
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
                self.console.print(f"[bold yellow]>>> Worker AI: Refining work via CLI...[/bold yellow]")
                current_work = self.worker.generate(prompt, feedback)
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
            "[bold cyan]CAPL CLI Session Completed[/bold cyan]",
            border_style="cyan"
        ))

        return result

    def save_session(self, result: Dict, filename: Optional[str] = None):
        """Save the session results to a file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"capl_cli_session_{timestamp}.md"

        with open(filename, 'w') as f:
            f.write(f"# CAPL CLI Session Results\n\n")
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
                    if item['work']:
                        f.write(f"### Refined Work\n\n")
                        f.write(f"{item['work']}\n\n")

            f.write(f"---\n\n")
            f.write(f"## Final Result\n\n")
            f.write(f"{result['final_work']}\n")

        self.console.print(f"[green]Session saved to: {filename}[/green]")


def create_capl_cli(
    max_iterations: int = 2,
    worker_cli: str = "claude",
    critic_cli: str = "openai"
) -> CAPLCLI:
    """
    Create a CAPL instance using CLI tools.

    Args:
        max_iterations: Maximum number of critic iterations
        worker_cli: Command for worker CLI (default: "claude")
        critic_cli: Command for critic CLI (default: "openai")

    Returns:
        CAPLCLI instance
    """
    worker = ClaudeWorkerAgentCLI(worker_cli)
    critic = ChatGPTCriticAgentCLI(critic_cli)

    return CAPLCLI(worker, critic, max_iterations=max_iterations)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="CAPL CLI - Using command-line tools")
    parser.add_argument("prompt", nargs="?", help="The task prompt")
    parser.add_argument("--iterations", type=int, default=2, help="Max iterations (default: 2)")
    parser.add_argument("--save", action="store_true", help="Save session results")
    parser.add_argument("--worker-cli", default="claude", help="Worker CLI command (default: claude)")
    parser.add_argument("--critic-cli", default="openai", help="Critic CLI command (default: openai)")

    args = parser.parse_args()

    if not args.prompt:
        console = Console()
        console.print("[yellow]Enter your task:[/yellow]")
        prompt = input("> ")
    else:
        prompt = args.prompt

    try:
        capl = create_capl_cli(
            max_iterations=args.iterations,
            worker_cli=args.worker_cli,
            critic_cli=args.critic_cli
        )
        result = capl.run(prompt, verbose=True)

        if args.save:
            capl.save_session(result)

    except Exception as e:
        Console().print(f"[bold red]Error: {e}[/bold red]")
        raise
