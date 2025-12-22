#!/usr/bin/env python3
"""
Claude Opus Wrapper for CAPL CLI
This wrapper makes Anthropic API calls work with CAPL CLI versions
"""

import sys
import os
from anthropic import Anthropic

def main():
    # Get API key from environment
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)

    # Read prompt from stdin or file argument
    if len(sys.argv) > 1:
        # Check if argument is --file flag
        if sys.argv[1] == '--file' and len(sys.argv) > 2:
            with open(sys.argv[2], 'r') as f:
                prompt = f.read()
        else:
            # Treat as file path
            with open(sys.argv[1], 'r') as f:
                prompt = f.read()
    else:
        # Read from stdin
        prompt = sys.stdin.read()

    if not prompt.strip():
        print("Error: No prompt provided", file=sys.stderr)
        sys.exit(1)

    # Call Anthropic API
    try:
        client = Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-opus-4-5-20251101",
            max_tokens=8192,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # Output just the response text
        print(message.content[0].text)

    except Exception as e:
        print(f"Error calling Anthropic API: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
