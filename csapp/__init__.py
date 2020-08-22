from flask import Flask
# import sqlite3
from . import models
from .views import app
from . import utils


@app.cli.command()
def create_indexitem_table():
    """Create IndexItem Table."""
    utils.create_indexitem_table()
