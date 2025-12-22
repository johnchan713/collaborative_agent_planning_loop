#!/usr/bin/env python3
"""
Example usage of CAPL - Collaborative Agent Planning Loop
"""

from capl import create_capl_from_env, ClaudeWorkerAgent, ChatGPTCriticAgent, CAPL


def example_basic_usage():
    """Basic usage with environment variables."""
    print("="*80)
    print("Example 1: Basic Usage with .env file")
    print("="*80)

    # Create CAPL instance from environment variables
    capl = create_capl_from_env(max_iterations=2)

    # Run with a sample prompt
    prompt = """Write a Python function that calculates the Fibonacci sequence up to n terms.
The function should be efficient, well-documented, and include error handling."""

    result = capl.run(prompt, verbose=True)

    # Optionally save the session
    capl.save_session(result)

    print(f"\nFinal work approved: {result['approved']}")
    print(f"Total iterations: {result['total_iterations']}")


def example_custom_api_keys():
    """Usage with API keys passed directly."""
    print("\n" + "="*80)
    print("Example 2: Custom API Keys")
    print("="*80)

    # You can pass API keys directly (useful for testing or custom configs)
    anthropic_key = "your_anthropic_api_key"
    openai_key = "your_openai_api_key"

    capl = create_capl_from_env(
        anthropic_api_key=anthropic_key,
        openai_api_key=openai_key,
        max_iterations=3  # Allow up to 3 critic iterations
    )

    prompt = "Explain the concept of blockchain technology in simple terms."

    result = capl.run(prompt, verbose=True)


def example_custom_models():
    """Usage with custom model selection."""
    print("\n" + "="*80)
    print("Example 3: Custom Model Selection")
    print("="*80)

    # You can specify different models
    capl = create_capl_from_env(
        max_iterations=2,
        worker_model="claude-opus-4-5-20251101",  # Claude Opus 4.5
        critic_model="gpt-4o"  # GPT-4o
    )

    prompt = """Design a RESTful API for a task management system.
Include endpoints, HTTP methods, request/response formats, and authentication."""

    result = capl.run(prompt, verbose=True)


def example_manual_setup():
    """Manual setup with full control."""
    print("\n" + "="*80)
    print("Example 4: Manual Agent Setup")
    print("="*80)

    import os
    from dotenv import load_dotenv

    load_dotenv()

    # Create agents manually
    worker = ClaudeWorkerAgent(
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        model="claude-opus-4-5-20251101"
    )

    critic = ChatGPTCriticAgent(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4o"
    )

    # Create CAPL with custom configuration
    capl = CAPL(
        worker_agent=worker,
        critic_agent=critic,
        max_iterations=2
    )

    prompt = "Write a short story about an AI that learns to appreciate art."

    result = capl.run(prompt, verbose=True)

    # Access detailed history
    print("\n" + "="*80)
    print("Session History:")
    print("="*80)
    for item in result['history']:
        print(f"Iteration {item['iteration']}:")
        if item['feedback']:
            print(f"  - Approved: {item['approved']}")


def example_different_tasks():
    """Examples with different types of tasks."""
    print("\n" + "="*80)
    print("Example 5: Different Task Types")
    print("="*80)

    capl = create_capl_from_env(max_iterations=2)

    # Code generation task
    code_prompt = """Create a Python class for a binary search tree with insert,
search, and delete methods. Include comprehensive docstrings and type hints."""

    print("\n>>> Task 1: Code Generation")
    result1 = capl.run(code_prompt, verbose=False)
    print(f"Result: {'✓ Approved' if result1['approved'] else '✗ Not approved'}")

    # Analysis task
    analysis_prompt = """Analyze the pros and cons of microservices architecture
versus monolithic architecture for a medium-sized e-commerce application."""

    print("\n>>> Task 2: Analysis")
    result2 = capl.run(analysis_prompt, verbose=False)
    print(f"Result: {'✓ Approved' if result2['approved'] else '✗ Not approved'}")

    # Creative task
    creative_prompt = """Design a gamification system for a fitness app that
encourages users to maintain consistent workout habits."""

    print("\n>>> Task 3: Creative Design")
    result3 = capl.run(creative_prompt, verbose=False)
    print(f"Result: {'✓ Approved' if result3['approved'] else '✗ Not approved'}")


if __name__ == "__main__":
    # Run the basic example
    # Uncomment other examples to try them

    try:
        example_basic_usage()

        # Uncomment to run other examples:
        # example_custom_models()
        # example_manual_setup()
        # example_different_tasks()

    except ValueError as e:
        print(f"\nError: {e}")
        print("\nPlease make sure you have:")
        print("1. Created a .env file (copy from .env.example)")
        print("2. Added your ANTHROPIC_API_KEY")
        print("3. Added your OPENAI_API_KEY")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        raise
