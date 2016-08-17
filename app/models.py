from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(120), index=True, unique=True)

    uploads = db.relationship("Upload", backref='person', lazy='dynamic')

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)    

    def __repr__(self):
        return '<User %r>' % (self.nickname)

class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(128), index=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship("User", back_populates="uploads")    

    def __repr__(self):
        return '<LogFile %r>' % (self.filename)