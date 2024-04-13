#!/usr/bin/env python3
import argparse
import json
import logging
import os
import sys
import requests

# Constants for API
API_URL = "https://api.anthropic.com/v1/messages"
API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL = "claude-3-opus-20240229"

# Configure logging
logging.basicConfig(level=logging.INFO)

def send_message(input_data):
    headers = {
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    data = {
        "model": MODEL,
        "max_tokens": 1024,
        "messages": input_data
    }
    response = requests.post(API_URL, headers=headers, json=data)
    response.raise_for_status()  # Raises an exception for 4XX/5XX errors
    return response.json()

def format_response(response):
    return json.dumps(response, indent=4)

def main():
    parser = argparse.ArgumentParser(description='Gecko: Interface with an Anthropic API')
#    parser.add_argument('-i', '--input', type=argparse.FileType('r'), default=sys.stdin,
#                        help='Optional input file containing JSON messages')
    parser.add_argument('-i','--input',required=True, type=argparse.FileType('r'),help='input file of JSON messages')
    parser.add_argument('-o', '--output', type=argparse.FileType('w'), default=sys.stdout,
                        help='Optional output file for API responses')
    args = parser.parse_args()
    logging.info("input file: %s", args.input.name)

    try:
        input_data = json.load(args.input.name)
        logging.info("Sending message to API")
        response = send_message(input_data)
        formatted_response = format_response(response)
        args.output.write(formatted_response)
        args.output.write("\n")
        logging.info("Response received and written to output")
    except Exception as e:
        logging.error(f"Error occurred: {e}")

if __name__ == "__main__":
    main()
