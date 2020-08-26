if __name__ != "__main__":
    from csapp import models
import sqlite3


def dict_factory(cursor, row):
    return dict([(col[0], row[idx]) for idx, col in enumerate(cursor.description)])


def create_indexitem_table(app):
    # Start connection with the database (also creates the file if it does not yet exist)
    con: sqlite3.Connection = sqlite3.connect(app.config['DATABASE_URI'])

    # Using the nonstandard `execute()` method of the `Connection` object, we don't have to create the `Cursor` objects explicitly
    con.execute("""CREATE TABLE IF NOT EXISTS `indexitem` 
                   (id INTEGER PRIMARY KEY ASC, label VARCHAR NOT NULL UNIQUE);""")
    
    con.commit()
    con.close()


def create_reminder_table(app):
    con: sqlite3.Connection = sqlite3.connect(app.config['DATABASE_URI'])
    con.execute("""CREATE TABLE IF NOT EXISTS `reminder` 
                   (id INTEGER PRIMARY KEY ASC, label VARCHAR, h1 TEXT, content_cell_1 TEXT, content_cell_2 TEXT);""")
    con.commit()
    con.close()


def write_html(label: str):
    if not isinstance(label, str):
        raise TypeError(f"'str' expected, not {type(label).__name__!r}.")

    capitalized_label: str = label.capitalize()

    return f"""{{% extends 'base.html' %}}

{{% block head %}}
    <link rel="stylesheet" href="{{{{ url_for('static', filename='css/cheatsheet.css', _external=True) }}}}">
    <title>{capitalized_label} Reminder</title>
{{% endblock %}}

{{% block body %}}
    <div class="main-container">

        <header>
            <div class="header-container">
                <nav>
                    <div>
                        <ul class="nav-list">
                        <li><a id="home" href="{{{{ url_for('index', _external=True) }}}}" >Back to Index</a></li>
                        </ul>
                    </div>
                </nav>
                <div class="main-title">
                    <h1>{capitalized_label}</h1>
                </div>
            </div>
        </header>

        <section>
            <aside></aside>
            <article></article>
            <aside></aside>
        </section>

        <footer></footer>

    </div>
{{% endblock %}}"""


if __name__ == "__main__":
    print(write_html('pandas'))
