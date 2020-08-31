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


@app.route('/reminder/<string:label>', methods=['GET', 'POST'])
def reminder(label: str):
    con: sqlite3.Connection = utils.create_connection(app.config['DATABASE_URI'])

    # Allows to pull request results in `dict` form
    con.row_factory = utils.dict_factory

    capitalized_label: str = label.capitalize()
    lower_label: str =label.lower()
    path: str = f"/reminder/{label.lower()}"

    if (request.method == 'POST'):
        # Build a `IndexItem` object (retrieve its `item_id`)
        query_index_item: str = "SELECT * FROM `index_items` WHERE item_label = ?;"
        res: dict = con.execute(query_index_item, (label, )).fetchone()  # E.g.: {'item_id': 1, 'item_label': 'pandas'}
        index_item = models.IndexItem(**res)

        # Create a Link object


        # Retrieve submitted values and store them in a `Reminder` instance
        # new_item = models.Reminder(**request.form)
        # new_item = models.Reminder(label=request.form['label'],
        #                            h1=request.form['h1'],
        #                            content_cell_1=request.form['content_cell_1'],
        #                            content_cell_2=request.form['content_cell_2'])

        try:
            # Push the item to the database
            con.execute("""INSERT INTO `reminder` (id, label, h1, content_cell_1, content_cell_2, lang, syntax_content, example_content, example_caption, link_text, link_href, link_type) 
                           VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""", (new_item.label, new_item.h1, new_item.content_cell_1, new_item.content_cell_2, new_item.lang, new_item.syntax_content, new_item.example_content, new_item.example_caption, new_item.link_text, new_item.link_href, new_item.link_type))
            # Save (commit) the changes
            con.commit()
            con.close()
            # Redirect to the reminder
            return redirect(path)
        except Exception as e:
            print(f"There was a problem adding your item. Error: {e}.", file=sys.stderr)
            con.close()
    else:
        res: sqlite3.Cursor = con.execute("SELECT * FROM `reminder` WHERE label = ?;", (label, ))
        items: list = sorted([models.Reminder(**row) for row in res], key=lambda el: el.h1)
        unique_titles: list = list(set([item.h1 for item in items]))
        con.close()
        return render_template('reminder.html',
                               capitalized_label=capitalized_label,
                               lower_label=lower_label,
                               path_action=path,
                               items=items,
                               unique_titles=unique_titles)


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
