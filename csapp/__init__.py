from flask import Flask
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


@app.cli.command()
def drop_reminder_table():
    """Drop Reminder Table."""
    utils.drop_reminder_table(app)

@app.cli.command()
def drop_reminder_table_data():
    """Drop data inside the Reminder Table."""
    utils.drop_reminder_table_data(app)


@app.cli.command()
def init_database():
    """Initialize the database."""
    utils.create_commands_table(app)
    utils.create_examples_table(app)
    utils.create_links_table(app)
    utils.create_commands_examples_table(app)
    utils.create_commands_links_table(app)


@app.cli.command()
def enable_fk():
    """Enable foreign key constraint."""
    utils.enable_fk(app)


@app.cli.command()
def disable_fk():
    """Disable foreign key constraint."""
    utils.disable_fk(app)