from .database import db_session
from .models import User
from flask import Flask
from flask_login import LoginManager
import os


app = Flask(__name__)
app.config.from_object(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.jinja_env.lstrip_blocks = True
app.jinja_env.trim_blocks = True

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'sqlite.db'),
    SECRET_KEY='8!93[0n6F-ti79sk(46%DrHFV',
    ALLOWED_EXTENSIONS=set(['jpg', 'png', 'gif', 'jpeg']),
    UPLOAD_DIR=os.path.join(app.root_path, 'uploads'),
    MAX_CONTENT_LENGTH=64*1024*1024
))


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.cli.command('initdb')
def initdb_command():
    from .database import init_db
    init_db()
    print('Initializing the database')


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


from . import views
