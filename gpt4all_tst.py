from gpt4all import GPT4All
import requests
from pathlib import Path

MODEL = GPT4All(model_name="gpt4all-falcon-q4_0.gguf", model_path=(Path.home() / ".cache" / "gpt4all"), allow_download=True)
WORD_PROMPT = str(requests.get("https://random-word-api.herokuapp.com/word").text)[2:-2]
response = MODEL.generate(f"The theme is {WORD_PROMPT} and this song is about", temp=1)
print(WORD_PROMPT)
resp = response.splitlines().pop(0)
print(resp)
