if __name__ != "__main__":
    from csapp import models
import sqlite3


def dict_factory(cursor, row):
    return dict([(col[0], row[idx]) for idx, col in enumerate(cursor.description)])


def create_indexitem_table(app):
    # Start connection with the database (also creates the file if it does not yet exist)
    con: sqlite3.Connection = sqlite3.connect(app.config['DATABASE_URI'])

    # Using the nonstandard `execute()` method of the `Connection` object, we don't have to create the `Cursor` objects explicitly
    con.execute("""CREATE TABLE IF NOT EXISTS `indexitem` (
        id INTEGER PRIMARY KEY ASC, 
        label TEXT NOT NULL UNIQUE,
        command_id INTEGER NOT NULL,
        FOREIGN KEY (command_id)
            REFERENCES `commands` (command_id)
        );""")
    
    con.commit()
    con.close()


def enable_fk(app):
    """Enable foreign key constraint."""
    con: sqlite3.Connection = sqlite3.connect(app.config['DATABASE_URI'])
    fk_enabled: bool = bool(con.execute("""PRAGMA foreign_keys;""").fetchone()[0])

    if fk_enabled:
        print("Foreign key constraint already enabled.")
    else:
        con.execute("PRAGMA foreign_keys = ON;")
        con.commit()
        print("Foreign key constraint enabled.")
    
    con.close()


def disable_fk(app):
    """Disable foreign key constraint."""
    con: sqlite3.Connection = sqlite3.connect(app.config['DATABASE_URI'])
    fk_enabled: bool = bool(con.execute("""PRAGMA foreign_keys;""").fetchone()[0])

    if fk_enabled:        
        con.execute("PRAGMA foreign_keys = OFF;")
        con.commit()
        print("Foreign key constraint disabled.")
    else:        
        print("Foreign key constraint already disabled.")
    
    con.close()


def create_reminder_table(app):
    con: sqlite3.Connection = sqlite3.connect(app.config['DATABASE_URI'])
    con.execute("""CREATE TABLE IF NOT EXISTS `reminder`  (id INTEGER PRIMARY KEY ASC, 
                                                           label VARCHAR(100),
                                                           h1 TEXT,
                                                           content_cell_1 TEXT,
                                                           content_cell_2 TEXT,
                                                           lang VARCHAR(10),
                                                           syntax_content TEXT,
                                                           example_content TEXT,
                                                           example_caption TEXT,
                                                           link_text TEXT,
                                                           link_href TEXT,
                                                           link_type VARCHAR(5));""")
    con.commit()
    con.close()


def create_commands_table(app):
    con: sqlite3.Connection = sqlite3.connect(app.config['DATABASE_URI'])
    con.execute("""CREATE TABLE IF NOT EXISTS `commands` (command_id INTEGER PRIMARY KEY ASC,
                                                          command TEXT,
                                                          description TEXT,
                                                          syntay TEXT);""")
    con.commit()
    con.close()


def create_examples_table(app):
    con: sqlite3.Connection = sqlite3.connect(app.config['DATABASE_URI'])
    con.execute("""CREATE TABLE IF NOT EXISTS `examples` (example_id INTEGER PRIMARY KEY ASC,
                                                          caption TEXT,
                                                          content TEXT);""")
    con.commit()
    con.close()


def create_links_table(app):
    con: sqlite3.Connection = sqlite3.connect(app.config['DATABASE_URI'])
    con.execute("""CREATE TABLE IF NOT EXISTS `links` (link_id INTEGER PRIMARY KEY ASC,
                                                       text TEXT,
                                                       href TEXT,
                                                       type VARCHAR(5));""")
    con.commit()
    con.close()


def create_commands_examples_table(app):
    """Composition table between Commands and Examples tables.
    
    Official information:
    - https://www.sqlitetutorial.net/sqlite-create-table/
    - To learn about SQLite foreign key constraint actions: https://www.sqlitetutorial.net/sqlite-foreign-key/
    """
    
    con: sqlite3.Connection = sqlite3.connect(app.config['DATABASE_URI'])
    con.execute("""CREATE TABLE IF NOT EXISTS `commands_examples` (
        command_id INTEGER,
        example_id INTEGER,
        PRIMARY KEY (command_id, example_id),
        FOREIGN KEY (command_id)
            REFERENCES `commands` (command_id)
                ON DELETE CASCADE
                ON UPDATE NO ACTION,
        FOREIGN KEY (example_id)
            REFERENCES `examples` (example_id)
                ON DELETE CASCADE
                ON UPDATE NO ACTION
    );""")
    con.commit()
    con.close()


def create_commands_links_table(app):
    """Composition table between Command and Link tables."""
    con: sqlite3.Connection = sqlite3.connect(app.config['DATABASE_URI'])
    con.execute("""CREATE TABLE IF NOT EXISTS `commands_links` (
        command_id INTEGER,
        link_id INTEGER,
        PRIMARY KEY (command_id, link_id),
        FOREIGN KEY (command_id)
            REFERENCES `commands` (command_id)
                ON DELETE CASCADE
                ON UPDATE NO ACTION,
        FOREIGN KEY (link_id)
            REFERENCES `links` (link_id)
                ON DELETE CASCADE
                ON UPDATE NO ACTION
    );""")
    con.commit()
    con.close()


def drop_reminder_table(app):    
    s: str = str(input("""This command is used to drop the 'reminder' table in the database. Be careful before dropping a table. Deleting a table will result in loss of complete information stored in the table!\nAre you sure you want to go ahead? [y/n] """))
    if s.lower() == 'y':
        con: sqlite3.Connection = sqlite3.connect(app.config['DATABASE_URI'])
        con.execute("""DROP TABLE IF EXISTS `reminder`;""")
        con.commit()
        con.close()
        print("You have succesfully removed the 'reminder' table.")
    else:
        print("You have not removed the 'reminder' table.")


def drop_reminder_table_data(app):
    s: str = str(input("""The TRUNCATE TABLE statement is used to delete the data inside the 'reminder' table, but not the table itself.\nAre you sure you want to go ahead? [y/n] """))
    if s.lower() == 'y':
        con: sqlite3.Connection = sqlite3.connect(app.config['DATABASE_URI'])
        con.execute("""TRUNCATE TABLE IF EXISTS `reminder`;""")
        con.commit()
        con.close()
        print("You have succesfully removed the data inside the 'reminder' table.")
    else:
        print("You have not removed the data inside the 'reminder' table.")

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
