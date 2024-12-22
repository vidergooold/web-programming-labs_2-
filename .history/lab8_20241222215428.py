from flask import Blueprint, render_template, request, redirect, session
from flask_login import login_user, login_required, logout_user, current_user
from db import users, articles
from werkzeug.security import generate_password_hash, check_password_hash
from db import db

lab8 = Blueprint('lab8', __name__)

@lab8.route('/')
def lab():
    return render_template('lab8/lab8.html')


@lab8.route('/lab8/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    if not login_form or not password_form:
        return render_template('lab8/register.html', error="Поля не должны быть пустыми")
    if users.query.filter_by(login=login_form).first():
        return render_template('lab8/register.html', error="Такой пользователь уже существует")
    hashed_password = generate_password_hash(password_form)
    new_user = users(login=login_form, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user)
    return redirect('/lab8/lab8/')

@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    user = users.query.filter_by(login=login_form).first()
    if user and check_password_hash(user.password, password_form):
        login_user(user, remember=request.form.get('remember') == 'on')
        return redirect('/lab8/lab8/')
    return render_template('lab8/login.html', error="Неверные логин или пароль")

@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/lab8/')

@lab8.route('/lab8/articles')
@login_required
def articles():
    user_articles = articles.query.filter_by(login_id=current_user.id).all()
    return render_template('lab8/articles.html', articles=user_articles)

@lab8.route('/lab8/create', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'GET':
        return render_template('lab8/create.html')
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    new_article = articles(login_id=current_user.id, title=title, article_text=article_text)
    db.session.add(new_article)
    db.session.commit()
    return redirect('/lab8/lab8/articles')

@lab8.route('/lab8/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = articles.query.get(article_id)
    if not article or article.login_id != current_user.id:
        return redirect('/lab8/lab8/articles')
    if request.method == 'GET':
        return render_template('lab8/edit.html', article=article)
    article.title = request.form.get('title')
    article.article_text = request.form.get('article_text')
    db.session.commit()
    return redirect('/lab8/lab8/articles')

@lab8.route('/lab8/delete/<int:article_id>', methods=['POST'])
@login_required
def delete_article(article_id):
    article = articles.query.get(article_id)
    if article and article.login_id == current_user.id:
        db.session.delete(article)
        db.session.commit()
    return redirect('/lab8/lab8/articles')

@lab8.route('/lab8/public-articles')
def public_articles():
    # Получаем все статьи с флагом is_public=True
    articles = articles.query.filter_by(is_public=True).all()
    return render_template('lab8/public_articles.html', articles=articles)

@lab8.route('/lab8/search', methods=['GET', 'POST'])
def search_articles():
    if request.method == 'GET':
        return render_template('lab8/search.html')
    search_query = request.form.get('query')
    if not search_query:
        return render_template('lab8/search.html', error="Введите строку для поиска.")
    
    # Поиск в публичных статьях и статьях текущего пользователя
    if current_user.is_authenticated:
        articles = articles.query.filter(
            (articles.is_public == True) | (articles.login_id == current_user.id),
            articles.title.ilike(f'%{search_query}%')
        ).all()
    else:
        articles = articles.query.filter(
            articles.is_public == True,
            articles.title.ilike(f'%{search_query}%')
        ).all()
    
    return render_template('lab8/search_results.html', articles=articles, query=search_query)
