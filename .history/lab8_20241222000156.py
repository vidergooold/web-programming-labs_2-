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

from flask import Blueprint, render_template, request, redirect
from werkzeug.security import generate_password_hash
from db.models import users
from db import db

lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')

    # Получение данных из формы
    login_form = request.form.get('login')
    password_form = request.form.get('password')

    # Проверки на пустые значения
    if not login_form or not password_form:
        return render_template('lab8/register.html', error='Логин и пароль не должны быть пустыми')

    # Проверка существования пользователя с таким логином
    login_exists = users.query.filter_by(login=login_form).first()
    if login_exists:
        return render_template('lab8/register.html', error='Такой пользователь уже существует')

    # Хеширование пароля и добавление нового пользователя
    password_hash = generate_password_hash(password_form)
    new_user = users(login=login_form, password=password_hash)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/lab8/')


@lab8.route('/articles')
def articles():
    return "Список статей (в разработке)"

@lab8.route('/create')
def create_article():
    return "Создать статью (в разработке)"
