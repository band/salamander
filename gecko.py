#!/usr/bin/env python3
"""
  gecko.py is based on salamader.py, written by Peter Kaminski
  - one main difference is that this code is written to interact with Anthropic's Claude-3 API
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

    args = parser.parse_args()

    # Constants for API
    API_URL = "https://api.anthropic.com/v1/messages"
    MODEL = "claude-3-opus-20240229"

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
    headers = {
        "X-Api-Key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    data = {
        "model": MODEL,
        "max_tokens": 1024,
        "messages": [{"role": "user", "content": f"{prompt}"}]
    }
    logging.debug('data: %s ', data)
    # Send the request
    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(data))
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
