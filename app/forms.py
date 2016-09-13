from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, BooleanField, PasswordField, validators
from wtforms.validators import DataRequired, Length
from app import logUpload
from app.models import User, Upload
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename


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
        user = self.get_user()
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

class UploadForm(Form):
    upload = FileField('filename', validators=[FileRequired(), FileAllowed(logUpload, 'Only Log Files!')])
    # upload = FileField()

    # def __init__(self, *args, **kwargs):
    #     Form.__init__(self, *args, **kwargs)
    #     self.filename = None

    # def validate(self):
    #     rv = Form.validate(self)
    #     if not rv:
    #         self.upload.errors.append('Something goes wrong!!!')
    #         return False
        
    #     filename = secure_filename(self.upload.data.filename)
    #     if filename is None:
    #         self.upload.errors.append('Something goes wrong!!!')

    #     self.filename = filename

    #     return True
    
            