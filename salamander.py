#!/usr/bin/env python3
import argparse
import json
import os
import requests

# Set up logging
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    parser = argparse.ArgumentParser(description="Interact with OpenAI's GPT-4 Turbo Preview API.")
    parser.add_argument('-i', '--input', required=True, help='Input file containing the prompt for GPT-4.')
    parser.add_argument('-o', '--output', help='Output file to write the response to. Prints to stdout if not specified.')

    args = parser.parse_args()

    # Read API key from environment variable
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logging.error("OPENAI_API_KEY environment variable not set.")
        return

    # Read prompt from input file
    try:
        with open(args.input, 'r') as file:
            prompt = file.read().strip()
    except Exception as e:
        logging.error(f"Failed to read input file: {e}")
        return

    # Prepare the request data
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "gpt-4-turbo-preview",
        "messages": [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": prompt}]
    }

    # Send the request
    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise an error for bad status codes
        result = response.json()
        output_content = result.get('choices', [{}])[0].get('message', {}).get('content', '')

        if args.output:
            with open(args.output, 'w') as file:
                file.write(output_content)
            logging.info(f"Response written to {args.output}")
        else:
            print(output_content)
    except Exception as e:
        logging.error(f"Failed to communicate with OpenAI API: {e}")

if __name__ == "__main__":
    main()
