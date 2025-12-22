#!/usr/bin/env python3
"""
CAPL Enhanced - Collaborative Agent Planning Loop with Critical Thinking
This version includes:
- Critic can search for information to verify facts
- Worker can critically evaluate feedback and reject invalid criticism
"""

import os
from typing import Optional, Dict, List, Tuple
from datetime import datetime
from anthropic import Anthropic
from openai import OpenAI
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown


class CAPLAgent:
    """Base class for CAPL agents."""

    def __init__(self, api_key: str, model: str, role: str):
        self.api_key = api_key
        self.model = model
        self.role = role

    def generate(self, prompt: str, context: Optional[str] = None) -> str:
        """Generate a response based on the prompt."""
        raise NotImplementedError


class ClaudeWorkerAgentEnhanced(CAPLAgent):
    """Enhanced Claude agent with critical evaluation of feedback."""

    def __init__(self, api_key: str, model: str = "claude-opus-4-5-20251101"):
        super().__init__(api_key, model, "Worker")
        self.client = Anthropic(api_key=api_key)

    def generate(self, prompt: str, feedback: Optional[str] = None, previous_work: Optional[str] = None) -> str:
        """Generate or refine work with critical evaluation of feedback."""
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

Remember: You have agency and judgment. The critic's role is to help you improve, but you are responsible for the final output quality. Stand by good work and defend it if needed."""
        else:
            full_prompt = f"""You are an intelligent working AI agent. Please complete the following task:

{prompt}

Provide a thorough, well-reasoned, and accurate response. Be prepared to defend your work and refine it based on constructive criticism."""

        message = self.client.messages.create(
            model=self.model,
            max_tokens=8192,
            messages=[
                {"role": "user", "content": full_prompt}
            ]
        )

        return message.content[0].text


class ChatGPTCriticAgentEnhanced(CAPLAgent):
    """Enhanced ChatGPT critic with web search capability for fact-checking."""

    def __init__(self, api_key: str, model: str = "gpt-4o", enable_search: bool = True):
        super().__init__(api_key, model, "Critic")
        self.client = OpenAI(api_key=api_key)
        self.enable_search = enable_search

    def _search_web(self, query: str) -> str:
        """Search the web for information (placeholder - implement based on your needs)."""
        # This is a placeholder. In production, you would:
        # - Use a web search API (e.g., Brave Search, Serper, etc.)
        # - Or use OpenAI's function calling with a search tool
        # - Or integrate with LangChain tools
        return f"[Web search for '{query}' would be performed here]"

    def generate(self, prompt: str, work: str) -> Tuple[str, bool, Optional[str]]:
        """
        Critique the work with optional web search for fact-checking.

        Returns:
            Tuple[str, bool, Optional[str]]: (feedback, is_approved, search_summary)
        """
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

Be thorough, fair, and constructive. Your criticism should help the worker improve, not just point out flaws."""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert critical reviewer who provides fair, constructive, and well-reasoned feedback. You verify facts when possible and acknowledge uncertainty."},
                {"role": "user", "content": critique_prompt}
            ],
            max_tokens=4096
        )

        feedback = response.choices[0].message.content

        # Check approval status
        is_approved = feedback.startswith("APPROVED:")
        needs_verification = feedback.startswith("NEEDS VERIFICATION:")

        # Extract search queries if verification is needed
        search_summary = None
        if needs_verification and self.enable_search:
            # In a full implementation, you would:
            # 1. Parse the verification requests from the feedback
            # 2. Perform web searches
            # 3. Re-evaluate with the search results
            search_summary = "[Search capability enabled but not implemented in this version]"

        return feedback, is_approved, search_summary


class CAPLEnhanced:
    """Enhanced Collaborative Agent Planning Loop with critical thinking."""

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
        Run the enhanced collaborative planning loop with critical thinking.

        Args:
            prompt: The user's initial prompt/task
            verbose: Whether to print detailed progress

        Returns:
            Dict containing final work, history, and metadata
        """
        self.console.print(Panel.fit(
            f"[bold cyan]CAPL Enhanced Session Started[/bold cyan]\n"
            f"Worker: {self.worker.model}\n"
            f"Critic: {self.critic.model}\n"
            f"Max Iterations: {self.max_iterations}\n"
            f"[yellow]Enhanced with: Critical evaluation & Fact-checking[/yellow]",
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
            self.console.print(f"\n[bold blue]>>> Critic AI: Reviewing work (Iteration {iteration}/{self.max_iterations})...[/bold blue]")

            # Get critique (with potential search)
            if isinstance(self.critic, ChatGPTCriticAgentEnhanced):
                feedback, is_approved, search_summary = self.critic.generate(prompt, current_work)
                if search_summary and verbose:
                    self.console.print(f"[dim]Search performed: {search_summary}[/dim]")
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
                self.console.print(f"[bold yellow]>>> Worker AI: Evaluating feedback and refining...[/bold yellow]")

                # Worker critically evaluates and refines
                if isinstance(self.worker, ClaudeWorkerAgentEnhanced):
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
            "[bold cyan]CAPL Enhanced Session Completed[/bold cyan]",
            border_style="cyan"
        ))

        return result

    def save_session(self, result: Dict, filename: Optional[str] = None):
        """Save the session results to a file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"capl_enhanced_session_{timestamp}.md"

        with open(filename, 'w') as f:
            f.write(f"# CAPL Enhanced Session Results\n\n")
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
                        f.write(f"**Search Performed:** {item['search_summary']}\n\n")
                    if item['work']:
                        f.write(f"### Worker's Response & Refined Work\n\n")
                        f.write(f"{item['work']}\n\n")

            f.write(f"---\n\n")
            f.write(f"## Final Result\n\n")
            f.write(f"{result['final_work']}\n")

        self.console.print(f"[green]Session saved to: {filename}[/green]")


def create_capl_enhanced(
    anthropic_api_key: Optional[str] = None,
    openai_api_key: Optional[str] = None,
    max_iterations: int = 2,
    worker_model: str = "claude-opus-4-5-20251101",
    critic_model: str = "gpt-4o",
    enable_search: bool = True
) -> CAPLEnhanced:
    """
    Create an enhanced CAPL instance.

    Args:
        anthropic_api_key: Anthropic API key
        openai_api_key: OpenAI API key
        max_iterations: Maximum number of critic iterations
        worker_model: Model for worker agent
        critic_model: Model for critic agent
        enable_search: Enable web search for critic (placeholder)

    Returns:
        CAPLEnhanced instance
    """
    from dotenv import load_dotenv
    load_dotenv()

    anthropic_key = anthropic_api_key or os.getenv("ANTHROPIC_API_KEY")
    openai_key = openai_api_key or os.getenv("OPENAI_API_KEY")

    if not anthropic_key:
        raise ValueError("ANTHROPIC_API_KEY not found")
    if not openai_key:
        raise ValueError("OPENAI_API_KEY not found")

    worker = ClaudeWorkerAgentEnhanced(anthropic_key, worker_model)
    critic = ChatGPTCriticAgentEnhanced(openai_key, critic_model, enable_search)

    return CAPLEnhanced(worker, critic, max_iterations=max_iterations)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="CAPL Enhanced - With Critical Thinking")
    parser.add_argument("prompt", nargs="?", help="The task prompt")
    parser.add_argument("--iterations", type=int, default=2, help="Max iterations (default: 2)")
    parser.add_argument("--save", action="store_true", help="Save session results")
    parser.add_argument("--worker-model", default="claude-opus-4-5-20251101")
    parser.add_argument("--critic-model", default="gpt-4o")
    parser.add_argument("--no-search", action="store_true", help="Disable web search")

    args = parser.parse_args()

    if not args.prompt:
        console = Console()
        console.print("[yellow]Enter your task:[/yellow]")
        prompt = input("> ")
    else:
        prompt = args.prompt

    try:
        capl = create_capl_enhanced(
            max_iterations=args.iterations,
            worker_model=args.worker_model,
            critic_model=args.critic_model,
            enable_search=not args.no_search
        )
        result = capl.run(prompt, verbose=True)

        if args.save:
            capl.save_session(result)

    except Exception as e:
        Console().print(f"[bold red]Error: {e}[/bold red]")
        raise
