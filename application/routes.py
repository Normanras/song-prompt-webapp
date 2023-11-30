"""
Flask app that uses gpt4all to generate random song writing prompt.
"""
import os
import string
import random
import requests
from flask import (
    render_template,
    session,
    request,
)
from gpt4all import GPT4All
from datetime import datetime, timezone, timedelta
from pathlib import Path
from application import app

app.config.update(SECRET_KEY=os.urandom(24))
app.permanent_session_lifetime = timedelta(minutes=30)

MODEL = GPT4All(
    model_name="gpt4all-falcon-q4_0.gguf",
    model_path=(Path.home() / ".cache" / "gpt4all"),
    allow_download=True,
)
TIME_SIGNATURES = ["2/4", "3/4", "4/4", "2/2", "6/8", "9/8", "12/8"]

# Need to decide between manually entering this list or using ascii_letters, below
KEYS = ["A", "B", "C", "D", "E", "F", "G"]
SIGN = ["b", "#"]
# Option 2
MINOR = string.ascii_letters[0:7]
MAJOR = string.ascii_letters[26:33]
# and then use this:
# output = random.choice(KEYS)+random.choice(SIGN)


@app.route("/")
def main_prompt():
    """
    Main function that loads the prompt
    """
    return render_template("index.html", title="Home")


@app.route("/all", methods=["GET", "POST"])
def prompt_all():
    WORD_PROMPT = str(requests.get("https://random-word-api.herokuapp.com/word").text)[
        2:-2
    ]
    SYSTEM_TEMPLATE = 'A single sentence based on a word.'
    PROMPT_TEMPLATE = '### Instruction: {0} \n### Response: '
    if request.method == "POST":
        message = "Results are here"
        session["output_key"] = random.choice(KEYS) + random.choice(SIGN)
        session["output_signature"] = random.choice(TIME_SIGNATURES)
        session["word_prompt"] = WORD_PROMPT
        with MODEL.chat_session(SYSTEM_TEMPLATE, PROMPT_TEMPLATE):
            response = MODEL.generate(f"A single sentence about {WORD_PROMPT}.", temp=0.7)
            session["output_theme"] = str(response.splitlines()[0])


        #  numresp = len(response)- 1
        # if numresp <= 1:
        #    session["output_theme"] = str(response)
        # randresp = random.randrange(0, numresp)
        # session["output_theme"] = response
        return render_template("single-button.html", title="Results", message=message)
    return render_template("single-button.html", title="Single Option")


@app.route("/")
def prompt_instrument():
    pass


@app.route("/")
def prompt_key():
    pass


@app.route("/")
def prompt_timesig():
    pass


@app.route("/")
def prompt_influence():
    pass
    response = MODEL.generate("The writing prompt is about the weather:", temp=0)
    session["list_response"] = response.splitlines()


if __name__ == "__main__":
    app.run(debug=True)
