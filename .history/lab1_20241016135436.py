from flask import Blueprint, redirect, url_for, render_template, request, abort
lab1 = Blueprint('lab1', __name__)

@lab1.route("/resource")
def resource_page():
    global resource_created
    css_path = url_for('static', filename='main.css')
    favicon_path = url_for('static', filename='favicon.ico')
    
    if resource_created:
        status = "Ресурс создан"
    else:
        status = "Ресурс ещё не создан"
    
    create_url = url_for('create_resource')
    delete_url = url_for('delete_resource')

    return f'''
<!doctype html>
<html>
    <head>
        <title>Управление ресурсом</title>
        <link rel="stylesheet" type="text/css" href="{css_path}">
        <link rel="icon" href="{favicon_path}" type="image/x-icon">
    </head>
    <body>
        <div class="container">
            <h1>Статус ресурса</h1>
            <p>{status}</p>
            <nav>
                <ul>
                    <li><a href="{create_url}">Создать ресурс</a></li>
                    <li><a href="{delete_url}">Удалить ресурс</a></li>
                </ul>
            </nav>
            <a href="/">Вернуться на главную</a>
        </div>
    </body>
</html>
'''

@lab1.route("/created")
def create_resource():
    global resource_created
    css_path = url_for('static', filename='main.css')
    favicon_path = url_for('static', filename='favicon.ico')

    if not resource_created:
        resource_created = True
        return f'''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="{css_path}">
        <link rel="icon" href="{favicon_path}" type="image/x-icon">
    </head>
    <body>
        <div class="container">
            <h1>Успешно: ресурс создан</h1>
            <a href="/resource">Вернуться к ресурсу</a>
        </div>
    </body>
</html>
''', 201
    else:
        return f'''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="{css_path}">
        <link rel="icon" href="{favicon_path}" type="image/x-icon">
    </head>
    <body>
        <div class="container">
            <h1>Отказано: ресурс уже создан</h1>
            <a href="/resource">Вернуться к ресурсу</a>
        </div>
    </body>
</html>
''', 400

@lab1.route("/delete")
def delete_resource():
    global resource_created
    css_path = url_for('static', filename='main.css')
    favicon_path = url_for('static', filename='favicon.ico')

    if resource_created:
        resource_created = False
        return f'''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="{css_path}">
        <link rel="icon" href="{favicon_path}" type="image/x-icon">
    </head>
    <body>
        <div class="container">
            <h1>Успешно: ресурс удалён</h1>
            <a href="/resource">Вернуться к ресурсу</a>
        </div>
    </body>
</html>
''', 200
    else:
        return f'''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="{css_path}">
        <link rel="icon" href="{favicon_path}" type="image/x-icon">
    </head>
    <body>
        <div class="container">
            <h1>Отказано: ресурс отсутствует</h1>
            <a href="/resource">Вернуться к ресурсу</a>
        </div>
    </body>
</html>
''', 400

@lab1.route("/")
def lab():
    css_path = url_for('static', filename='main.css')
    favicon_path = url_for('static', filename='favicon.ico')

    # Генерируем ссылки на все маршруты
    web_url = url_for('lab1.web')
    author_url = url_for('lab1.author')
    oak_url = url_for('lab1.oak')
    counter_url = url_for('lab1.counter')
    reset_counter_url = url_for('lab1.reset_counter')
    custom_url = url_for('lab1.custom_page')

    return f'''
<!doctype html>
<html>
    <head>
        <title>Лабораторная 1</title>
        <link rel="stylesheet" type="text/css" href="{css_path}">
        <link rel="icon" href="{favicon_path}" type="image/x-icon">
    </head>
    <body>
        <h1>Лабораторная 1</h1>
        <p>Flask — фреймворк для создания веб-приложений на языке программирования Python.</p>
        <a href="/">Вернуться на главную</a>
        <h2>Список роутов</h2>
        <ul>
            <li><a href="/">Главная страница</a></li>
            <li><a href="{web_url}">Web-сервер</a></li>
            <li><a href="{author_url}">Author</a></li>
            <li><a href="{oak_url}">Oak</a></li>
            <li><a href="{counter_url}">Counter</a></li>
            <li><a href="{reset_counter_url}">Reset Counter</a></li>
            <li><a href="{custom_url}">Custom Page</a></li>
        </ul>
    </body>
</html>
'''

@lab1.route("/web")
def web():
    favicon_path = url_for('static', filename='favicon.ico')
    return f"""
<!doctype html>
<html>
    <head>
        <link rel="icon" href="{favicon_path}" type="image/x-icon">
    </head>
    <body>
        <h1>web-сервер на flask</h1>
        <a href="lab1/author">author</a>
    </body>
</html>
""", 200, {
        'X-Server': 'sample',
        'Content-Type': 'text/plain; charset=utf-8'
    }

@lab1.route("/author")
def author():
    name = "Видергольд Ирина Сергеевна"
    group = "ФБИ-22"
    faculty = "ФБ"
    favicon_path = url_for('static', filename='favicon.ico')

    return f'''
<!doctype html>
<html>
    <head>
        <link rel="icon" href="{favicon_path}" type="image/x-icon">
    </head>
    <body>
        <p>Студент: {name}</p>
        <p>Группа: {group}</p>
        <p>Факультет: {faculty}</p>
        <a href="/lab1/web">web</a>
    </body>
</html>
'''

@lab1.route("/oak")
def oak():
    path = url_for("static", filename="oak.jpg")
    css_path = url_for('static', filename='main.css')
    favicon_path = url_for('static', filename='favicon.ico')
    return f'''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="{css_path}">
        <link rel="icon" href="{favicon_path}" type="image/x-icon">
    </head>
    <body>
        <h1>Дуб</h1>
        <img src="{path}">
    </body>
</html>
'''

count = 0

@lab1.route("/counter")
def counter():
    global count
    count += 1
    reset_url = url_for('lab1.reset_counter')
    favicon_path = url_for('static', filename='favicon.ico')
    return f'''
<!doctype html>
<html>
    <head>
        <link rel="icon" href="{favicon_path}" type="image/x-icon">
    </head>
    <body>
        Сколько раз вы сюда заходили: {count}
        <a href="{reset_url}">Очистить счётчик</a>
    </body>
</html>
'''

@lab1.route("/reset_counter")
def reset_counter():
    global count
    count = 0
    favicon_path = url_for('static', filename='favicon.ico')
    return f'''
<!doctype html>
<html>
    <head>
        <link rel="icon" href="{favicon_path}" type="image/x-icon">
    </head>
    <body>
        <p>Счётчик был сброшен.</p>
        <a href="{url_for('lab1.counter')}">Вернуться на страницу счётчика</a>
    </body>
</html>
'''

@lab1.route("/custom")
def custom_page():
    image_path = url_for('static', filename='/duolingo.jpg')
    favicon_path = url_for('static', filename='favicon.ico')
    
    return f"""
<!doctype html>
<html>
    <head>
        <title>Текстовая страница с изображением</title>
        <link rel="icon" href="{favicon_path}" type="image/x-icon">
    </head>
    <body>
        <h1>Добро пожаловать на нашу страницу!</h1>
        <img src="{image_path}" alt="Sample Image" width="400px">
    </body>
</html>
"""
