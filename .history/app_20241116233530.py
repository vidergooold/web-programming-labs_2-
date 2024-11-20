from flask import Flask, url_for
import os
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5

app = Flask(__name__)

# Регистрация Blueprints
app.register_blueprint(lab1, url_prefix='/lab1')
app.register_blueprint(lab2, url_prefix='/lab2')
app.register_blueprint(lab3, url_prefix='/lab3')
app.register_blueprint(lab4, url_prefix='/lab4')
app.register_blueprint(lab5, url_prefix='/lab5')

# Настройки приложения
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'секретно-секретный секрет')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'sqlite')  # Возможные значения: 'postgres' или 'sqlite'

@app.route("/")
@app.route("/index")
def index():
    css_path = url_for('static', filename='main.css')
    favicon_path = url_for('static', filename='favicon.ico')
    lab1_url = url_for('lab1.lab')
    lab2_url = url_for('lab2.lab_2')
    lab3_url = url_for('lab3.lab')
    lab4_url = url_for('lab4.lab')
    lab5_url = url_for('lab5.lab5_home')  # Исправлено

    return f'''
<!doctype html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>НГТУ, ФБ, Лабораторные работы</title>
    <link rel="stylesheet" href="{css_path}">
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
                <li><a href="{lab4_url}">Лабораторная 4</a></li>
                <li><a href="{lab5_url}">Лабораторная 5</a></li>
            </ul>
        </nav>
    </div>
</body>
</html>
'''

if __name__ == "__main__":
    app.run(debug=True)
