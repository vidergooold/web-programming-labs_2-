from flask import Blueprint, render_template, request, session, redirect, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path

# Создаем Blueprint
lab5 = Blueprint('lab5', __name__)

# Главная страница базы знаний
@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html', login=session.get('login'))

# Подключение к базе данных
def db_connect():
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            conn = psycopg2.connect(
                host='127.0.0.1',
                database='kb',
                user='irina_vidergold_knowledge_base',
                password='123'
            )
            cur = conn.cursor(cursor_factory=RealDictCursor)
        else:
            dir_path = path.dirname(path.realpath(__file__))
            db_path = path.join(dir_path, "database.db")
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
        return conn, cur
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")
        return None, None

# Закрытие соединения с базой данных
def db_close(conn, cur):
    if conn:
        conn.commit()
        cur.close()
        conn.close()

# Регистрация нового пользователя
@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')

    # Получаем данные из формы
    login = request.form.get('login')
    password = request.form.get('password')

    # Проверка на пустые поля
    if not login or not password:
        return render_template('lab5/register.html', error="Заполните все поля")

    conn, cur = db_connect()
    if not conn:
        return render_template('lab5/register.html', error="Ошибка подключения к базе данных")

    try:
        # Проверка существования пользователя
        query = "SELECT login FROM users WHERE login=%s;" if current_app.config['DB_TYPE'] == 'postgres' else "SELECT login FROM users WHERE login=?;"
        cur.execute(query, (login,))
        if cur.fetchone():
            db_close(conn, cur)
            return render_template('lab5/register.html', error="Такой пользователь уже существует")

        # Добавление нового пользователя
        password_hash = generate_password_hash(password)
        insert_query = "INSERT INTO users (login, password) VALUES (%s, %s);" if current_app.config['DB_TYPE'] == 'postgres' else "INSERT INTO users (login, password) VALUES (?, ?);"
        cur.execute(insert_query, (login, password_hash))
    except Exception as e:
        print(f"Ошибка при регистрации: {e}")
        db_close(conn, cur)
        return render_template('lab5/register.html', error="Произошла ошибка при регистрации")
    
    db_close(conn, cur)
    return render_template('lab5/success.html', login=login)

# Авторизация пользователя
@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')

    # Получаем данные из формы
    login = request.form.get('login')
    password = request.form.get('password')

    # Проверка на пустые поля
    if not login or not password:
        return render_template('lab5/login.html', error="Заполните поля")

    conn, cur = db_connect()
    if not conn:
        return render_template('lab5/login.html', error="Ошибка подключения к базе данных")

    try:
        # Проверка пользователя
        query = "SELECT * FROM users WHERE login=%s;" if current_app.config['DB_TYPE'] == 'postgres' else "SELECT * FROM users WHERE login=?;"
        cur.execute(query, (login,))
        user = cur.fetchone()
        if not user or not check_password_hash(user['password'], password):
            db_close(conn, cur)
            return render_template('lab5/login.html', error="Логин и/или пароль неверны")

        # Сохранение логина в сессии
        session['login'] = login
    except Exception as e:
        print(f"Ошибка при авторизации: {e}")
        db_close(conn, cur)
        return render_template('lab5/login.html', error="Произошла ошибка при авторизации")
    
    db_close(conn, cur)
    return render_template('lab5/success_login.html', login=login)

# Создание статьи
@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create():
    login = session.get('login')
    if not login:
        return redirect('/lab5/lab5/login')

    if request.method == 'GET':
        return render_template('lab5/create_article.html')

    # Получаем данные из формы
    title = request.form.get('title')
    article_text = request.form.get('article_text')

    if not title or not article_text:
        return render_template('lab5/create_article.html', error="Название и текст статьи не должны быть пустыми")

    conn, cur = db_connect()
    if not conn:
        return render_template('lab5/create_article.html', error="Ошибка подключения к базе данных")

    try:
        # Получение ID пользователя
        query = "SELECT id FROM users WHERE login=%s;" if current_app.config['DB_TYPE'] == 'postgres' else "SELECT id FROM users WHERE login=?;"
        cur.execute(query, (login,))
        login_id = cur.fetchone()["id"]

        # Вставка статьи
        insert_query = "INSERT INTO articles (login_id, title, article_text) VALUES (%s, %s, %s);" if current_app.config['DB_TYPE'] == 'postgres' else "INSERT INTO articles (login_id, title, article_text) VALUES (?, ?, ?);"
        cur.execute(insert_query, (login_id, title, article_text))
    except Exception as e:
        print(f"Ошибка при создании статьи: {e}")
        db_close(conn, cur)
        return render_template('lab5/create_article.html', error="Произошла ошибка при сохранении статьи")
    
    db_close(conn, cur)
    return redirect('/lab5/lab5/list')

@lab5.route('/lab5/delete/<int:article_id>', methods=['POST'])
def delete(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/lab5/login')

    conn, cur = db_connect()

    # Удаление статьи
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("DELETE FROM articles WHERE id=%s;", (article_id,))
    else:
        cur.execute("DELETE FROM articles WHERE id=?;", (article_id,))

    db_close(conn, cur)
    return redirect('/lab5/lab5/list')

@lab5.route('/lab5/users')
def users():
    login = session.get('login')
    if not login:
        return redirect('/lab5/lab5/login')
    
    conn, cur = db_connect()

    # Получение всех логинов пользователей
    cur.execute("SELECT login FROM users;")
    users = cur.fetchall()

    db_close(conn, cur)
    return render_template('lab5/users.html', users=users)

@lab5.route('/lab5/public_articles')
def public_articles():
    conn, cur = db_connect()

    # Получение всех публичных статей
    cur.execute("SELECT articles.title, articles.article_text, users.login FROM articles JOIN users ON articles.login_id = users.id WHERE articles.is_public = TRUE;")
    articles = cur.fetchall()

    db_close(conn, cur)
    return render_template('lab5/public_articles.html', articles=articles)
