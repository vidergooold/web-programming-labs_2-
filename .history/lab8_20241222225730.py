from flask import Blueprint, render_template, request, redirect, session
from flask_login import login_user, login_required, logout_user, current_user
from db import Lab8Users, Lab8Articles, db
from werkzeug.security import generate_password_hash, check_password_hash

lab8 = Blueprint('lab8', __name__)

@lab8.route('/')
def lab():
    return render_template('lab8/lab8.html')

# Регистрация
@lab8.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login_form = request.form.get('login')
        password_form = request.form.get('password')

        if not login_form or not password_form:
            return render_template('lab8/register.html', error="Поля не должны быть пустыми")

        if Lab8Users.query.filter_by(login=login_form).first():
            return render_template('lab8/register.html', error="Такой пользователь уже существует")

        hashed_password = generate_password_hash(password_form)
        new_user = Lab8Users(login=login_form, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        # Перезагрузка объекта из базы данных
        user = Lab8Users.query.filter_by(login=login_form).first()
        login_user(user)

        return redirect('/lab8/')

    return render_template('lab8/register.html')


# Вход
@lab8.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_form = request.form.get('login')
        password_form = request.form.get('password')

        user = Lab8Users.query.filter_by(login=login_form).first()

        if user and check_password_hash(user.password, password_form):
            login_user(user, remember=request.form.get('remember') == 'on')
            return redirect('/lab8/')
        return render_template('lab8/login.html', error="Неверные логин или пароль")

    return render_template('lab8/login.html')

# Выход
@lab8.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')

# Статьи текущего пользователя
@lab8.route('/articles')
@login_required
def articles():
    user_articles = Lab8Articles.query.filter_by(login_id=current_user.id).all()
    return render_template('lab8/articles.html', articles=user_articles)

# Создание статьи
@lab8.route('/create', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'POST':
        title = request.form.get('title')
        article_text = request.form.get('article_text')
        new_article = Lab8Articles(login_id=current_user.id, title=title, article_text=article_text)
        db.session.add(new_article)
        db.session.commit()
        return redirect('/lab8/articles')

    return render_template('lab8/create.html')

# Редактирование статьи
@lab8.route('/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = Lab8Articles.query.get(article_id)
    if not article or article.login_id != current_user.id:
        return redirect('/lab8/articles')

    if request.method == 'POST':
        article.title = request.form.get('title')
        article.article_text = request.form.get('article_text')
        db.session.commit()
        return redirect('/lab8/articles')

    return render_template('lab8/edit.html', article=article)

# Удаление статьи
@lab8.route('/delete/<int:article_id>', methods=['POST'])
@login_required
def delete_article(article_id):
    article = Lab8Articles.query.get(article_id)
    if article and article.login_id == current_user.id:
        db.session.delete(article)
        db.session.commit()
    return redirect('/lab8/articles')

# Публичные статьи
@lab8.route('/public-articles')
def public_articles():
    articles = Lab8Articles.query.filter_by(is_public=True).all()
    return render_template('lab8/public_articles.html', articles=articles)
