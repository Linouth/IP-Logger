from .database import db_session
from flask import Flask
from flask_login import LoginManager
import os


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


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.cli.command('initdb')
def initdb_command():
    from .database import init_db
    init_db()
    print('Initializing the database')


from . import views
