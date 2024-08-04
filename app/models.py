from flask_sqlalchemy import SQLAlchemy
from cryptography.fernet import Fernet

db = SQLAlchemy()
key = Fernet.generate_key()
cipher_suite = Fernet(key)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    hashed_password = db.Column(db.String(255), nullable=False)

    def __init__(self, username, hashed_password):
        self.username = username
        self.hashed_password = hashed_password


class PasswordEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    website = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    encrypted_password = db.Column(db.String(255), nullable=False)

    def __init__(self, user_id, website, username, encrypted_password):
        self.user_id = user_id
        self.website = website
        self.username = username
        self.encrypted_password = encrypted_password
