# -*- coding: utf-8 -*-

from app import app
from flask import render_template, request, redirect, url_for


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        message = None
        if request.form['email'] and request.form['password']:
            return redirect('/index')
        else:
            message = '登陆失败'
            return render_template('login.html', message=message)


@app.route('/map/<jd>/<wd>')
def map(jd=None, wd=None):
    return render_template('map.html', jd=jd, wd=wd)
