from gpt4all import GPT4All
import requests
from pathlib import Path

MODEL = GPT4All(
    model_name="gpt4all-falcon-q4_0.gguf",
#    model_path=(Path.home() / ".cache" / "gpt4all"),
# /root/.pyenv/versions/gpt-song-prompt/lib/python3.10/site-packages/gpt4all
    allow_download=True,
)
WORD_PROMPT = str(requests.get("https://random-word-api.herokuapp.com/word").text)[2:-2]
SYSTEM_TEMPLATE = 'A single sentence based on a word.'
PROMPT_TEMPLATE = '### Instruction: {0} \n### Response: '
with MODEL.chat_session(SYSTEM_TEMPLATE, PROMPT_TEMPLATE):
    response = MODEL.generate(f"A single sentence about {WORD_PROMPT}.", temp=0.7)
    print(WORD_PROMPT)
    resp = str(response.splitlines()[0])
    print(resp)
