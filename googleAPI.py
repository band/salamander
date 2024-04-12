#!/bin/env/python3

import os
import google.generativeai as genai

#from dotenv import load_dotenv
#load_dotenv()

genai.configure(api_key=os.environ["PALM_API_KEY"])

model = genai.GenerativeModel('gemini-pro')

response = model.generate_content("Write a short life story of a billiard ball.")                

print(response.text)

