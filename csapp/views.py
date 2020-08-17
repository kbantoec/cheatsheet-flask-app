import time
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/server/time')
def get_current_time():
    return {'time': time.time()}


if __name__ == '__main__':
    pass
