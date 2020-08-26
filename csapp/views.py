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
    con.row_factory = utils.dict_factory

    if request.method == 'POST':
        # Retrieve the submitted label value
        item_label: str = str(request.form['label'])
        new_item = models.IndexItem(item_label)

        # Push the item to the database
        try:
            con.execute("INSERT INTO `indexitem` VALUES (NULL, ?);", (new_item.label, ))
            # Save (commit) the changes
            con.commit()
            con.close()
            # Redirect to the index
            return redirect('/')
        except Exception as e:
            con.close()
            print(f"There was a problem adding your item. Error: {e}.", file=sys.stderr)
    else:
        # Retrieve all the items stored in the database
        res: sqlite3.Cursor = con.execute("SELECT * FROM `indexitem`;")
        items: list = [models.IndexItem(**row) for row in res]
        con.close()

        # Create HTML file if it does not yet exist
        filenames: list = [f"{item.label.lower()}.html" for item in items]

        for filename in filenames:
            if not os.path.exists(f"./csapp/templates/{filename}"):
                with open(f"./csapp/templates/{filename}", mode='w') as f:
                    f.write(utils.write_html(label=filename[:-5]))

        # labels: list = [item.label.lower() for item in items]

        return render_template('index.html', items=items)


@app.route('/reminder/<string:label>', methods=['GET', 'POST'])
def reminder(label: str):
    con: sqlite3.Connection = sqlite3.connect(app.config['DATABASE_URI'])
    con.row_factory = utils.dict_factory

    capitalized_label: str = label.capitalize()
    lower_label: str =label.lower()
    path: str = f"/reminder/{label.lower()}"

    if (request.method == 'POST'):
        # Retrieve submitted values and store them in a `Reminder` instance
        # new_item = models.Reminder(**request.form)
        new_item = models.Reminder(label=request.form['label'], 
                                   h1=request.form['h1'], 
                                   content_cell_1=request.form['content_cell_1'], 
                                   content_cell_2=request.form['content_cell_2'])

        # Push the item to the database
        try:
            con.execute("""INSERT INTO `reminder` (id, label, h1, content_cell_1, content_cell_2) 
                           VALUES (NULL, ?, ?, ?, ?);""", (new_item.label, new_item.h1, new_item.content_cell_1, new_item.content_cell_2))
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
