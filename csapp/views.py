from flask import Flask, render_template, request, redirect
import sqlite3
import sys
import os
from . import utils
from . import models

app = Flask(__name__)
app.config.from_object('config')


@app.route('/', methods=['GET', 'POST'])
def index():
    con: sqlite3.Connection = sqlite3.connect(app.config['DATABASE_URI'])

    # Allows to pull request results in `dict` form
    con.row_factory = utils.dict_factory

    if request.method == 'POST':
        # Retrieve the submitted label value
        item_label: str = str(request.form['label'])
        # Create `IndexItem` instance (transforms automatically to lowercase the `item_label`)
        index_item = models.IndexItem(item_label)  # SQL command will manage how to set the `item_id` attribute

        try:
            # Push the item to the database
            sql_instruction: str = """INSERT INTO `index_items` (item_id, item_label) 
                                      VALUES (NULL, ?);"""
            con.execute(sql_instruction, (index_item.item_label, ))
            con.commit()
            con.close()
            # Redirect to the index
            return redirect('/')
        except Exception as e:
            con.close()
            print(f"There was a problem adding your item. Error: {e}.", file=sys.stderr)
    else:
        # Retrieve all the items stored in the database
        res: sqlite3.Cursor = con.execute("SELECT * FROM `index_items`;")
        items: list = [models.IndexItem(**row) for row in res]
        con.close()

        # # Create HTML file if it does not yet exist
        # filenames: list = [f"{item.label.lower()}.html" for item in items]

        # for filename in filenames:
        #     if not os.path.exists(f"./csapp/templates/{filename}"):
        #         with open(f"./csapp/templates/{filename}", mode='w') as f:
        #             f.write(utils.write_html(label=filename[:-5]))

        # labels: list = [item.label.lower() for item in items]

        return render_template('index.html', items=items)


@app.route('/cheatsheet/<string:label>', methods=['GET', 'POST'])
def cheatsheet(label: str):
    con: sqlite3.Connection = utils.create_connection(app.config['DATABASE_URI'])
    path: str = f"/cheatsheet/{label}"

    # Allows to pull request results in `dict` form
    con.row_factory = utils.dict_factory

    query_index_item: str = "SELECT * FROM `index_items` WHERE item_label = ?;"
    res: dict = con.execute(query_index_item, (label,)).fetchone()  # E.g.: {'item_id': 1, 'item_label': 'pandas'}
    # Build a `IndexItem` object (retrieve its `item_id`)
    index_item = models.IndexItem(**res)

    if request.method == 'POST' and len(request.form) == 6:
        # >>> print(request.form)
        # ImmutableMultiDict([('h1', '...'), ('command', '...'), ('description', '...'), ('lang', '...'),
        #                     ('syntax', '...'), ('label', '...')])
        try:
            # Push the item to the database
            insert_command: str = """INSERT INTO `commands` (command, description, syntax, lang, h1, item_id)
                                     VALUES (?, ?, ?, ?, ?, ?);"""
            values = (request.form["command"], request.form["description"], request.form["syntax"],
                      request.form['lang'], request.form['h1'], res['item_id'])
            con.execute(insert_command, values)
            con.commit()
            con.close()

            return redirect(path)
        except Exception as e:
            print(f"There was a problem adding your command. Error: {e}.", file=sys.stderr)
            con.close()
    elif request.method == 'POST' and len(request.form) == 3:
        print(request.form)
        try:
            insert_example: str = """INSERT INTO `examples` (example_caption, example_content, command_id)
                                     VALUES (?, ?, ?);"""
            values: tuple = (request.form['example_caption'], request.form['example_content'],
                             request.form['command_id'])
            con.execute(insert_example, values)
            con.commit()
            con.close()
            return redirect(path)
        except sqlite3.Error as e:
            print(f"There was a problem adding your example. Error: {e}.", file=sys.stderr)
            con.close()
    elif request.method == 'POST' and len(request.form) == 4:
        print(request.form)
        try:
            insert_link: str = """INSERT INTO `links` (link_label, link_href, link_type, command_id)
                                  VALUES (?, ?, ?, ?);"""
            values: tuple = (request.form['link_label'], request.form['link_href'],
                             request.form['link_type'], request.form['command_id'])
            con.execute(insert_link, values)
            con.commit()
            con.close()
            return redirect(path)
        except sqlite3.Error as e:
            print(f"There was a problem adding your link. Error: {e}.", file=sys.stderr)
            con.close()
    else:
        # Get the `item_id` from the label
        query_item_commands: str = "SELECT * FROM `commands` WHERE item_id = ?;"
        item_commands: list = con.execute(query_item_commands, (index_item.item_id, )).fetchall()

        for command in item_commands:
            command['item_label'] = label

        # Create Command objects
        item_commands: list = [models.Command(**row) for row in item_commands]

        # Add links to Command objects
        query_command_links: str = "SELECT link_label, link_href, link_type, link_id FROM `links` WHERE command_id = ?;"
        for command in item_commands:
            command_links: list = con.execute(query_command_links, (command.command_id,)).fetchall()
            if len(command_links) > 0:
                command.links = [models.Link(**link) for link in command_links]

        # Add examples to Command objects
        query_command_examples: str = """SELECT example_id, example_caption, example_content 
                                         FROM `examples` 
                                         WHERE command_id = ?;"""
        for command in item_commands:
            command_examples: list = con.execute(query_command_examples, (command.command_id,)).fetchall()
            if len(command_examples) > 0:
                command.examples = [models.Example(**example) for example in command_examples]

        return render_template('cheatsheet.html', label=label, path_action=path, item_commands=item_commands)


@app.route('/commands/<int:command_id>')
def commands(command_id: int):
    """Needed to send AJAX requests."""
    con: sqlite3.Connection = utils.create_connection(app.config['DATABASE_URI'])
    con.row_factory = utils.dict_factory

    query_command_examples: str = """SELECT example_id, example_caption, example_content 
                                     FROM `examples` 
                                     WHERE command_id = ?;"""

    command_examples: list = con.execute(query_command_examples, (command_id,)).fetchall()
    if len(command_examples) > 0:
        command_examples: list = [models.Example(**example) for example in command_examples]

    query_command_lang: str = """SELECT lang FROM `commands` WHERE command_id = ?;"""
    lang: dict = con.execute(query_command_lang, (command_id, )).fetchone()

    con.close()
    return render_template('commands.html', command_examples=command_examples, lang=lang['lang'])


@app.route('/links/<int:command_id>')
def links(command_id: int):
    """Needed to send AJAX requests."""
    con: sqlite3.Connection = utils.create_connection(app.config['DATABASE_URI'])
    con.row_factory = utils.dict_factory

    query_command_links: str = """SELECT link_id, link_label, link_href, link_type
                                  FROM `links` 
                                  WHERE command_id = ?;"""

    command_links: list = con.execute(query_command_links, (command_id,)).fetchall()
    if len(command_links) > 0:
        command_links: list = [models.Link(**link) for link in command_links]

    con.close()
    return render_template('links.html', command_links=command_links)


@app.route('/delete_command/<int:command_id>', methods=['GET', 'POST'])
def delete_command(command_id: int):
    con: sqlite3.Connection = utils.create_connection(app.config['DATABASE_URI'])
    con.row_factory = utils.dict_factory

    # Grab label for redirection purposes
    query_item_id: str = "SELECT item_id FROM `commands` WHERE command_id = ?;"
    item_id: int = con.execute(query_item_id, (command_id,)).fetchone()['item_id']
    # Having the item_id allows us to find the label
    query_item_label: str = "SELECT item_label FROM `index_items` WHERE item_id = ?"
    label: str = con.execute(query_item_label, (item_id,)).fetchone()['item_label']
    path: str = f"/cheatsheet/{label}"

    try:
        # Delete command
        con.execute("DELETE FROM `commands` WHERE command_id = ?;", (command_id, ))
        con.commit()
        con.close()
        return redirect(path)
    except sqlite3.Error as e:
        print(f"Failed to delete command with id {command_id}. Error: {e}.", file=sys.stderr)


@app.route('/delete_item/<int:item_id>', methods=['GET', 'POST'])
def delete_item(item_id: int):
    con: sqlite3.Connection = utils.create_connection(app.config['DATABASE_URI'])
    con.row_factory = utils.dict_factory

    try:
        # Delete item
        con.execute("DELETE FROM `index_items` WHERE item_id = ?;", (item_id,))
        con.commit()
        con.close()
        return redirect('/')
    except sqlite3.Error as e:
        print(f"Failed to delete command with id {item_id}. Error: {e}.", file=sys.stderr)
        con.close()


@app.route('/delete_example/<int:example_id>', methods=['GET', 'POST'])
def delete_example(example_id: int):
    con: sqlite3.Connection = utils.create_connection(app.config['DATABASE_URI'])
    con.row_factory = utils.dict_factory

    # Grab label for redirection purposes
    query_command_id: str = "SELECT command_id FROM `examples` WHERE example_id = ?;"
    command_id: int = con.execute(query_command_id, (example_id,)).fetchone()['command_id']
    query_item_id: str = "SELECT item_id FROM `commands` WHERE command_id = ?;"
    item_id: int = con.execute(query_item_id, (command_id,)).fetchone()['item_id']
    query_item_label: str = "SELECT item_label FROM `index_items` WHERE item_id = ?"
    label: str = con.execute(query_item_label, (item_id,)).fetchone()['item_label']
    path: str = f"/cheatsheet/{label}"

    try:
        # Delete item
        con.execute("DELETE FROM `examples` WHERE example_id = ?;", (example_id,))
        con.commit()
        con.close()
        return redirect(path)
    except sqlite3.Error as e:
        print(f"Failed to delete example with id {example_id}. Error: {e}.", file=sys.stderr)
        con.close()

@app.route('/delete_link/<int:link_id>', methods=['GET', 'POST'])
def delete_link(link_id: int):
    con: sqlite3.Connection = utils.create_connection(app.config['DATABASE_URI'])
    con.row_factory = utils.dict_factory

    # Grab label for redirection purposes
    query_command_id: str = "SELECT command_id FROM `links` WHERE link_id = ?;"
    command_id: int = con.execute(query_command_id, (link_id,)).fetchone()['command_id']
    query_item_id: str = "SELECT item_id FROM `commands` WHERE command_id = ?;"
    item_id: int = con.execute(query_item_id, (command_id,)).fetchone()['item_id']
    query_item_label: str = "SELECT item_label FROM `index_items` WHERE item_id = ?"
    label: str = con.execute(query_item_label, (item_id,)).fetchone()['item_label']
    path: str = f"/cheatsheet/{label}"

    try:
        # Delete item
        con.execute("DELETE FROM `links` WHERE link_id = ?;", (link_id,))
        con.commit()
        con.close()
        return redirect(path)
    except sqlite3.Error as e:
        print(f"Failed to delete link with id {link_id}. Error: {e}.", file=sys.stderr)
        con.close()
