#!/usr/bin/env/python
"""
  kinose.py is based on salamader.py, written by Peter Kaminski
  - one main difference is that this code is written to interact with Cohere's API
  - Cohere returned "kinose" as a Cree name for a turtle
"""
import argparse
import json
import os
import requests

# Set up logging
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    parser = argparse.ArgumentParser(description="Interact with the Cohere API.")
    parser.add_argument('-i', '--input', required=True, help='Input file containing the prompt for Cohere.')
    parser.add_argument('-o', '--output', help='Output file the response is written to. Prints to stdout if not specified.')
    args = parser.parse_args()

    # Read API key from environment variable
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        logging.error("COHERE_API_KEY environment variable not set.")
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
    api_url = "https://api.cohere.ai/v1/generate"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "accept": "application/json"
    }
    data = {
        "prompt": f"{prompt}",
    }

    # Send the request
    try:
        response = requests.post(api_url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()['generations'][0]['text']
        else:
            print(f"Request failed with status code {response.status_code}")
            return None

        if args.output:
            with open(args.output, 'w') as file:
                file.write(output_content)
            logging.info(f"Response written to {args.output}")
        else:
            print(output_content)
    except Exception as e:
        logging.error(f"Failed to communicate with Cohere API: {e}")

if __name__ == "__main__":
    exit(main())
