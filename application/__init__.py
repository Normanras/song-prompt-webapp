from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from .utils import make_celery

app = Flask(__name__)
#    app.config.from_object(Config)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///words_prompts.db"
app.config["CELERY_CONFIG"] = {"broker_url": "redis://localhost"}
db = SQLAlchemy(app)

celery = make_celery(app)
celery.set_default()

Base = declarative_base()


class AllWords(Base, db.Model):
    word = db.Column(db.String, primary_key=True)

    def __init__(self, word):
        self.word = word


class Themes(Base, db.Model):
    themes = db.Column(db.String, primary_key=True)

    def __init__(self, themes):
        self.themes = themes

import application.routes
