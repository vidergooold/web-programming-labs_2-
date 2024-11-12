from flask import Blueprint, render_template
import psycopg2

lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html')

@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
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
        cur.execute("INSERT INTO users (login, password) VALUES ('{login}', '{password}');")
        cur.close()
        conn.close()
        return render_template('lab5/success.html', login=login)
    
        # Если пользователя нет, добавляем нового пользователя
        cur.execute("INSERT INTO users (login, password) VALUES ('{login}', '{password}');")
        conn.commit()
        cur.close()
        conn.close()
        return render_template('lab5/success.html', login=login)
