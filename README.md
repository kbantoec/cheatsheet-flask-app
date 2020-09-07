# Welcome to the **Cheatsheet App** with Flask

In short, this full-stack project was the opportunity for me to use several technologies together such as Flask python-microframework along with ES6, and SQL.

The purpose of this web application is to order programming commands in dynamically generated web pages that could be saved in a database (here: SQLite).

![index](https://github.com/kbantoec/cheatsheet-flask-app/blob/master/csapp/static/img/index.png)

![cheatsheet](https://github.com/kbantoec/cheatsheet-flask-app/blob/master/csapp/static/img/cheatsheet.png)

## How to run this app

### On Windows command line

To run this app first clone repository and then open a terminal to the app folder.

```bash
>>> git clone https://github.com/kbantoec/cheatsheet-flask-app.git
>>> cd cheatsheet-flask-app
>>> virtualenv venv
>>> .\venv\Scripts\activate
>>> pip install -r requirements.txt
>>> python .\run.py
```

If you are using PowerShell, after having set up your virtual environment:

```powershell
>>> .\activate_environment.ps1
>>> flask run
```

## Specifications

I am using SQLite relational database.

I am not using the `SQLAlchemy` ORM (Object-Relational Mapping). Instead I use `sqlite3` to interact with the database.

I have set up several command line commands that can run in the flask shell during development.
