from flask import Flask
from . import models
from .views import app
from . import utils
import os


"""
The functions below are functions to run in the command line (CLI).
The idea of the `flask reinit-db` command is to start with a new database again.
During development, it is worth to use the `test-db` command with your own tests to 
verify that the database behaves as desired.
Run `flask --help` in the flask shell tool after having activated your virtual 
environment to get more information.
"""


@app.cli.command()
def create_index_items_table():
    """Create index_items Table."""
    utils.create_index_items_table(app)


@app.cli.command()
def drop_index_items_table():
    """Create index_items Table."""
    utils.drop_index_items_table(app)


@app.cli.command()
def create_reminder_table():
    """Create Reminder Table."""
    utils.create_reminder_table(app)


@app.cli.command()
def drop_reminder_table():
    """Drop Reminder Table."""
    utils.drop_reminder_table(app)

@app.cli.command()
def drop_reminder_table_data():
    """Drop data inside the Reminder Table."""
    utils.drop_reminder_table_data(app)


@app.cli.command()
def init_db():
    """Initialize the database with all tables."""
    utils.init_db(app)


@app.cli.command()
def drop_database():
    """Drops all tables of the database."""    
    utils.drop_index_items_table(app)
    utils.drop_commands_table(app)


@app.cli.command()
def reinit_db():
    """Overwrite the database file and initialize all tables again."""
    utils.reinit_db(app)


@app.cli.command()
def reset_db():
    """Overwrite the database file."""
    utils.reset_db(app)


@app.cli.command()
def enable_fk():
    """Enable foreign key constraint."""
    utils.enable_fk(app)


@app.cli.command()
def disable_fk():
    """Disable foreign key constraint."""
    utils.disable_fk(app)


@app.cli.command()
def test_db():
    """Database tests."""
    utils.test_db(app)
