# Python *cheat-sheet* app with Flask

1. What is the project structure?
   1. How to connect front-end with back-end?
   2. How to interact with the database?

```powershell
> virtualenv -p C:\Users\YBant\AppData\Local\Programs\Python\Python37\python.exe venv
> .\venv\Scripts\activate.ps1
> (venv) pip list
> (venv) pip install flask
> (venv) pip install python-dotenv
```

* `.flaskenv` is where we set up our environment variables for the Flask backend (works only if `python-dotenv` installed)
* A Flask based API backend was added in the `server` directory.

## Table modification workflow

1. Modify the structure in `models.py`
2. Modify the CLI command to create the table in `utils.py`
3. `reminder.html`template.
   1. Modify the form
   2. Modify the data-* attributes
4. Modify the requests in `views.py`
5. Add relevant functionalities in corresponding javascript file

## Creation of the database

Using the CLI:

1. `flask reinit-db`
2. `flask init-db`
3. `flask test-db`

## Flask CLI commands

I have added a CLI command in  the `__init__.py` file:

```python
@app.cli.command()
def create_indexitem_table():
    """Create IndexItem Table."""
    utils.create_indexitem_table()
```

Running on the terminal at the root of the project we can observe the `create-indexitem-table` command:

```powershell
> flask --help
...
Commands:
  create-indexitem-table  Create IndexItem Table.
  routes                  Show the routes for the app.
  run                     Run a development server.
  shell                   Run a shell in the app context.
```

```powershell
> flask create-indexitem-table
```



Run them on the PowerShell terminal at the root of the project:

```powershell
> $env:FLASK_APP = "run.py"
> $env:FLASK_ENV = "development"
> flask create-indexitem-table
> flask shell
>>> from csapp import app
>>> import sqlite3
>>> app.config
>>> con = sqlite3.connect(app.config['DATABASE_URI'])
>>> con.execute("SELECT * FROM indexitem").fetchall()
[]
>>> con.execute("INSERT INTO indexitem VALUES (NULL, 'Hello World');")
<sqlite3.Cursor object at 0x0000013B3363AB90>
>>> con.execute("SELECT * FROM indexitem").fetchall()                  
[(1, 'Hello World')]
>>> con.execute("DELETE FROM indexitem WHERE id = 1;")
<sqlite3.Cursor object at 0x0000013B3363AB90>
>>> con.commit()
>>> con.execute("SELECT * FROM indexitem").fetchall()
[]
>>> con.close()
>>> exit()
```

```python
>>> from csapp import app
>>> import sqlite3
>>> con = sqlite3.connect(app.config['DATABASE_URI'])
>>> con.execute("SELECT * FROM indexitem").fetchall()
[(1, 'Pandas'), (2, 'Numpy'), (3, 'Statsmodels')]
>>> con.execute("DELETE FROM indexitem WHERE id = 2 OR id = 3;")
<sqlite3.Cursor object at 0x000001C45B4DAB90>
>>> con.commit()
>>> con.execute("SELECT * FROM indexitem").fetchall()
[(1, 'Pandas')]
```

```python
from csapp import app
import sqlite3
con = sqlite3.connect(app.config['DATABASE_URI'])
con.execute("SELECT * FROM index_items;").fetchall()
con.execute("SELECT * FROM indexitem").fetchall()
con.execute("DELETE FROM `indexitem` WHERE id = 4;")
con.commit()
con.execute("SELECT * FROM indexitem").fetchall()


con.execute("SELECT name FROM sqlite_master;").fetchall()
con.execute("SELECT 'DROP TABLE ' || name || ';' from sqlite_master WHERE type = 'table';")
```



Other flask CLI commands: 

```powershell
> flask run
> flask --help
> flask routes
```

```powershell
> $env:FLASK_APP = "run.py"
> $env:FLASK_ENV = "development"
> flask create-reminder-table
> flask shell
>>> from csapp import app
>>> import sqlite3
>>> app.config
>>> con = sqlite3.connect(app.config['DATABASE_URI'])
>>> con.execute("SELECT * FROM `reminder`").fetchall()
[]
>>> con.execute("INSERT INTO `reminder` VALUES (NULL, 'pandas', 'pandas.Series', 'pandas.Series.value_counts', 'Return a Series containing counts of unique values.');")
<sqlite3.Cursor object at 0x0000028FCAC90180>
>>> con.commit()
>>> con.execute("SELECT * FROM `reminder`").fetchall()    
[(1, 'pandas', 'pandas.Series', 'pandas.Series.value_counts', 'Return a Series containing counts of unique values.')]
>>> con.execute("DELETE FROM `reminder` WHERE id = 1;")
<sqlite3.Cursor object at 0x0000028FCAC90180>
>>> con.commit()
>>> con.execute("SELECT * FROM `reminder`").fetchall()
[]
>>> con.close()
>>> exit()
>>> con.execute("INSERT INTO `reminder` VALUES (NULL, 'pandas', '<code>pandas.DataFrame</code>', '<code>pandas.DataFrame.apply</code>', 'Apply a function along an axis of the DataFrame.');")
```



## Documentation

* `sqlite3`:
  * [Official documentation](https://docs.python.org/3/library/sqlite3.html)
  
  * [SQLite Tutorial documentation](https://www.sqlitetutorial.net/sqlite-python/)
  
  * How to create foreign keys?
  
    * [Python MySQL Tutorial - Foreign Keys & Relating Tables](https://www.youtube.com/watch?v=f7oYCzKuv-w)
  
      ```sqlite
      CREATE TABLE Users (id int PRIMARY KEY AUTO_INCREMENT, name VARCHAR(50), passwd VARCHAR(50));
      CREATE TABLE Scores (userId int PRIMARY KEY, FOREIGN KEY(userId) REFERENCES Users(id), game1 int DEFAULT 0, game2 int DEFAULT 0);
      ```
  
      