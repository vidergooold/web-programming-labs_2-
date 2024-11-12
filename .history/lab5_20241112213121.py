from flask import Blueprint, render_template, request, session
import psycopg2
from psycopg2.extras import RealDictCursor

lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html', login=session.get('login'))

def db_connect():
    try:
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='kb',
            user='irina_vidergold_knowledge_base',
            password='123'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
        return conn, cur
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")
        return None, None

def db_close(conn, cur):
    if conn:
        conn.commit()
        cur.close()
        conn.close()

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
        # Проверка, существует ли пользователь с таким логином
        cur.execute("SELECT login FROM users WHERE login = %s;", (login,))
        if cur.fetchone():
            db_close(conn, cur)
            return render_template('lab5/register.html', error="Такой пользователь уже существует")
        
        # Если пользователя нет, добавляем нового пользователя
        cur.execute("INSERT INTO users (login, password) VALUES (%s, %s);", (login, password))
        conn.commit()
    except Exception as e:
        print(f"Ошибка при регистрации пользователя: {e}")
        db_close(conn, cur)
        return render_template('lab5/register.html', error="Произошла ошибка при регистрации")
    
    db_close(conn, cur)
    return render_template('lab5/success.html', login=login)

@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    # Проверка на пустые поля
    if not login or not password:
        return render_template('lab5/login.html', error="Заполните поля")
    
    conn, cur = db_connect()
    if not conn:
        return render_template('lab5/login.html', error="Ошибка подключения к базе данных")

    try:
        # Проверка существования пользователя и его пароля
        cur.execute("SELECT * FROM users WHERE login = %s;", (login,))
        user = cur.fetchone()

        if not user or user['password'] != password:
            db_close(conn, cur)
            return render_template('lab5/login.html', error="Логин и/или пароль неверны")
        
        # Сохранение логина пользователя в сессии
        session['login'] = login
    except Exception as e:
        print(f"Ошибка при входе в систему: {e}")
        db_close(conn, cur)
        return render_template('lab5/login.html', error="Произошла ошибка при входе")

    db_close(conn, cur)
    return render_template('lab5/success_login.html', login=login)

@lab5.route('/lab5/list')
def list():
    return render_template('lab5/list.html')

@lab5.route('/lab5/create')
def create():
    return render_template('lab5/create.html')
