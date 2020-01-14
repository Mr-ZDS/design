from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from note.extensions import db


class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    telephone = db.Column(db.String(11), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    icon = db.Column(db.String(20), default='user.png')

    def __init__(self, *args, **kwargs):
        telephone = kwargs.get('telephone')
        username = kwargs.get('username')
        password = kwargs.get('password')
        self.telephone = telephone
        self.username = username
        self.password = generate_password_hash(password)
        self.icon = 'user.png'

    def check_password(self, password):
        return check_password_hash(self.password, password)
