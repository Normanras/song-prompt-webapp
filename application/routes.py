"""
Flask app that uses gpt4all to generate random song writing prompt.
"""
import os
import string
import random
import asyncio
from flask import (
    render_template,
    session,
    request,
)
from gpt4all import GPT4All
from datetime import timedelta
from application import app

# , AllWords, Themes
from sqlalchemy.sql.expression import func, select
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

# from werkzeug.middleware.profiler import ProfilerMiddleware

# app.wsgi_app = ProfilerMiddleware(
#     app.wsgi_app,
#     profile_dir="/Users/normrasmussen/Documents/Projects/gpt-song-prompt/flask-profiler/",
# )

engine = create_engine("sqlite:///words_prompts.db", pool_pre_ping=True)

Base = automap_base()
Base.prepare(engine, reflect=True)

Words = Base.classes.words
Themes = Base.classes.themes

app.config.update(SECRET_KEY=os.urandom(24))
app.permanent_session_lifetime = timedelta(minutes=30)

MODEL = GPT4All(
    model_name="gpt4all-falcon-q4_0.gguf",
    #    model_path=(Path.home() / ".cache" / "gpt4all"),
    allow_download=False,
)
TIME_SIGNATURES = ["2/4", "3/4", "4/4", "2/2", "6/8", "9/8", "12/8"]

# Need to decide between manually entering this list or using ascii_letters, below
KEYS = ["A", "B", "C", "D", "E", "F", "G"]
SIGN = ["b", "#"]
# Option 2
MINOR = string.ascii_letters[0:7]
MAJOR = string.ascii_letters[26:33]

async def grab_word():
    print("Running Grab_word func")
    await asyncio.sleep(1)
    while True:
        with Session(engine) as word_session:
            random_word = word_session.query(Words.words)
            random_word = random_word.order_by(func.random()).first()
            random_word = str(random_word)[4:-4]
            print(f"Word func, random word: {random_word}")
            return random_word


async def every(__seconds: float, func, *args, **kwargs):
    while True:
        func(*args, **kwargs)
        await asyncio.sleep(__seconds)


async def main():
    asyncio.ensure_future(grab_word())

with app.app_context():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(grab_word())
    loop.run_forever()


async def get_theme():
    # SYSTEM_TEMPLATE = "A single sentence based on a word."
    # PROMPT_TEMPLATE = "### Instruction: {0} \n### Response: "
    WORD_PROMPT = await grab_word()
    print(f"Theme Func, word: {WORD_PROMPT}")
    while True:
        response = MODEL.generate(
            f"Tell me about {WORD_PROMPT}.", temp=0.7, callback=stop_on_token_callback)
        with Session(engine) as thm_session:
            print(f"Theme func, response: {response}")
            thm_session.add(response)
            thm_session.commit()


@app.route("/")
def main_prompt():
    """
    Main function that loads the prompt
    """
    return render_template("index.html", title="Home")


@app.route("/all", methods=["GET", "POST"])
def prompt_all():
    if request.method == "POST":
        message = "Results are here"
        session["output_key"] = random.choice(KEYS) + random.choice(SIGN)
        session["output_signature"] = random.choice(TIME_SIGNATURES)
        with Session(engine) as word_session:
            random_theme = word_session.query(Themes.themes)
            session["output_theme"] = random_theme.order_by(func.random()).first()


        # with MODEL.chat_session(SYSTEM_TEMPLATE, PROMPT_TEMPLATE):
        #     response = MODEL.generate(f"A single sentence about {WORD_PROMPT}.", temp=0.7)
        #     session["output_theme"] = str(response.splitlines()[0])

        return render_template("single-button.html", title="Results", message=message)
    return render_template("single-button.html", title="Single Option")


def stop_on_token_callback(token_string):
    """
    Function to limit return length of the gpt4all response. Period indicates a sentence.
    """
    if "." in token_string:
        return False
    return True


if __name__ == "__main__":
    app.run(debug=True)
