from flask import Flask
# import sqlite3
from . import models
from .views import app
from . import utils


@app.cli.command()
def create_indexitem_table():
    """Create IndexItem Table."""
    utils.create_indexitem_table(app)


@app.cli.command()
def create_reminder_table():
    """Create Reminder Table."""
    utils.create_reminder_table(app)
