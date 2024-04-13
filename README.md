# Salamander - a simple LLM front end

#### 2024-03-03:
- forked this repo from Peter Kaminski
- expanded to include different LLM models

## Python programs:
	- these Python programs use the direct REST interface provided by
      the PyPI `requests` module and do not require the `pip`
      installation of LLM specific modules.  
	  
	- each LLM does require an API key  
	
- `salamander.py` is the original program written to provide OpenAI text
  output in response to an input file that contains some prompt text.

- `gecko.py` is a similar program that uses Anthropic's Claude-3-sonnet model.
  
- `iguana.py` uses Google's Gemini-Pro model.

### How to use these programs:

- One way to use these programs is to set up a local Python virtual
  environment and run them in the terminal:  
  - initial setup:  
  
``` shell
python3 -m venv venv
source venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```
  - My working practice is to activate the virtual environment  
   (`$ source venv/bin/activate`)  
   before running any code and deactivating (`$ deactivate`)  when done.  

  - run these programs (using a simple "why is the sky blue?" prompt):
    - first set up API keys: see `env.sh-template` for an example of how to
      do this.

``` shell
./salamander.py -i prompts/skybluePrompt.md
./gecko.py -i prompts/skybluePrompt.md
./iguana.py -i prompts/skybluePrompt.md
```
  
### Plans and TODOs:
   
 - experiment with some summarization and topic extraction prompts  
   - two examples in the `prompts/` directory
 
 - experiment with using the previous response as part of a topic and
   summarization conversation  

Please post issues.
