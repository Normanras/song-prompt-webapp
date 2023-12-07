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
    # SYSTEM_TEMPLATE = "A creative response about a word."
    # PROMPT_TEMPLATE = "### Instruction: {0} \n### Response: "
    response = MODEL.generate(
        f"Give me a writing prompt where the writer has to write a song based on {WORD_PROMPT}.",
        temp=1,
        callback=stop_on_token_callback,
    )
    response2 = MODEL.generate(
        f"Give me a writing prompt about {WORD_PROMPT}.",
        #"Tell me one-sentence about Jitteriest.",
        temp=1,
        callback=stop_on_token_callback,
    )
    print("Make up a short story response:")
    print(response)
    print("\n")
    print("Tell me  one-sentence story about.")
    print(response2)

    # with MODEL.chat_session(SYSTEM_TEMPLATE, PROMPT_TEMPLATE):
    #     response = MODEL.generate(f"A single sentence about {WORD_PROMPT}.", temp=0.7)
    #     print(WORD_PROMPT)
    #     resp = str(response.splitlines()[0])
    #     print(resp)


def stop_on_token_callback(token_id, token_string):
    # per_amt = token_string.count('.')
    # while per_amt < 3:
    #     return True
    # return False
    if "." in token_string:
       return False
    return True


if __name__ == "__main__":
    prompt()
