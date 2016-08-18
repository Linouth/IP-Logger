from . import app, utils
from .database import db_session
from .models import Picture
# from . import forms
from flask import render_template, request, flash, redirect, url_for, send_from_directory, jsonify
from flask_login import login_user, logout_user, current_user, login_required
import json
import os


@app.route('/')
def index():
    return 'Hello.'


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    ''' Upload picture '''
    if request.method == 'POST':
        def no_file():
            flash('No file found')
            return redirect(request.url)

        def allowed_file(filename):
            extension = utils.get_extension(filename)
            return ('.' in filename) and\
                   (extension in app.config['ALLOWED_EXTENSIONS'])

        if 'file' not in request.files:
            return no_file()
        file = request.files['file']
        if file.filename == '':
            return no_file()

        if file and allowed_file(file.filename):
            filename = utils.gen_filename()
            extension = utils.get_extension(file.filename)
            savename = filename + '.' + extension

            pic = Picture(filename, extension)
            db_session.add(pic)
            db_session.commit()

            file.save(os.path.join(app.config['UPLOAD_DIR'], savename))
            return redirect(url_for('show', filename=filename))
    return render_template('upload.html')


@app.route('/img/<filename>')
def show(filename):
    ''' Render Show page '''
    pic = Picture.query.filter(Picture.filename == filename).first()
    if not pic:
        return 'File not found.'
    filetype = pic.filetype
    file = filename + '.' + filetype
    return render_template('show.html', filename=filename, file=file)


@app.route('/img/raw/<file>')
def show_raw(file):
    ''' Render raw image and save remote ip to database '''
    ip = request.environ.get('REMOTE_ADDR')
    # TODO: proxy = request.environ.get('HTTP_X_FORWARDED_FOR') (Proxy Support)

    filename = file.split('.', 1)[0]
    pic = Picture.query.filter(Picture.filename == filename).first()
    visitors = json.loads(pic.visitors)
    if ip not in visitors:
        visitors.append(ip)
        pic.visitors = json.dumps(visitors)
        db_session.commit()
    return send_from_directory(app.config['UPLOAD_DIR'], file)


''' User pages '''

"""
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.RegistrationForm(request.form)
    if request.method == 'GET':
        return render_template('register', form=form)
    if request.method == 'POST' and form.validate():
        forms.User(form.username.data, form.email.data,
                   form.password.data, request.environ['REMOTE_ADDR'])
        flash('User successfully registered')
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm(request.form)
    if request.method == 'GET':
        return render_template('login', form=form)
    username = form.username.data
    password = form.password.data

    user = forms.User(username, password)
    if not user.is_authenticated():
        flash('Username of Password is invalid', 'error')
        return redirect(url_for('login'))
    login_user(user)
    flash('Logged in successfully')
    return redirect(url_for('upload'))
"""


def ip():
    return jsonify({
        'remote_addr1': request.remote_addr,
        'remote_addr2': request.environ.get('REMOTE_ADDR'),
        'HTTP_X_FORWARDED_FOR': request.environ.get('HTTP_X_FORWARDED_FOR'),
        'X-Forwarded-For': request.environ.get('X-Forwarded-For'),
        'X-Client-IP': request.environ.get('X-Client-IP')
})
