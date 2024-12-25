from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Lab8Users(db.Model, UserMixin):
    __tablename__ = 'lab8_users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(162), nullable=False)

    def get_id(self):
        return str(self.id)


class Lab8Articles(db.Model):
    __tablename__ = 'lab8_articles'
    id = db.Column(db.Integer, primary_key=True)
    login_id = db.Column(db.Integer, db.ForeignKey('lab8_users.id'))
    title = db.Column(db.String(50), nullable=False)
    article_text = db.Column(db.Text, nullable=False)
    is_favorite = db.Column(db.Boolean, default=False)
    is_public = db.Column(db.Boolean, default=False)
