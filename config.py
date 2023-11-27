import os

class Config(object):
    SECRET_KEY = os.environ.get("SONGPROMPT") or "song-prompt"
