import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True

# upload configuration
UPLOADED_FILES_DEST = basedir+'/tmp/' 
UPLOADED_FILES_ALLOW = set(['txt','log'])

# wtf cofiguration
WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

# user
SECRET_KEY = '12345'
USERNAME = 'admin'
PASSWORD = 'default'
