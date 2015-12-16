# -*- coding: utf-8 -*-

from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from .models import User


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.before_request
def before_request():
    g.user = current_user


@app.route('/login', methods=['GET', 'POST'])
def login():
    # 若用户已登录，重定向到index
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))

    # 若用户未登录，重定向到index
    if request.method == 'POST':
        try:
            user = User.query.filter_by(email=request.form['email'], password=request.form['password']).first()
            print user
            if user is None:
                raise KeyError
            try:
                request.form['remember_me']
                remember_me = True
            except KeyError:
                remember_me = False
            finally:
                login_user(user, remember=remember_me)
                return redirect(url_for('index'))
        except KeyError:
            # flash 有bug
            flash('error!')
            return redirect(url_for('login'))

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
