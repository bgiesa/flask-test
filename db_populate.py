#!venv/bin/python
from app import db, models
from werkzeug.security import generate_password_hash

u = models.User(nickname='admin', email='admin@example.com', password=generate_password_hash('default'))

db.session.add(u)
db.session.commit()