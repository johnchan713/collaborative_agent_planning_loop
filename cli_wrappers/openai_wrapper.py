#!/usr/bin/env python3
"""
OpenAI GPT-4o Wrapper for CAPL CLI
This wrapper makes OpenAI API calls work with CAPL CLI versions
"""

import sys
import os
from openai import OpenAI

def main():
    # Get API key from environment
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)

    # Read prompt from stdin or file argument
    if len(sys.argv) > 1:
        # Read from file
        with open(sys.argv[1], 'r') as f:
            prompt = f.read()
    else:
        # Read from stdin
        prompt = sys.stdin.read()

    if not prompt.strip():
        print("Error: No prompt provided", file=sys.stderr)
        sys.exit(1)

    # Call OpenAI API
    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4096
        )

        # Output just the response text
        print(response.choices[0].message.content)

    except Exception as e:
        print(f"Error calling OpenAI API: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
