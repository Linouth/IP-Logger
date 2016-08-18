from flask import Flask, g
from flask_login import LoginManager
import os
import sqlite3


app = Flask(__name__)
app.config.from_object(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'sqlite.db'),
    SECRET_KEY='8!93[0n6F-ti79sk(46%DrHFV',
    ALLOWED_EXTENSIONS=set(['jpg', 'png', 'gif', 'jpeg']),
    UPLOAD_DIR=os.path.join(app.root_path, 'uploads')
))


def connect_db():
    ' Create and return database connection '
    db = sqlite3.connect(app.config['DATABASE'])
    db.row_factory = sqlite3.Row
    return db


def get_db():
    ' Return (and create) database connection '
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    ' Close database connection '
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def init_db():
    ' Initialize database connection '
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    init_db()
    print('Initializing the database')


from . import views
