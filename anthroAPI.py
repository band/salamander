#!/bin/env/python3

import os
from anthropic import Anthropic
#from dotenv import load_dotenv
#load_dotenv()

client = Anthropic(
    # This is the default and can be omitted
    api_key=os.environ.get("ANTHROPIC_API_KEY3"),
)

message = client.messages.create(
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": 'write a summary sentence of the following text: Back in 2004, as the ‘war on terror’ heralded a new age of fear and violence, Rebecca Solnit published *Hope in the Dark*, an argument against despair in the face of an unknowable future. The book, which went on to be hailed as a *Guardian*‘best book of the 21st century’, insisted upon the world-shaping power of storytelling. ‘Stories trap us, stories free us, we live and die by stories,’ Solnit wrote. To her mind, ‘politics arises out of the spread of ideas and the shaping of imaginations. It means symbolic and cultural acts have real political power.’ In other words, ‘the change that counts in revolution takes place first in the imagination.’',
        }
    ],
    model="claude-3-opus-20240229",
)
print(message.content)
