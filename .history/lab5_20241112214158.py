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
            password='123'  # Убедитесь, что здесь нет специальных символов
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
        return conn, cur
    except UnicodeDecodeError as e:
        print(f"Ошибка кодировки: {e}")
        raise e
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")
        raise e
 

def db_close(conn, cur):
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

    # Проверка на существование пользователя с таким логином
    cur.execute("SELECT login FROM users WHERE login = %s;", (login,))
    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab5/register.html', error="Такой пользователь уже существует")

    # Добавляем нового пользователя
    try:
        cur.execute("INSERT INTO users (login, password) VALUES (%s, %s);", (login, password))
    except Exception as e:
        db_close(conn, cur)
        return render_template('lab5/register.html', error=f"Ошибка при регистрации: {e}")

    # Закрываем соединение с базой данных
    db_close(conn, cur)
    return render_template('lab5/success.html', login=login)
    
@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not login or not password:
        return render_template('lab5/login.html', error="Заполните поля")
    
    # Подключение к базе данных
    conn, cur = db_connect()

    # Проверка существования пользователя
    cur.execute("SELECT * FROM users WHERE login = %s;", (login,))
    user = cur.fetchone()

    if not user or user['password'] != password:
        db_close(conn, cur)
        return render_template('lab5/login.html', error="Логин и/или пароль неверны")

    # Сохранение логина пользователя в сессии
    session['login'] = login 
    db_close(conn, cur)
 
    return render_template('lab5/success_login.html', login=login)

@lab5.route('/lab5/list')
def list():
    return render_template('lab5/list.html')

@lab5.route('/lab5/create')
def create():
    return render_template('lab5/create.html')

