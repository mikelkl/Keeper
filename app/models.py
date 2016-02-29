from app import db
from datetime import datetime


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


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True)
    sex = db.Column(db.String(5), index=True)
    age = db.Column(db.String(5))
    height = db.Column(db.String(8))
    weight = db.Column(db.String(8))
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(20), index=True)
    about_me = db.Column(db.String(140))
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    avatar = db.Column(db.String(40))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

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
                     member_since=forgery_py.date.date(True))
            db.session.add(u)
            try:
                db.session.commit()
            except:
                db.session.rollback()

    def __repr__(self):
        return '<User %r>' % (self.nickname)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)
