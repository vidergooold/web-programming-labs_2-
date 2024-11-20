from flask import Blueprint, render_template, request, session, redirect, current_app  
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash 
import sqlite3
from os import path

lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html', login=session.get('login'))

# def db_connect():
#     if current_app.config['DB_TYPE'] == 'postgres':
#         conn = psycopg2.connect(
#             host='127.0.0.1',
#             database='kb',
#             user='irina_vidergold_knowledge_base',
#             password='123'
#         )
#         cur = conn.cursor(cursor_factory=RealDictCursor)
#     else:
#         dir_path = path.dirname(path.realpath(__file__))
#         db_path = path.join(dir_path, "database.db")
#         conn = sqlite3.connect(db_path)
#         conn.row_factory = sqlite3.Row 
#         cur = conn.cursor()

#     return conn, cur 

# def db_close(conn, cur):
#     conn.commit()
#     cur.close()
#     conn.close()

# def db_connect():
#     if current_app.config['DB_TYPE'] == 'postgres':
#         # Подключение к базе данных
#         conn = sqlite3.connect(r'C:\Users\admin\Desktop\web-programming-labs_2\database.db') 
#         conn.row_factory = sqlite3.Row
#         cur = conn.cursor()
#     else:
#         dir_path = path.dirname(path.realpath(__file__))
#         db_path = path.join(dir_path, "database.db")
#         conn = sqlite3.connect(db_path)
#         conn.row_factory = sqlite3.Row
#         cur = conn.cursor()
#     return conn, cur

# def db_close(conn,cur):
#     conn.commit()
#     cur.close()
#     conn.close()

@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')
    
    # Получаем данные из формы
    login = request.form.get('login')
    password = request.form.get('password')

    # Проверка на пустые поля
    if not login or not password:
        return render_template('lab5/register.html', 
                               error="Заполните все поля")

    conn, cur = db_connect()

    # Проверка существования пользователя
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT login FROM users WHERE login=?;", (login,))

    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab5/register.html', 
                               error="Такой пользователь уже существует")
        
    # Если пользователя нет, добавляем нового пользователя
    password_hash = generate_password_hash(password)
    if current_app.config['DB_TYPE'] == 'postgres': 
        cur.execute("INSERT INTO users (login, password) VALUES (%s, %s);", (login, password_hash))
    else:
        cur.execute("INSERT INTO users (login, password) VALUES (?, ?);", (login, password_hash))
        
    db_close(conn, cur) 
    return render_template('lab5/success.html', login=login)

@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not (login or password):
        return render_template('lab5/login.html', error="Заполните поля")
    
    # Подключение к базе данных
    conn, cur = db_connect()

    # Поиск пользователя в базе данных
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login,))
    user = cur.fetchone()

    if not user or not check_password_hash(user['password'], password):
        db_close(conn, cur)
        return render_template('lab5/login.html', error="Логин и/или пароль неверны")

    # Сохранение логина пользователя в сессии
    session['login'] = login 
    db_close(conn, cur)
 
    return render_template('lab5/success_login.html', login=login)

@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create():
    login = session.get('login')
    if not login:
        return redirect('/lab5/lab5/login')
    
    if request.method == 'GET':
        return render_template('lab5/create_article.html')
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')

    # Проверка на пустые поля
    if not title or not article_text:
        return render_template('lab5/create_article.html', error="Название и текст статьи не должны быть пустыми")

    conn, cur = db_connect()

    # Получение ID пользователя
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    result = cur.fetchone()
    user_id = result["id"] if result else None

    # Проверка, что user_id был найден
    if user_id is None:
        db_close(conn, cur)
        return render_template('lab5/create_article.html', 
                               error="Пользователь не найден")

    # Вставка статьи в базу данных
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO articles (user_id, title, article_text) VALUES (%s, %s, %s);", (user_id, title, article_text))
    else:
        cur.execute("INSERT INTO articles (user_id, title, article_text) VALUES (?, ?, ?);", (user_id, title, article_text))

    db_close(conn, cur)
    return redirect('/lab5/lab5')

@lab5.route('/lab5/list')
def list():
    login = session.get('login')
    if not login:
        return redirect('/lab5/lab5/login')

    conn, cur = db_connect()

    # Получение ID пользователя
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    user_id = cur.fetchone()["id"]

    # Получение статей пользователя с любимыми статьями первыми
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE user_id=%s ORDER BY is_favorite DESC;", (user_id,))
    else:
        cur.execute("SELECT * FROM articles WHERE user_id=? ORDER BY is_favorite DESC;", (user_id,))
    articles = cur.fetchall()

    db_close(conn, cur)

    # Проверка на отсутствие статей
    if not articles:
        message = "У вас пока нет статей."
    else:
        message = None

    return render_template('/lab5/articles.html', articles=articles, message=message)

@lab5.route('/lab5/logout')
def logout():
    session.pop('login', None)
    return redirect('/lab5/lab5')

@lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
def edit(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/lab5/login')

    conn, cur = db_connect()

    if request.method == 'GET':
        # Получение статьи для редактирования
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM articles WHERE id=%s;", (article_id,))
        else:
            cur.execute("SELECT * FROM articles WHERE id=?;", (article_id,))
        article = cur.fetchone()
        db_close(conn, cur)

        if not article:
            return redirect('/lab5/lab5/list')

        return render_template('lab5/edit_article.html', article=article)
    
    # Обновление статьи
    title = request.form.get('title')
    article_text = request.form.get('article_text')

    if not title or not article_text:
        return render_template('lab5/edit_article.html', article={'id': article_id, 'title': title, 'article_text': article_text}, error="Название и текст статьи не должны быть пустыми")

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("UPDATE articles SET title=%s, article_text=%s WHERE id=%s;", (title, article_text, article_id))
    else:
        cur.execute("UPDATE articles SET title=?, article_text=? WHERE id=?;", (title, article_text, article_id))

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
    cur.execute("SELECT articles.title, articles.article_text, users.login FROM articles JOIN users ON articles.user_id = users.id WHERE articles.is_public = TRUE;")
    articles = cur.fetchall()

    db_close(conn, cur)
    return render_template('lab5/public_articles.html', articles=articles)

