# Welcome to the **Cheatsheet App** with Flask

In short, this full-stack project was the opportunity for me to use several technologies together such as Flask python-microframework along with ES6, and SQL.

The purpose of this web application is to order programming commands in dynamically generated web pages that could be saved in a database (here: SQLite).

![index](https://github.com/kbantoec/cheatsheet-flask-app/blob/master/csapp/static/img/index.png)

![cheatsheet](https://github.com/kbantoec/cheatsheet-flask-app/blob/master/csapp/static/img/cheatsheet.png)

## Workflow

Using PowerShell:

```powershell
>>> .\activate_environment.ps1
>>> flask run
```

## Specifications

I am using SQLite relational database.

I am not using the `SQLAlchemy` ORM (Object-Relational Mapping). Instead I use `sqlite3` to interact with the database.

I set up several command line commands that can run in the flask shell during development.
