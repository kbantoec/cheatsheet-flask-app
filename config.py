import os

basedir = os.path.abspath(os.path.dirname(__file__))
DATABASE_URI = f"{os.path.normpath(os.path.join(basedir, 'app.db'))}"
ENV = "development"
DEBUG = True