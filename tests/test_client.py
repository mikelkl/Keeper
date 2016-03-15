# -*- coding: utf-8 -*-
import unittest

import re
from app import create_app, db
from app.models import User
from flask import url_for


class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_index(self):
        response = self.client.get(url_for('main.index'))
        self.assertTrue(re.search(b'Keeper', response.data))

    def login(self):
        # create a test account
        u = User()
        u.email = '123@qq.com'
        u.password = '888'
        db.session.add(u)
        db.session.commit()
        # login with a test account
        return self.client.post(url_for('auth.login'), data={
            'email': '123@qq.com',
            'password': '888'
        }, follow_redirects=True)

    def logout(self):
        return self.client.get(url_for('auth.logout'), follow_redirects=True)

    def test_login_and_logout(self):
        response = self.login()
        self.assertTrue(re.search(b'Test account', response.data))

        response = self.logout()
        print response.data
        self.assertTrue(re.search('Keeper', response.data))
