# -*- coding: utf-8 -*-

from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from .models import User
from datetime import datetime
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from werkzeug import secure_filename
import os


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # 若用户已登录，重定向到index
    if g.user is not None and g.user.is_authenticated:
        flash('请勿重复登录！')
        # return redirect(url_for('index'))

    # 若用户未登录，重定向到index
    if request.method == 'POST':
        user = User.query.filter_by(
            email=request.form.get('email'), password=request.form.get('password')).first()
        # print user
        if user is None:
            flash('用户名或密码错误！请重新输入！')
            return redirect(url_for('login'))

        remember_me = False
        if request.form.get('remember_me'):
            remember_me = True
        login_user(user, remember=remember_me)
        return redirect(url_for('doctor'))

    return render_template('login.html')


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/map/<jd>/<wd>')
@login_required
def map(jd=None, wd=None):
    return render_template('map.html', jd=jd, wd=wd)


@app.route('/record')
@login_required
def record():
    return render_template('record.html')


@app.route('/doctor')
@login_required
def doctor():
    if g.user == None:
        flash('User ' + g.nickname + ' not found.')
        return redirect(url_for('index'))
    return render_template('doctor.html',
                           user=g.user)


@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    if request.method == 'POST':
        if request.form.get('nickname'):
            g.user.nickname = request.form.get('nickname')
        if request.form.get('about_me'):
            g.user.about_me = request.form.get('about_me')
        avatar = request.files.get('avatar')
        if avatar and allowed_file(avatar.filename):
            avatar_name = unicode(g.user.id) + '.' + avatar.filename.rsplit('.', 1)[1]
            # avatar_url = os.path.join(UPLOAD_FOLDER, avatar_name)
            avatar.save( UPLOAD_FOLDER + '/' + avatar_name)
            g.user.avatar = avatar_name

        db.session.add(g.user)
        db.session.commit()
        flash('您的修改已保存！')
        return redirect(url_for('edit'))

    return render_template('edit.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# @app.route('/upload', methods=['GET', 'POST'])
# def upload():
#     if request.method == 'POST':
#         file = request.files.get('')
#         if file:
#             file.save( 'app/static/uploads/avatars/' + file.filename)
