#!/usr/bin/env python3
"""
CAPL - Collaborative Agent Planning Loop
Using multiple AI models to form a critic loop to improve each other's thinking in the working process.
"""

import os
from typing import Optional, Dict, List, Tuple
from datetime import datetime
from anthropic import Anthropic
from openai import OpenAI
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn


class CAPLAgent:
    """Base class for CAPL agents."""

    def __init__(self, api_key: str, model: str, role: str):
        self.api_key = api_key
        self.model = model
        self.role = role

    def generate(self, prompt: str, context: Optional[str] = None) -> str:
        """Generate a response based on the prompt."""
        raise NotImplementedError


class ClaudeWorkerAgent(CAPLAgent):
    """Claude Opus agent that performs the main work."""

    def __init__(self, api_key: str, model: str = "claude-opus-4-5-20251101"):
        super().__init__(api_key, model, "Worker")
        self.client = Anthropic(api_key=api_key)

    def generate(self, prompt: str, feedback: Optional[str] = None) -> str:
        """Generate or refine work based on prompt and optional feedback."""
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

        message = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            messages=[
                {"role": "user", "content": full_prompt}
            ]
        )

        return message.content[0].text


class ChatGPTCriticAgent(CAPLAgent):
    """ChatGPT agent that provides critical feedback."""

    def __init__(self, api_key: str, model: str = "gpt-4o"):
        super().__init__(api_key, model, "Critic")
        self.client = OpenAI(api_key=api_key)

    def generate(self, prompt: str, work: str) -> Tuple[str, bool]:
        """
        Critique the work and return feedback and approval status.

        Returns:
            Tuple[str, bool]: (feedback, is_approved)
        """
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

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert critical reviewer with high standards."},
                {"role": "user", "content": critique_prompt}
            ],
            max_tokens=2048
        )

        feedback = response.choices[0].message.content
        is_approved = feedback.startswith("APPROVED:")

        return feedback, is_approved


class CAPL:
    """Collaborative Agent Planning Loop orchestrator."""

    def __init__(
        self,
        worker_agent: CAPLAgent,
        critic_agent: CAPLAgent,
        max_iterations: int = 2,
        console: Optional[Console] = None
    ):
        self.worker = worker_agent
        self.critic = critic_agent
        self.max_iterations = max_iterations
        self.console = console or Console()
        self.history: List[Dict] = []

    def run(self, prompt: str, verbose: bool = True) -> Dict:
        """
        Run the collaborative planning loop.

        Args:
            prompt: The user's initial prompt/task
            verbose: Whether to print detailed progress

        Returns:
            Dict containing final work, history, and metadata
        """
        self.console.print(Panel.fit(
            f"[bold cyan]CAPL Session Started[/bold cyan]\n"
            f"Worker: {self.worker.model}\n"
            f"Critic: {self.critic.model}\n"
            f"Max Iterations: {self.max_iterations}",
            border_style="cyan"
        ))

        self.console.print(f"\n[bold]Original Prompt:[/bold]\n{prompt}\n")

        # Initial work generation
        self.console.print("[bold yellow]>>> Worker AI: Generating initial work...[/bold yellow]")
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
            self.console.print(f"\n[bold blue]>>> Critic AI: Reviewing work (Iteration {iteration}/{self.max_iterations})...[/bold blue]")

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
                self.console.print(f"[bold yellow]>>> Worker AI: Refining work based on feedback...[/bold yellow]")
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
            "[bold cyan]CAPL Session Completed[/bold cyan]",
            border_style="cyan"
        ))

        return result

    def save_session(self, result: Dict, filename: Optional[str] = None):
        """Save the session results to a file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"capl_session_{timestamp}.md"

        with open(filename, 'w') as f:
            f.write(f"# CAPL Session Results\n\n")
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


def create_capl_from_env(
    anthropic_api_key: Optional[str] = None,
    openai_api_key: Optional[str] = None,
    max_iterations: int = 2,
    worker_model: str = "claude-opus-4-5-20251101",
    critic_model: str = "gpt-4o"
) -> CAPL:
    """
    Create a CAPL instance with API keys from environment or parameters.

    Args:
        anthropic_api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
        openai_api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
        max_iterations: Maximum number of critic iterations
        worker_model: Model to use for worker agent
        critic_model: Model to use for critic agent

    Returns:
        CAPL instance ready to use
    """
    from dotenv import load_dotenv
    load_dotenv()

    anthropic_key = anthropic_api_key or os.getenv("ANTHROPIC_API_KEY")
    openai_key = openai_api_key or os.getenv("OPENAI_API_KEY")

    if not anthropic_key:
        raise ValueError("ANTHROPIC_API_KEY not found. Set it in .env file or pass as parameter.")
    if not openai_key:
        raise ValueError("OPENAI_API_KEY not found. Set it in .env file or pass as parameter.")

    worker = ClaudeWorkerAgent(anthropic_key, worker_model)
    critic = ChatGPTCriticAgent(openai_key, critic_model)

    return CAPL(worker, critic, max_iterations=max_iterations)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="CAPL - Collaborative Agent Planning Loop")
    parser.add_argument("prompt", nargs="?", help="The task prompt for the AI agents")
    parser.add_argument("--iterations", type=int, default=2, help="Maximum number of critic iterations (default: 2)")
    parser.add_argument("--save", action="store_true", help="Save session results to file")
    parser.add_argument("--worker-model", default="claude-opus-4-5-20251101", help="Worker model to use")
    parser.add_argument("--critic-model", default="gpt-4o", help="Critic model to use")

    args = parser.parse_args()

    if not args.prompt:
        console = Console()
        console.print("[yellow]No prompt provided. Please enter your task:[/yellow]")
        prompt = input("> ")
    else:
        prompt = args.prompt

    try:
        capl = create_capl_from_env(
            max_iterations=args.iterations,
            worker_model=args.worker_model,
            critic_model=args.critic_model
        )
        result = capl.run(prompt, verbose=True)

        if args.save:
            capl.save_session(result)

    except Exception as e:
        Console().print(f"[bold red]Error: {e}[/bold red]")
        raise
