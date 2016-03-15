# -*- coding: utf-8 -*-
import re
import threading
import time
import unittest
from selenium import webdriver
from app import create_app, db
from app.models import User


class SeleniumTestCase(unittest.TestCase):
    client = None

    @classmethod
    def setUpClass(cls):
        # start Firefox
        try:
            cls.client = webdriver.Firefox()
        except:
            pass

        # skip these tests if the browser could not be started
        if cls.client:
            # create the application
            cls.app = create_app('testing')
            cls.app_context = cls.app.app_context()
            cls.app_context.push()

            # suppress logging to keep unittest output clean
            import logging
            logger = logging.getLogger('werkzeug')
            logger.setLevel("ERROR")

            # create the database and populate with some fake data
            db.create_all()
            # create a test account
            u = User()
            u.email = '123@qq.com'
            u.password = '888'
            db.session.add(u)
            db.session.commit()

            # start the Flask server in a thread
            threading.Thread(target=cls.app.run).start()

            # give the server a second to ensure it is up
            time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        if cls.client:
            # stop the flask server and the browser
            cls.client.get('http://localhost:5000/shutdown')
            cls.client.close()

            # destroy database
            db.drop_all()
            db.session.remove()

            # remove application context
            cls.app_context.pop()

    def setUp(self):
        if not self.client:
            self.skipTest('Web browser not available')

    def tearDown(self):
        pass

    def test_home_page(self):
        # navigate to home page
        self.client.get('http://localhost:5000/')
        self.assertTrue(re.search('index',
                                  self.client.page_source))

        # navigate to login page
        self.client.find_element_by_link_text('登陆').click()
        self.assertTrue('记住我'.decode('utf-8') in self.client.page_source)

        # login
        self.client.find_element_by_name('email'). \
            send_keys('123@qq.com')
        self.client.find_element_by_name('password').send_keys('888')
        self.client.find_element_by_name('submit').click()
        self.assertTrue(re.search('关注ta'.decode('utf-8'), self.client.page_source))

        # navigate to the about page
        self.client.find_element_by_link_text('关于我们').click()
        self.assertTrue('运营计划'.decode('utf-8') in self.client.page_source)
