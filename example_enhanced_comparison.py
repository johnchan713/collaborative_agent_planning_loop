#!/usr/bin/env python3
"""
Comparison: Basic CAPL vs Enhanced CAPL
Demonstrates the difference between blind feedback acceptance and critical evaluation
"""

from capl import create_capl_from_env
from capl_enhanced import create_capl_enhanced
from rich.console import Console


def compare_basic_vs_enhanced():
    """
    Compare basic CAPL (worker blindly follows feedback)
    vs enhanced CAPL (worker critically evaluates feedback)
    """
    console = Console()

    # A task where the critic might give questionable feedback
    prompt = """Calculate the square root of 144 and explain the mathematical principle.
    Also mention if there are multiple valid answers."""

    console.print("\n" + "="*80)
    console.print("[bold cyan]COMPARISON: Basic vs Enhanced CAPL[/bold cyan]")
    console.print("="*80)

    # Example 1: Basic CAPL
    console.print("\n[bold yellow]>>> Running BASIC CAPL (worker follows all feedback)[/bold yellow]\n")
    try:
        capl_basic = create_capl_from_env(max_iterations=2)
        result_basic = capl_basic.run(prompt, verbose=True)
        console.print("\n[bold]Basic CAPL Result:[/bold]")
        console.print("- Worker follows critic's feedback without question")
        console.print("- May incorporate invalid suggestions")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

    # Example 2: Enhanced CAPL
    console.print("\n[bold yellow]>>> Running ENHANCED CAPL (worker evaluates feedback critically)[/bold yellow]\n")
    try:
        capl_enhanced = create_capl_enhanced(max_iterations=2, enable_search=True)
        result_enhanced = capl_enhanced.run(prompt, verbose=True)
        console.print("\n[bold]Enhanced CAPL Result:[/bold]")
        console.print("- Worker evaluates critic's feedback for validity")
        console.print("- Can reject incorrect or unhelpful suggestions")
        console.print("- Defends correct work if critic is wrong")
        console.print("- Critic can verify facts (when search is implemented)")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


def demonstrate_critical_thinking():
    """
    Demonstrate scenarios where critical evaluation is important
    """
    console = Console()

    scenarios = [
        {
            "title": "Factual Task",
            "prompt": "What is the speed of light in vacuum? Provide the exact value and units.",
            "why": "Critic can fact-check the value, worker can defend if correct"
        },
        {
            "title": "Controversial Topic",
            "prompt": "Explain the benefits and drawbacks of nuclear energy.",
            "why": "Critic might have biases, worker should evaluate feedback objectively"
        },
        {
            "title": "Code Review",
            "prompt": "Write a function to check if a number is prime.",
            "why": "Worker can defend efficient algorithm if critic suggests slower approach"
        }
    ]

    console.print("\n" + "="*80)
    console.print("[bold cyan]WHY ENHANCED CAPL MATTERS[/bold cyan]")
    console.print("="*80 + "\n")

    for i, scenario in enumerate(scenarios, 1):
        console.print(f"[bold]{i}. {scenario['title']}[/bold]")
        console.print(f"   Task: {scenario['prompt']}")
        console.print(f"   [yellow]Why critical thinking helps:[/yellow] {scenario['why']}\n")


def show_key_differences():
    """Show the key differences between basic and enhanced versions."""
    console = Console()

    console.print("\n" + "="*80)
    console.print("[bold cyan]KEY DIFFERENCES: Basic vs Enhanced[/bold cyan]")
    console.print("="*80 + "\n")

    differences = [
        {
            "aspect": "Worker Response to Feedback",
            "basic": "Blindly follows all critic feedback",
            "enhanced": "Critically evaluates feedback, can accept or reject"
        },
        {
            "aspect": "Critic Capability",
            "basic": "Reviews based only on internal knowledge",
            "enhanced": "Can search for facts to verify claims (when implemented)"
        },
        {
            "aspect": "Worker Agency",
            "basic": "Passive - just refines as told",
            "enhanced": "Active - defends good work, explains decisions"
        },
        {
            "aspect": "Output Quality",
            "basic": "May degrade if critic is wrong",
            "enhanced": "Maintains quality even with flawed criticism"
        },
        {
            "aspect": "Transparency",
            "basic": "Just shows refined work",
            "enhanced": "Shows what feedback was accepted/rejected and why"
        }
    ]

    for diff in differences:
        console.print(f"[bold cyan]{diff['aspect']}:[/bold cyan]")
        console.print(f"  [red]Basic:[/red] {diff['basic']}")
        console.print(f"  [green]Enhanced:[/green] {diff['enhanced']}\n")


if __name__ == "__main__":
    import sys

    console = Console()

    # Show key differences
    show_key_differences()

    # Demonstrate scenarios
    demonstrate_critical_thinking()

    # Ask if user wants to run comparison
    console.print("\n[yellow]Do you want to run a live comparison? This will use API credits. (y/n)[/yellow]")
    choice = input("> ").lower()

    if choice == 'y':
        compare_basic_vs_enhanced()
    else:
        console.print("[dim]Comparison skipped. Run with 'y' to see live comparison.[/dim]")
