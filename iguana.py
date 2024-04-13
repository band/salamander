#!/usr/bin/env python3
"""
  anolis.py is based on salamader.py, written by Peter Kaminski, and its cousin gecko.py
  (Anolis is an iguanian lizard native to the Americas (https://en.wikipedia.org/wiki/Anolis))
  - this code is written to interact with Google's Gemini API
  2024-04-05 TODO: specify and document prompt structures and examples (applies here as well)
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

    # Read API key from environment variable
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        logging.error("GOOGLE_API_KEY environment variable not set.")
        return
    API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=" + api_key 

    # read prompt from input file
    try:
        with open(args.input, 'r') as file:
            prompt = file.read().strip()
    except Exception as e:
        logging.error(f"Failed to read input file: {e}")
        return
    logging.debug("the prompt: %s", prompt)

    # prepare the request data
    headers = {
        "content-type": "application/json",
    }

    data = {
        "contents": [ {"parts":[{"text":f"{prompt}"}]}]
    }
    logging.debug('data: %s ', data)

    # Send the request
    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise an error for bad status codes
        result = response.json()
        logging.debug("result: %s", result)
        output_content=result.get('candidates', [{}])[0].get('content', '').get('parts', [{}])[0].get('text', '')

        if args.output:
            with open(args.output, 'w') as file:
                file.write(output_content)
            logging.info(f"Response written to {args.output}")
        else:
            print(output_content)
    except Exception as e:
        logging.error(f"Failed to communicate with GOOGLE API: {e}")

if __name__ == "__main__":
    main()

