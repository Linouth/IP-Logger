from . import app, utils, forms
from .database import db_session
from .models import Picture, User
import bcrypt
from flask import (
        render_template, request, flash, redirect, url_for,
        send_from_directory, jsonify
)
from flask_login import login_user, logout_user, login_required, current_user
import json
import os


@app.route('/')
def index():
    return 'Hello.'


@app.route('/upload', methods=['GET', 'POST'])
@login_required
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

            pic = Picture(filename, extension, current_user.username)
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


@app.route('/register', methods=['GET', 'POST'])
def register():
    ''' Register user '''
    form = forms.RegisterForm()
    if request.method == 'GET':
        return render_template('register.html', form=form)

    if not form.validate_on_submit():
        es = []
        for errors in form.errors.values():
            for error in errors:
                es.append(error)
        flash(' - '.join(es))
        return redirect(url_for('register'))

    # Check if username or password already exist in database.
    ex = User.query.filter(User.username == form.username.data).first()
    if ex is not None:
        flash('Username already exists')
        return redirect(url_for('register'))
    ex = User.query.filter(User.email == form.email.data).first()
    if ex is not None:
        flash('Email already registered')
        return redirect(url_for('register'))

    # Hash password and save data in database.
    hashed = bcrypt.hashpw(form.password.data, bcrypt.gensalt())
    user = User(form.username.data, hashed,
                form.email.data, request.remote_addr)
    db_session.add(user)
    db_session.commit()
    flash('Welcome, you can continue now.')
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    ''' Login user '''
    form = forms.LoginForm()
    if request.method == 'GET':
        return render_template('login.html', form=form)
    username = form.username.data
    password = form.password.data
    user = User.query.filter(User.username == username).first()
    if user is None:
        flash('Invalid.')
        return redirect(url_for('login'))
    hashed = user.password
    if bcrypt.hashpw(password, hashed) != hashed:
        flash('Invalid.')
        return redirect(url_for('login'))
    login_user(user)
    return redirect(request.args.get('next') or url_for('upload'))


@app.route('/logout')
def logout():
    ''' Logout user '''
    logout_user()
    return redirect(url_for('index'))


@app.route('/uploads')
@login_required
def uploads():
    ''' Render page with all uploaded images '''
    uploads = Picture.query.filter(Picture.uploaded_by == current_user.username)
    return render_template('uploads.html', user=current_user, uploads=uploads)


@app.route('/uploads/<filename>')
@login_required
def upload_info(filename):
    ''' Show logged ip's and visits of uploaded image '''
    upload = Picture.query.filter(Picture.filename == filename).first()
    if upload.uploaded_by != current_user.username:
        return redirect(url_for('upload'))
    visitors = json.loads(upload.visitors)
    return render_template('picture_info.html', upload=upload, visitors=visitors)


''' Just some tests '''


@app.route('/ip')
def ip():
    ''' Some tests regarding the remote IP and proxy usage '''
    return jsonify({
        'remote_addr1': request.remote_addr,
        'remote_addr2': request.environ.get('REMOTE_ADDR'),
        'HTTP_X_FORWARDED_FOR': request.environ.get('HTTP_X_FORWARDED_FOR'),
        'X-Forwarded-For': request.environ.get('X-Forwarded-For'),
        'X-Client-IP': request.environ.get('X-Client-IP')
    })


@app.route('/info')
def info():
    return '''<h2>Info Page<h2>
              <ul>
                <li>{}</li>
                <li>{}</li>
              </ul>'''.format(current_user.username, url_for('uploads'))
