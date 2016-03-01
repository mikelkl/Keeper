# -*- coding: utf-8 -*-

from .forms import LoginForm
from . import auth
from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, logout_user, current_user, login_required
from .. import db, login_manager
from ..models import User
from datetime import datetime


@auth.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.add(current_user)
        db.session.commit()


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # # 若用户已登录，重定向到index
    # if g.user is not None and g.user.is_authenticated:
    #     flash('请勿重复登录！')
    #     # return redirect(url_for('index'))
    #
    # # 若用户未登录，重定向到index
    # if request.method == 'POST':
    #     user = User.query.filter_by(
    #         email=request.form.get('email'), password=request.form.get('password')).first()
    #
    #     if user is None:
    #         flash('用户名或密码错误！请重新输入！')
    #         return redirect(url_for('login'))
    #
    #     remember_me = False
    #     if request.form.get('remember_me'):
    #         # print request.form.get('remember_me')
    #         remember_me = True
    #     login_user(user, remember=remember_me)
    #     return redirect(url_for('patient'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(
            email=form.email.data, password=form.password.data).first()
        if user is not None:
            login_user(user, form.remember_me.data)
            return redirect(url_for('main.patient'))
    if request.method == 'POST':
        flash('用户名或密码错误！请重新输入！')
    return render_template('login.html', form=form)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
