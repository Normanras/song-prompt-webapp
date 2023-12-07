from celery import shared_task
from time import sleep
from redbeat import RedBeatSchedulerEntry
from sqlalchemy import create_engine
from sqlalchemy.sql.expression import func, select, insert
from sqlalchemy.ext.automap import automap_base
from gpt4all import GPT4All
from sqlalchemy.orm import Session
from celery import current_app as celery_app

from .extensions import db
from .models import Result

engine = create_engine("sqlite:///words_prompts.db", pool_pre_ping=True)

Base = automap_base()
Base.prepare(engine, reflect=True)

Words = Base.classes.words
Themes = Base.classes.themes

MODEL = GPT4All(
    model_name="gpt4all-falcon-q4_0.gguf",
    #    model_path=(Path.home() / ".cache" / "gpt4all"),
    allow_download=False,
)


@shared_task
def my_task(text, schedule_name):
    while True:
        with Session(engine) as word_session:
            random_word = word_session.query(Words.words)
            random_word = random_word.order_by(func.random()).first()
            random_word = str(random_word)[4:-4]
            # SYSTEM_TEMPLATE = "A single sentence based on a word."
            # PROMPT_TEMPLATE = "### Instruction: {0} \n### Response: "
            response = MODEL.generate(
                f"Give me a writing prompt about {random_word}.",
                temp=0.7,
                callback=stop_on_token_callback,
            )
            word_session.execute(insert(Themes).values(themes=response))
            word_session.commit()

    try:
        entry = RedBeatSchedulerEntry.from_key(
            "redbeat:" + schedule_name, app=celery_app
        )
    except KeyError:
        entry = None

    if entry:
        entry.delete()


def stop_on_token_callback(token_id, token_string):
    """
    Function to limit return length of the
    gpt4all response. Period indicates a sentence.
    """
    if "." in token_string:
        return False
    return True
