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

Other flask CLI commands: 

```powershell
> flask run
> flask --help
> flask routes
```



## Documentation

* `sqlite3`:
  * [Official documentation](https://docs.python.org/3/library/sqlite3.html)
  * [SQLite Tutorial documentation](https://www.sqlitetutorial.net/sqlite-python/)