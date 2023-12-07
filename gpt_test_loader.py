from gpt4all import GPT4All
import requests
from pathlib import Path


def prompt():
    MODEL = GPT4All(
        model_name="gpt4all-falcon-q4_0.gguf",
        #    model_path=(Path.home() / ".cache" / "gpt4all"),
        # /root/.pyenv/versions/gpt-song-prompt/lib/python3.10/site-packages/gpt4all
        allow_download=False,
    )
    WORD_PROMPT = str(requests.get("https://random-word-api.herokuapp.com/word").text)[
        2:-2
    ]
    SYSTEM_TEMPLATE = "A creative response about a word."
    PROMPT_TEMPLATE = "### Instruction: {0} \n### Response: "
    response = MODEL.generate(
        f"Tell me something interesting about {WORD_PROMPT}.",
        temp=0.7,
        callback=stop_on_token_callback,
    )
    print(response)

def stop_on_token_callback(token_id, token_string):
    if "." in token_string:
        return False
    return True


if __name__ == "__main__":
    prompt()
