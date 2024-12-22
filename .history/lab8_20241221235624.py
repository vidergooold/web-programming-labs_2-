from flask import Blueprint, render_template
from db import db
from db.models import users, articles

lab8 = Blueprint('lab8', __name__)

@lab8.route('/')
def lab8_main():
    user = "anonymous"  # Пока пользователь анонимный
    return render_template('lab8/lab8.html', user=user)

@lab8.route('/login')
def login():
    return "Страница входа (в разработке)"

@lab8.route('/register')
def register():
    return "Страница регистрации (в разработке)"

@lab8.route('/articles')
def articles():
    return "Список статей (в разработке)"

@lab8.route('/create')
def create_article():
    return "Создать статью (в разработке)"
