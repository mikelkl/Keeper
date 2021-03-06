from datetime import datetime

from app import db
from flask import url_for
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Treatment(object):
    def __init__(self, doctor, administrative, professional, date, hospital, patient, treatmentReason):
        self.doctor = doctor
        self.administrative = administrative
        self.professional = professional
        self.date = date
        self.hospital = hospital
        self.patient = patient
        self.treatmentReason = treatmentReason

    def __repr__(self):
        return '<Treatment %r>' % (self.doctor)


class ECG(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(100), index=True)
    date = db.Column(db.String(20))
    time = db.Column(db.String(30))

    def __repr__(self):
        return '<ECG %r>' % (self.file_name)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True)
    sex = db.Column(db.String(5), index=True)
    age = db.Column(db.String(5))
    height = db.Column(db.String(8))
    weight = db.Column(db.String(8))
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    avatar = db.Column(db.String(40))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readble attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def generate_fake(count=100):
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            u = User(email=forgery_py.internet.email_address(),
                     nickname=forgery_py.internet.user_name(),
                     password=forgery_py.lorem_ipsum.word(),
                     about_me=forgery_py.lorem_ipsum.sentence(),
                     member_since=forgery_py.date.date(True),
                     sex=forgery_py.personal.gender(),
                     height='170',
                     weight='70',
                     age='20')
            db.session.add(u)
            try:
                db.session.commit()
            except:
                db.session.rollback()

    def to_json(self):
        json_user = {
            'url': url_for('api.get_user', id=self.id, _external=True),
            'nickname': self.nickname,
            'sex': self.sex,
            'age': self.age,
            'height': self.height,
            'weight': self.weight,
            'email': self.email,
            'about_me': self.about_me,
            'member_since': self.member_since,
            'last_seen': self.last_seen,
            'avatar': url_for('static', filename='uploads/avatars/%s' % self.avatar, _external=True)
        }
        return json_user

    def __repr__(self):
        return '<User %r>' % (self.nickname)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)
