from app import db


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
    date = db.Column(db.String(20), index=True)
    time = db.Column(db.String(30), index=True)
    def __repr__(self):
        return '<ECG %r>' % (self.file_name)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True)
    sex = db.Column(db.String(5), index=True)
    age = db.Column(db.String(5), index=True)
    height = db.Column(db.String(8), index=True)
    weight = db.Column(db.String(8), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(20), index=True, unique=False)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)
    avatar = db.Column(db.String(40))

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

    def __repr__(self):
        return '<User %r>' % (self.nickname)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)
