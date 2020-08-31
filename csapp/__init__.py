from flask import Flask
from . import models
from .views import app
from . import utils
import os


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
    # utils.enable_fk(app)
    # utils.create_index_items_table(app)
    # utils.create_commands_table(app)
    # utils.create_examples_table(app)
    # utils.create_links_table(app)
    # print("Database initialized!")

    # utils.create_examples_table(app)
    # utils.create_links_table(app)
    # utils.create_commands_examples_table(app)
    # utils.create_commands_links_table(app)


@app.cli.command()
def drop_database():
    """Drops all tables of the database."""    
    utils.drop_index_items_table(app)
    utils.drop_commands_table(app)


@app.cli.command()
def reinit_db():
    """Overwrite the database file and initialize all tables again."""
    utils.reinit_db(app)
    # db_uri: str = app.config['DATABASE_URI']
    #
    # with open(db_uri, mode="w"):
    #     # The "w" method will overwrite the entire file.
    #     print("Database reinitialized!")


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
