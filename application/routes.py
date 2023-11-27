"""
Flask app that uses gpt4all to generate random song writing prompt.
"""
import os
import string
import random
from flask import (
    render_template,
    session,
)
from gpt4all import GPT4All
from datetime import datetime, timezone, timedelta
from pathlib import Path
from application import app

app.config.update(SECRET_KEY=os.urandom(24))
app.permanent_session_lifetime = timedelta(minutes=30)

MODEL = GPT4All(
    model_name="orca-mini-3b-gguf2-q4_0.gguf",
    model_path=(Path.home() / ".cache" / "gpt4all"),
    allow_download=False,
)
TIME_SIGNATURES=["2/4", "3/4", "4/4", "2/2", "6/8", "9/8", "12/8"]

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
def prompt_all():
    pass

@app.route("/")
def prompt_influence():
    pass
    response = MODEL.generate("The writing prompt is about the weather:", temp=0)
    session["list_response"] = response.splitlines()


if __name__ == "__main__":
    app.run(debug=True)
