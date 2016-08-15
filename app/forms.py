from flask_wtf import Form
from wtforms import StringField, BooleanField, PasswordField, validators
from wtforms.validators import DataRequired, Length
from app.models import User
from werkzeug.security import check_password_hash


class LoginForm(Form):
    username = StringField('username', validators=[validators.required()])
    password = PasswordField('password', validators=[validators.required()])
    remember_me = BooleanField('remember_me', default=False)

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None
        
    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False    
        user = User.query.filter_by(nickname=self.username.data).first()
        if user is None:
            self.username.errors.append('Unknown username')
            return False

        if not check_password_hash(user.password, self.password.data):
            self.password.errors.append('Invalid password')
            return False

        self.user = user
        return True

    def get_user(self):
        return User.query.filter_by(nickname=self.username.data).first()