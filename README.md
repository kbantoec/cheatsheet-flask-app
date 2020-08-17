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

```
$env:FLASK_APP = "csapp/server.py"
$env:FLASK_ENV = "development"
```

