from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    login = db.Column(db.String(30), nullable = False, unique = True)
    password = db.Column(db.String(162), nullable = False)

class articles(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    login_id = db.Column(db.Integer, db.ForeignKey('users.id'))