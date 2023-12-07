from celery import shared_task
from redbeat import RedBeatSchedulerEntry
from celery import current_app as celery_app
from sqlalchemy.sql.expression import func, select, insert
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from gpt4all import GPT4All

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
def grab_word():
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


def stop_on_token_callback(token_id, token_string):
    """
    Function to limit return length of the
    gpt4all response. Period indicates a sentence.
    """
    if "." in token_string:
        return False
    return True


# def every(__seconds: float, func, *args, **kwargs):
#     while True:
#         func(*args, **kwargs)
#         await asyncio.sleep(__seconds)
#
#
# def main():
#     asyncio.ensure_future(grab_word())


# with app.app_context():
# loop = asyncio.get_event_loop()
# loop.run_until_complete(grab_word())
# loop.run_forever()


# async def get_theme(random_word):
#     print("Get Theme function running.")
#     # SYSTEM_TEMPLATE = "A single sentence based on a word."
#     # PROMPT_TEMPLATE = "### Instruction: {0} \n### Response: "
#     random_word = await random_word
#     print(f"Theme Func, word: {random_word}")
#     while True:
#         response = MODEL.generate(
#             f"Tell me about {random_word}.", temp=0.7, callback=stop_on_token_callback
#         )
#         with Session(engine) as thm_session:
#             print(f"Theme func, response: {response}")
#             thm_session.add(response)
#             thm_session.commit()
