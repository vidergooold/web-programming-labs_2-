from flask import Flask, url_for
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3

app = Flask(__name__)
app.register_blueprint(lab1, url_prefix='/lab1')
app.register_blueprint(lab2, url_prefix='/lab2')
app.register_blueprint(lab3, url_prefix='/lab3', name='lab3')

# Глобальная переменная для отслеживания состояния ресурса
resource_created = False

@app.route("/")
@app.route("/index")
def index():
    css_path = url_for('static', filename='main.css')
    favicon_path = url_for('static', filename='favicon.ico')
    lab1_url = url_for('lab1.lab')
    lab2_url = url_for('lab2.lab_2')
    lab3_url = url_for('lab3.lab')

    return f'''
<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
        <link rel="stylesheet" type="text/css" href="{css_path}">
        <link rel="icon" href="{favicon_path}" type="image/x-icon">
    </head>
    <body>
        <div>
            <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
            <nav>
                <ul>
                    <li><a href="{lab1_url}">Лабораторная 1</a></li>
                    <li><a href="{lab2_url}">Лабораторная 2</a></li>
                    <li><a href="{lab3_url}">Лабораторная 3</a></li>
                    <li><a href="{lab3_url}">Лабораторная 3</a></li>
                </ul>
            </nav>
        </div>
        <footer class="footer-home">
            <p>ФИО: Видергольд Ирина Сергеевна</p>
            <p>Группа: ФБИ-22</p>
            <p>Курс: 3</p>
            <p>Год: 2024</p>
        </footer>
    </body>
</html>
'''

# Обработчик для ошибки 404
@app.errorhandler(404)
def page_not_found(e):
    image_path = url_for('static', filename='/lab1/delulu.jpg')
    favicon_path = url_for('static', filename='favicon.ico')
    return f'''
<!doctype html>
<html>
    <head>
        <title>404 - Страница не найдена</title>
        <link rel="icon" href="{favicon_path}" type="image/x-icon">
        <style>
            body {{
                background-color: #f8f9fa;
                color: #333;
                font-family: Arial, sans-serif;
                text-align: center;
                padding: 50px;
            }}
            h1 {{
                font-size: 3em;
                margin-bottom: 20px;
                color: #ff6f61;
            }}
            p {{
                font-size: 1.2em;
                margin-bottom: 30px;
            }}
            img {{
                width: 300px;
                height: auto;
                margin-bottom: 30px;
            }}
            a {{
                text-decoration: none;
                color: #007bff;
                font-weight: bold;
            }}
            a:hover {{
                text-decoration: underline;
            }}
        </style>
    </head>
    <body>
        <h1>404 - Страница потерялась</h1>
        <p>Извините, но мы не можем найти нужную вам страницу.</p>
        <img src="{image_path}" alt="404 - Not Found">
        <p>Попробуйте вернуться на <a href="/">главную страницу</a> и продолжить навигацию оттуда.</p>
    </body>
</html>
''', 404

# Обработчик для ошибки 500
@app.errorhandler(500)
def internal_server_error(e):
    favicon_path = url_for('static', filename='favicon.ico')
    return f'''
<!doctype html>
<html>
    <head>
        <title>500 - Внутренняя ошибка сервера</title>
        <link rel="icon" href="{favicon_path}" type="image/x-icon">
    </head>
    <body>
        <h1>500 - Внутренняя ошибка сервера</h1>
        <p>На сервере произошла ошибка. Мы работаем над её исправлением.</p>
        <p>Пожалуйста, вернитесь на <a href="/">главную страницу</a> и попробуйте снова позже.</p>
    </body>
</html>
''', 500

