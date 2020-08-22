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
    # res: sqlite3.Cursor = con.execute("SELECT * FROM `indexitem`;")
    # items: list = [models.IndexItem(**row) for row in res]
    # con.close()
    # return render_template('index.html', items=items)

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


# con: sqlite3.Connection = sqlite3.connect(app.config['DATABASE_URI'])
# con.row_factory = utils.dict_factory
# res: sqlite3.Cursor = con.execute("SELECT * FROM `indexitem`;")
# items: list = [models.IndexItem(**row) for row in res]
# lower_labels: list = [item.lower_label for item in items]

# @app.route('/reminder/<str:label>', methods=['GET', 'POST'])
# def reminder(label):
#     return render_template(f"{label}.html")

# @app.route('/pandas/', methods=['GET', 'POST'])
# def pandas():
#     return render_template('pandas.html')
