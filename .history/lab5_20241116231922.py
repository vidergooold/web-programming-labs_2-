from flask import Blueprint, request, render_template, redirect, session, url_for, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from os import path

lab5 = Blueprint('lab5', __name__)

# Функция для подключения к базе данных
def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='ira_vidergold_knowledge_base',
            user='ira_vidergold_knowledge_base',
            password='123'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        db_path = path.join(path.dirname(path.realpath(__file__)), 'database.db')
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    return conn, cur

# Функция для закрытия соединения
def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

@lab5.route('/lab5')
def lab5_home():
    user_name = session.get('login', 'Anonymous')
    return render_template('lab5/lab5.html', user_name=user_name)

@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')

        if not login or not password:
            error = "Заполните все поля"
            return render_template('lab5/register.html', error=error)

        conn, cur = db_connect()
        query = "SELECT login FROM users WHERE login=%s" if current_app.config['DB_TYPE'] == 'postgres' else "SELECT login FROM users WHERE login=?"
        cur.execute(query, (login,))
        
        if cur.fetchone():
            db_close(conn, cur)
            error = "Такой пользователь уже существует"
            return render_template('lab5/register.html', error=error)
        
        password_hash = generate_password_hash(password)
        insert_query = "INSERT INTO users (login, password) VALUES (%s, %s)" if current_app.config['DB_TYPE'] == 'postgres' else "INSERT INTO users (login, password) VALUES (?, ?)"
        cur.execute(insert_query, (login, password_hash))
        db_close(conn, cur)
        return render_template('lab5/success.html')

    return render_template('lab5/register.html')

@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')

        if not login or not password:
            error = "Заполните все поля"
            return render_template('lab5/login.html', error=error)
        
        conn, cur = db_connect()
        query = "SELECT * FROM users WHERE login=%s" if current_app.config['DB_TYPE'] == 'postgres' else "SELECT * FROM users WHERE login=?"
        cur.execute(query, (login,))
        user = cur.fetchone()
        db_close(conn, cur)

        if user and check_password_hash(user['password'], password):
            session['login'] = login
            return render_template('lab5/success_login.html', login=login)
        else:
            error = "Неверный логин и/или пароль"
    return render_template('lab5/login.html', error=error)

@lab5.route('/lab5/logout', methods=['POST'])
def logout():
    session.pop('login', None)
    return redirect(url_for('lab5.lab5_home'))

@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create():
    if 'login' not in session:
        return redirect(url_for('lab5.login'))

    if request.method == 'POST':
        title = request.form.get('title')
        article_text = request.form.get('article_text')
        is_favorite = request.form.get('is_favorite') is not None
        is_public = request.form.get('is_public') is not None

        conn, cur = db_connect()
        query = "SELECT id FROM users WHERE login=%s" if current_app.config['DB_TYPE'] == 'postgres' else "SELECT id FROM users WHERE login=?"
        cur.execute(query, (session['login'],))
        user_id = cur.fetchone()['id']
        
        insert_query = """
            INSERT INTO articles (user_id, title, article_text, is_favorite, is_public)
            VALUES (%s, %s, %s, %s, %s)
        """ if current_app.config['DB_TYPE'] == 'postgres' else """
            INSERT INTO articles (user_id, title, article_text, is_favorite, is_public)
            VALUES (?, ?, ?, ?, ?)
        """
        cur.execute(insert_query, (user_id, title, article_text, is_favorite, is_public))
        db_close(conn, cur)
        return redirect(url_for('lab5.list_articles'))

    return render_template('lab5/create_article.html')

@lab5.route('/lab5/list', methods=['GET'])
def list_articles():
    if 'login' not in session:
        return redirect(url_for('lab5.login'))

    conn, cur = db_connect()
    query = "SELECT id FROM users WHERE login=%s" if current_app.config['DB_TYPE'] == 'postgres' else "SELECT id FROM users WHERE login=?"
    cur.execute(query, (session['login'],))
    user = cur.fetchone()

    if user:
        user_id = user['id']
        article_query = """
            SELECT * FROM articles 
            WHERE user_id=%s 
            ORDER BY is_favorite DESC
        """ if current_app.config['DB_TYPE'] == 'postgres' else """
            SELECT * FROM articles 
            WHERE user_id=? 
            ORDER BY is_favorite DESC
        """
        cur.execute(article_query, (user_id,))
        articles = cur.fetchall()
    else:
        articles = []

    db_close(conn, cur)
    return render_template('lab5/articles.html', articles=articles)

@lab5.route('/lab5/public_articles', methods=['GET'])
def public_articles():
    conn, cur = db_connect()
    query = "SELECT * FROM articles WHERE is_public=TRUE ORDER BY is_favorite DESC" if current_app.config['DB_TYPE'] == 'postgres' else "SELECT * FROM articles WHERE is_public=1 ORDER BY is_favorite DESC"
    cur.execute(query)
    public_articles = cur.fetchall()
    db_close(conn, cur)
    return render_template('lab5/public_articles.html', articles=public_articles)

@lab5.route('/lab5/edit_article/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    if 'login' not in session:
        return redirect(url_for('lab5.login'))

    conn, cur = db_connect()
    query = """
        SELECT * FROM articles WHERE id=%s AND user_id=(SELECT id FROM users WHERE login=%s)
    """ if current_app.config['DB_TYPE'] == 'postgres' else """
        SELECT * FROM articles WHERE id=? AND user_id=(SELECT id FROM users WHERE login=?)
    """
    cur.execute(query, (article_id, session['login']))
    article = cur.fetchone()

    if not article:
        db_close(conn, cur)
        return "Статья не найдена или у вас нет прав для ее редактирования", 403

    if request.method == 'POST':
        title = request.form.get('title')
        article_text = request.form.get('article_text')
        is_favorite = bool(request.form.get('is_favorite'))
        is_public = bool(request.form.get('is_public'))

        if not title or not article_text:
            error = "Заполните все поля"
            return render_template('lab5/edit_article.html', article=article, error=error)

        update_query = """
            UPDATE articles
            SET title=%s, article_text=%s, is_favorite=%s, is_public=%s
            WHERE id=%s
        """ if current_app.config['DB_TYPE'] == 'postgres' else """
            UPDATE articles
            SET title=?, article_text=?, is_favorite=?, is_public=?
            WHERE id=?
        """
        cur.execute(update_query, (title, article_text, is_favorite, is_public, article_id))
        db_close(conn, cur)
        return redirect(url_for('lab5.list_articles'))

    db_close(conn, cur)
    return render_template('lab5/edit_article.html', article=article)

@lab5.route('/lab5/delete/<int:article_id>', methods=['POST'])
def delete_article(article_id):
    if 'login' not in session:
        return redirect(url_for('lab5.login'))

    conn, cur = db_connect()
    delete_query = """
        DELETE FROM articles WHERE id=%s AND user_id=(SELECT id FROM users WHERE login=%s)
    """ if current_app.config['DB_TYPE'] == 'postgres' else """
        DELETE FROM articles WHERE id=? AND user_id=(SELECT id FROM users WHERE login=?)
    """
    cur.execute(delete_query, (article_id, session['login']))
    db_close(conn, cur)
    return redirect(url_for('lab5.list_articles'))

@lab5.route('/lab5/users', methods=['GET'])
def list_users():
    conn, cur = db_connect()
    query = "SELECT login FROM users"
    cur.execute(query)
    users = cur.fetchall()
    db_close(conn, cur)
    return render_template('lab5/users.html', users=users)


@lab5.route('/lab5/public_articles', methods=['GET'])
def show_public_articles():
    conn, cur = db_connect()
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE is_public=TRUE")
    else:
        cur.execute("SELECT * FROM articles WHERE is_public=1")
    
    articles = cur.fetchall()
    db_close(conn, cur)
    return render_template('lab5/public_articles.html', articles=articles)

