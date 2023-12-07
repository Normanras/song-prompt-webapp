"""
Flask app that uses gpt4all to generate random song writing prompt.
"""
import os
import string
from uuid import uuid4
import random
from flask import (
    render_template,
    session,
    request,
)
from redbeat import RedBeatSchedulerEntry
from application import app
from sqlalchemy.sql.expression import func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from celery import current_app as celery_app
# from celery.schedules import schedule

from werkzeug.middleware.profiler import ProfilerMiddleware

from .background_tasks import grab_word

app.wsgi_app = ProfilerMiddleware(
    app.wsgi_app,
    profile_dir="/Users/normrasmussen/Documents/Github/song-prompt-webapp/flask-profiler/",
)
engine = create_engine("sqlite:///words_prompts.db", pool_pre_ping=True)

Base = automap_base()
Base.prepare(engine, reflect=True)

Words = Base.classes.words
Themes = Base.classes.themes

app.config.update(SECRET_KEY=os.urandom(24))
# app.permanent_session_lifetime = timedelta(minutes=30)

TIME_SIGNATURES = ["2/4", "3/4", "4/4", "2/2", "6/8", "9/8", "12/8"]

# Need to decide between manually entering this list or using ascii_letters, below
KEYS = ["A", "B", "C", "D", "E", "F", "G"]
SIGN = ["b", "#"]
# Option 2
MINOR = string.ascii_letters[0:7]
MAJOR = string.ascii_letters[26:33]


@app.route("/", methods=["GET", "POST"])
def prompt_all():
    """
    Main function that loads the prompt
    """
    schedule_id = str(uuid4())
    interval = celery_app.schedule(run_every=60)
    entry = RedBeatSchedulerEntry(
        schedule_id, "application.background_tasks.grab_word", interval
    )
    entry.save()
    if request.method == "POST":
        message = "Results are here"
        session["output_key"] = random.choice(KEYS) + random.choice(SIGN)
        session["output_signature"] = random.choice(TIME_SIGNATURES)
        with Session(engine) as word_session:
            random_theme = word_session.query(Themes.themes)
        theme = random_theme.order_by(func.random()).first()
        session["output_theme"] = str(theme)[3:-3]

        return render_template("single-button.html", title="Results", message=message)
    return render_template("single-button.html", title="Single Option")


if __name__ == "__main__":
    app.run(debug=True)
