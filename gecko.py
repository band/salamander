#!/usr/bin/env python3
"""
  gecko.py is based on salamader.py, written by Peter Kaminski
  - one main difference is that this code is written to interact with Anthropic's Claude-3 API
  2024-04-05 TODO: specify and document prompt structures and examples
"""
import argparse
import json
import os
import requests

# Set up logging
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    parser = argparse.ArgumentParser(description="Interact with Anthropic's Claude-3 API.")
    parser.add_argument('-i', '--input', required=True, help='Input file containing the prompt for Claude-3.')
    parser.add_argument('-o', '--output', help='Output file the response is written to. Prints to stdout if not specified.')
    parser.add_argument('-m', '--model', help="Claude-3 model to use; 'opus' (used if no model specified), 'sonnet', or 'haiku'")
    args = parser.parse_args()

    match args.model:
        case ["sonnet" | "opus"]:
            model = f"claude-3-{args.model}-20240229"
        case "haiku":
            model = f"claude-3-{args.model}-20240307"
        case _:
            model = 'claude-3-opus-20240229'

    # Read API key from environment variable
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        logging.error("ANTHROPIC_API_KEY environment variable not set.")
        return

    # Read prompt from input file
    try:
        with open(args.input, 'r') as file:
            prompt = file.read().strip()
    except Exception as e:
        logging.error(f"Failed to read input file: {e}")
        return
    logging.debug("the prompt: %s", prompt)

    # Prepare the request data
    api_url = "https://api.anthropic.com/v1/messages"

    headers = {
        "X-Api-Key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    data = {
        "model": model,
        "max_tokens": 1024,
        "messages": [{"role": "user", "content": f"{prompt}"}]
    }
    logging.debug('data: %s ', data)

    # Send the request
    try:
        response = requests.post(api_url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise an error for bad status codes
        result = response.json()
        logging.debug("result: %s", result)
        output_content = result.get('content', [{}])[0].get('text','')

        if args.output:
            with open(args.output, 'w') as file:
                file.write(output_content)
            logging.info(f"Response written to {args.output}")
        else:
            print(output_content)
    except Exception as e:
        logging.error(f"Failed to communicate with ANTHROPIC API: {e}")

if __name__ == "__main__":
    main()
