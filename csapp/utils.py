if __name__ != "__main__":
    from csapp import models
import sqlite3


def dict_factory(cursor, row):
    return dict([(col[0], row[idx]) for idx, col in enumerate(cursor.description)])


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    con = None

    try:
        # Start connection with the database (also creates the file if it does not yet exist)
        con = sqlite3.connect(db_file)
        return con
    except sqlite3.Error as e:
        print(e)

    return con


def create_table(app, sql_table):
    """ create a table from the sql_table statement
    :param conn: Connection object
    :param sql_table: a CREATE TABLE statement
    :return:
    """
    con: sqlite3.Connection = create_connection(app.config['DATABASE_URI'])

    if con is not None:
        try:            
            c = con.cursor()
            c.execute(sql_table)
            con.commit()
            con.close()
        except sqlite3.Error as e:
            print(e)
    else:
        print("Error! Cannot create the database connection.")


def drop_table(app, table_name: str):
    s: str = str(input(f"This command is used to drop the {table_name!r} table in the database. " +
                       "Be careful before dropping a table. " +
                       "Deleting a table will result in loss of complete information stored in the table!" +
                       "\nAre you sure you want to go ahead? [y/n] "))
        
    if s.lower() == 'y':
        con: sqlite3.Connection = create_connection(app.config['DATABASE_URI'])
        sql_instruction: str = f"DROP TABLE IF EXISTS `{table_name}`;"
        con.execute(sql_instruction)
        con.commit()
        con.close()
        print(f"You have succesfully removed the {table_name!r} table.")
    else:
        print(f"You have not removed the {table_name!r} table.")


def create_index_items_table(app):

    table: str = """CREATE TABLE IF NOT EXISTS `index_items` (
                        item_id INTEGER PRIMARY KEY ASC, 
                        item_label TEXT NOT NULL UNIQUE                        
                    );"""
    
    create_table(app, table)


def create_commands_table(app):

    table: str = """CREATE TABLE IF NOT EXISTS `commands` (
                        command_id INTEGER PRIMARY KEY ASC,
                        command TEXT,
                        description TEXT,
                        syntax TEXT,
                        lang TEXT,
                        h1 TEXT,
                        item_id INTEGER NOT NULL,
                        FOREIGN KEY (item_id)
                            REFERENCES `index_items` (item_id)
                                ON UPDATE CASCADE
                                ON DELETE CASCADE
                    );"""
    
    create_table(app, table)


def create_examples_table(app):

    table: str = """CREATE TABLE IF NOT EXISTS `examples` (
                        example_id INTEGER PRIMARY KEY ASC,
                        example_caption TEXT,
                        example_content TEXT,
                        command_id INTEGER NOT NULL,
                        FOREIGN KEY (command_id)
                            REFERENCES commands (command_id)
                                ON UPDATE CASCADE
                                ON DELETE CASCADE
                    );"""
    
    create_table(app, table)


def create_links_table(app):

    table: str = """CREATE TABLE IF NOT EXISTS `links` (
                        link_id INTEGER PRIMARY KEY ASC,
                        link_label TEXT,
                        link_href TEXT,
                        link_type VARCHAR(5),
                        command_id INTEGER NOT NULL,
                        FOREIGN KEY (command_id)
                            REFERENCES commands (command_id)
                                ON UPDATE CASCADE
                                ON DELETE CASCADE
                    );"""
    
    create_table(app, table)


# def create_commands_examples_table(app):
#     # https://stackoverflow.com/questions/7296846/how-to-implement-one-to-one-one-to-many-and-many-to-many-relationships-while-de

#     table: str = """CREATE TABLE IF NOT EXISTS `commands_examples` (
#                         example_id INTEGER NOT NULL,
#                         command_id INTEGER NOT NULL,
#                         PRIMARY KEY (example_id, command_id),
#                         FOREIGN KEY (example_id)
#                             REFERENCES examples (example_id)
#                                 ON DELETE CASCADE 
#                                 ON UPDATE NO ACTION,
#                         FOREIGN KEY (command_id)
#                             REFERENCES commands (command_id)
#                                 ON DELETE CASCADE 
#                                 ON UPDATE NO ACTION
#                     );"""
    
#     create_table(app, table)


def drop_index_items_table(app):
    drop_table(app, 'index_items')   


def drop_commands_table(app):
    drop_table(app, 'commands')


def drop_examples_table(app):
    drop_table(app, 'examples')


def drop_links_table(app):
    drop_table(app, 'links')


def init_db(app):
    enable_fk(app)
    create_index_items_table(app)
    create_commands_table(app)
    create_examples_table(app)
    create_links_table(app)
    print("Database initialized!")


def reinit_db(app):
    reset_db(app)
    init_db(app)


def reset_db(app):
    db_uri: str = app.config['DATABASE_URI']

    with open(db_uri, mode="w"):
        # The "w" method will overwrite the entire file.
        print("Database reinitialized!")


def test_db(app):
    con = create_connection(app.config['DATABASE_URI'])
    
    try:
        fk_state: int = con.execute("""PRAGMA foreign_keys;""").fetchone()[0]
        print(f"Foreign key constraint state (1 = enabled, 0 = disabled): {fk_state}.")

        if fk_state == 1:
            print("Foreign key constraint already enabled.")
        else:
            con.execute("PRAGMA foreign_keys = ON;")
            con.commit()
            fk_state_expost: int = con.execute("""PRAGMA foreign_keys;""").fetchone()[0]
            print(f"Foreign key constraint enabled: {fk_state_expost}.")

        con.execute("INSERT INTO index_items (item_label) VALUES ('statsmodels'), ('scikit-learn'), ('pandas');")
        con.commit()
        print(con.execute("SELECT * FROM index_items;").fetchall())

        item_id: int = con.execute("SELECT item_id FROM index_items WHERE item_label = 'pandas';").fetchone()[0]
        con.execute("""INSERT INTO commands (command, description, syntax, lang, h1, item_id) 
                       VALUES ('test', 'test desc', 'test syn', 'py', 'test', 1), 
                              ('ma commande', 'ma description', 'ma syntaxe', 'py', 'test', 1),
                              ('<code>pandas.DataFrame</code>', 'Create a DataFrame', 'pandas.DataFrame()', 'py', 'pandas', ?);""",
                    (item_id, ))
        con.commit()
        print(con.execute("SELECT * FROM commands;").fetchall())
                
        con.execute("""INSERT INTO examples (example_caption, example_content, command_id)
                       VALUES ('Print hello world', 'print(''hello world'')', 3);""")
        con.commit()
        print(con.execute("SELECT * FROM examples;").fetchall())

        # con.execute("""INSERT INTO commands_examples (example_id, command_id) VALUES (1, 3)""")        
        # print(con.execute("SELECT * FROM commands_examples;").fetchall())

        # Modify informations to see if foreing key constraints update correctly
        con.execute("""UPDATE index_items
                       SET item_id = 100
                       WHERE item_label = 'pandas';""")
        con.commit()
        print(con.execute("SELECT * FROM index_items;").fetchall())
        print(con.execute("SELECT * FROM commands;").fetchall())

        con.execute("""UPDATE commands
                       SET command_id = 99
                       WHERE command = '<code>pandas.DataFrame</code>';""")
        con.commit()
        print(con.execute("SELECT * FROM commands;").fetchall())
        print(con.execute("SELECT * FROM examples;").fetchall())

        con.execute("""INSERT INTO links (link_label, link_href, link_type, command_id) 
                       VALUES ('Official documentation', 
                               'https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html',
                               'code',
                               99), 
                               ('Youtube', 
                               'avfrhbauhb',
                               'video',
                               99);""")
        con.commit()

        # con.execute("""UPDATE examples
        #                SET example_id = 99
        #                WHERE caption = 'Print hello world';""")  # FOREIGN KEY constraint failed
        # con.commit()
        
        # con.execute("""DELETE FROM examples WHERE example_id = 1;""")
        # con.commit()
        # print(con.execute("SELECT * FROM examples;").fetchall())
        # print(con.execute("SELECT * FROM commands_examples;").fetchall())
    except sqlite3.Error as e:
        print(e)
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


# def create_examples_table(app):
#     con: sqlite3.Connection = sqlite3.connect(app.config['DATABASE_URI'])
#     con.execute("""CREATE TABLE IF NOT EXISTS `examples` (example_id INTEGER PRIMARY KEY ASC,
#                                                           caption TEXT,
#                                                           content TEXT);""")
#     con.commit()
#     con.close()


# def create_commands_examples_table(app):
#     """Composition table between Commands and Examples tables.
    
#     Official information:
#     - https://www.sqlitetutorial.net/sqlite-create-table/
#     - To learn about SQLite foreign key constraint actions: https://www.sqlitetutorial.net/sqlite-foreign-key/
#     """
    
#     con: sqlite3.Connection = sqlite3.connect(app.config['DATABASE_URI'])
#     con.execute("""CREATE TABLE IF NOT EXISTS `commands_examples` (
#         command_id INTEGER,
#         example_id INTEGER,
#         PRIMARY KEY (command_id, example_id),
#         FOREIGN KEY (command_id)
#             REFERENCES `commands` (command_id)
#                 ON DELETE CASCADE
#                 ON UPDATE NO ACTION,
#         FOREIGN KEY (example_id)
#             REFERENCES `examples` (example_id)
#                 ON DELETE CASCADE
#                 ON UPDATE NO ACTION
#     );""")
#     con.commit()
#     con.close()


# def create_commands_links_table(app):
#     """Composition table between Command and Link tables."""
#     con: sqlite3.Connection = sqlite3.connect(app.config['DATABASE_URI'])
#     con.execute("""CREATE TABLE IF NOT EXISTS `commands_links` (
#         command_id INTEGER,
#         link_id INTEGER,
#         PRIMARY KEY (command_id, link_id),
#         FOREIGN KEY (command_id)
#             REFERENCES `commands` (command_id)
#                 ON DELETE CASCADE
#                 ON UPDATE NO ACTION,
#         FOREIGN KEY (link_id)
#             REFERENCES `links` (link_id)
#                 ON DELETE CASCADE
#                 ON UPDATE NO ACTION
#     );""")
#     con.commit()
#     con.close()


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


def enable_fk(app):
    """Enable foreign key constraint."""
    con: sqlite3.Connection = sqlite3.connect(app.config['DATABASE_URI'])
    fk_state: int = con.execute("""PRAGMA foreign_keys;""").fetchone()[0]
    print(f"Foreign key constraint state: {fk_state}.")

    if fk_state == 1:
        print("Foreign key constraint already enabled.")
    else:
        con.execute("PRAGMA foreign_keys = ON;")
        con.commit()
        fk_state_expost: int = con.execute("""PRAGMA foreign_keys;""").fetchone()[0]
        print(f"Foreign key constraint enabled: {fk_state_expost}.")
    
    con.close()


def disable_fk(app):
    """Disable foreign key constraint."""
    con: sqlite3.Connection = sqlite3.connect(app.config['DATABASE_URI'])
    fk_state: int = con.execute("""PRAGMA foreign_keys;""").fetchone()[0]
    print(f"Foreign key constraint state: {fk_state}.")

    if fk_state == 1:        
        con.execute("PRAGMA foreign_keys = OFF;")
        con.commit()
        fk_state_expost: int = con.execute("""PRAGMA foreign_keys;""").fetchone()[0]
        print(f"Foreign key constraint disabled: {fk_state_expost}.")
    else:        
        print("Foreign key constraint already disabled.")
    
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
