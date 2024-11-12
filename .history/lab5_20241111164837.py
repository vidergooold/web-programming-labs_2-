from flask import Blueprint, render_template, request, redirect, g
import psycopg2

lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html')

# Подключение к базе данных
DATABASE = {
    'dbname': 'irina_vidergold_knowledge_base',
    'user': 'irina_vidergold_knowledge_base',
    'password': '123',
    'host': 'localhost'
}

def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(
            dbname=DATABASE['dbname'],
            user=DATABASE['user'],
            password=DATABASE['password'],
            host=DATABASE['host']
        )
    return g.db

@lab5.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Получаем данные из формы
        login = request.form.get('login')
        password = request.form.get('password')

        # Проверка на пустые поля
        if not login or not password:
            return render_template('lab5/register.html', error="Заполните все поля")

        conn = psycopg2.connect(
            host = '127.0.0.1',
            database = 'irina_vidergold_knowledge_base',
            user = 'irina_vidergold_knowledge_base',
            password = '123'
        )
        cur = conn.sursor()

        cur.execute(f"SELECT login FROM users WHERE login ='{login}';")
        if cur.fetchone():
            cur.close()
            conn.close()
            return render_template('lab5/register.html', 
                                   error="Такой пользователь уже существует")
        
        # Если пользователя нет, добавляем нового пользователя
        cur.execute("INSERT INTO users (login, password) VALUES )


        
        if cur.fetchone():
            # Закрываем соединение и возвращаем сообщение об ошибке
            cur.close()
            return render_template('lab5/register.html', error="Такой пользователь уже существует")

        # Если пользователя нет, добавляем нового пользователя
        cur.execute("INSERT INTO users (login, password) VALUES (%s, %s)", (login, password))
        db.commit()  # Сохраняем изменения
        cur.close()

        # Перенаправляем на страницу успеха
        return render_template('lab5/success.html', login=login)
    
    # Если метод GET, просто отображаем форму
    return render_template('lab5/register.html')
