from flask import Flask, url_for, redirect, render_template

app = Flask(__name__)

# Глобальная переменная для отслеживания состояния ресурса
resource_created = False

@app.route("/")
@app.route("/index")
def index():
    css_path = url_for('static', filename='style.css')
    favicon_path = url_for('static', filename='favicon.ico')
    return f'''
<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
        <link rel="stylesheet" type="text/css" href="{css_path}">
        <link rel="icon" href="{favicon_path}" type="image/x-icon">
    </head>
    <body>
        <div class="container">
            <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
            <nav>
                <ul>
                    <li><a href="/lab1/resource">Управление ресурсом</a></li>
                    <li><a href="/lab2">Лабораторная 2</a></li>
                </ul>
            </nav>
            <footer>
                <p>ФИО: Видергольд Ирина Сергеевна</p>
                <p>Группа: ФБИ-22</p>
                <p>Курс: 3</p>
                <p>Год: 2024</p>
            </footer>
        </div>
    </body>
</html>
'''

@app.route("/lab1/resource")
def resource_page():
    global resource_created
    css_path = url_for('static', filename='style.css')
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

@app.route("/lab1/created")
def create_resource():
    global resource_created
    css_path = url_for('static', filename='style.css')
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
            <a href="/lab1/resource">Вернуться к ресурсу</a>
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
            <a href="/lab1/resource">Вернуться к ресурсу</a>
        </div>
    </body>
</html>
''', 400

@app.route("/lab1/delete")
def delete_resource():
    global resource_created
    css_path = url_for('static', filename='style.css')
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
            <a href="/lab1/resource">Вернуться к ресурсу</a>
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
            <a href="/lab1/resource">Вернуться к ресурсу</a>
        </div>
    </body>
</html>
''', 400

@app.route("/lab1")
def lab1():
    css_path = url_for('static', filename='style.css')
    favicon_path = url_for('static', filename='favicon.ico')

    # Генерируем ссылки на все маршруты
    web_url = url_for('web')
    author_url = url_for('author')
    oak_url = url_for('oak')
    counter_url = url_for('counter')
    reset_counter_url = url_for('reset_counter')
    custom_url = url_for('custom_page')

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

@app.route("/lab1/web")
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
        <a href="/lab1/author">author</a>
    </body>
</html>
""", 200, {
        'X-Server': 'sample',
        'Content-Type': 'text/plain; charset=utf-8'
    }

@app.route("/lab1/author")
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

@app.route("/lab1/oak")
def oak():
    path = url_for("static", filename="oak.jpg")
    css_path = url_for("static", filename="lab1.css")
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

@app.route("/lab1/counter")
def counter():
    global count
    count += 1
    reset_url = url_for('reset_counter')
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

@app.route("/lab1/reset_counter")
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
        <a href="/lab1/counter">Вернуться на страницу счётчика</a>
    </body>
</html>
'''

@app.route("/custom")
def custom_page():
    image_path = url_for('static', filename='duolingo.jpg')
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

    # Возвращаем HTML-контент с заголовками
    return content, 200, {
        'Content-Language': 'ru',  # Указываем язык содержимого страницы (русский)
        'X-Powered-By': 'Flask',  # Дополнительный заголовок
        'X-Custom-Header': 'My Custom Header',  # Ещё один заголовок
        'Content-Type': 'text/html; charset=utf-8'  # Указываем тип контента и кодировку
    }

# Обработчик для ошибки 400
@app.route("/400")
def bad_request():
    favicon_path = url_for('static', filename='favicon.ico')
    return f'''
<!doctype html>
<html>
    <head>
        <title>400 - Bad Request</title>
        <link rel="icon" href="{favicon_path}" type="image/x-icon">
    </head>
    <body>
        <h1>400 - Bad Request</h1>
        <p>Ваш запрос был неверен. Проверьте параметры и попробуйте снова.</p>
    </body>
</html>
''', 400

# Обработчик для ошибки 401
@app.route("/401")
def unauthorized():
    favicon_path = url_for('static', filename='favicon.ico')
    return f'''
<!doctype html>
<html>
    <head>
        <title>401 - Unauthorized</title>
        <link rel="icon" href="{favicon_path}" type="image/x-icon">
    </head>
    <body>
        <h1>401 - Unauthorized</h1>
        <p>Для доступа к этому ресурсу требуется аутентификация. Пожалуйста, войдите в систему.</p>
    </body>
</html>
''', 401

# Обработчик для ошибки 402
@app.route("/402")
def payment_required():
    favicon_path = url_for('static', filename='favicon.ico')
    return f'''
<!doctype html>
<html>
    <head>
        <title>402 - Payment Required</title>
        <link rel="icon" href="{favicon_path}" type="image/x-icon">
    </head>
    <body>
        <h1>402 - Payment Required</h1>
        <p>Этот ресурс требует оплаты. Пожалуйста, произведите платеж, чтобы продолжить.</p>
    </body>
</html>
''', 402

# Обработчик для ошибки 403
@app.route("/403")
def forbidden():
    favicon_path = url_for('static', filename='favicon.ico')
    return f'''
<!doctype html>
<html>
    <head>
        <title>403 - Forbidden</title>
        <link rel="icon" href="{favicon_path}" type="image/x-icon">
    </head>
    <body>
        <h1>403 - Forbidden</h1>
        <p>У вас нет прав доступа к этому ресурсу.</p>
    </body>
</html>
''', 403

# Обработчик для ошибки 405
@app.route("/405")
def method_not_allowed():
    favicon_path = url_for('static', filename='favicon.ico')
    return f'''
<!doctype html>
<html>
    <head>
        <title>405 - Method Not Allowed</title>
        <link rel="icon" href="{favicon_path}" type="image/x-icon">
    </head>
    <body>
        <h1>405 - Method Not Allowed</h1>
        <p>Метод, использованный в запросе, не поддерживается для этого ресурса.</p>
    </body>
</html>
''', 405

# Обработчик для ошибки 418 (I'm a teapot)
@app.route("/418")
def im_a_teapot():
    favicon_path = url_for('static', filename='favicon.ico')
    return f'''
<!doctype html>
<html>
    <head>
        <title>418 - I'm a teapot</title>
        <link rel="icon" href="{favicon_path}" type="image/x-icon">
    </head>
    <body>
        <h1>418 - I'm a teapot</h1>
        <p>Я — чайник. RFC 2324 гласит, что этот сервер не может заварить кофе, так как он является чайником.</p>
    </body>
</html>
''', 418

# Обработчик для ошибки 404
@app.errorhandler(404)
def page_not_found(e):
    image_path = url_for('static', filename='delulu.jpg')
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

# Обработчик, который вызывает ошибку на сервере
@app.route("/cause-error")
def cause_error():
    return 1 / 0  # Ошибка деления на ноль

# Маршрут для лабораторной работы 2 с фавиконкой
@app.route('/lab2', strict_slashes=False)
def lab2():
    css_path = url_for('static', filename='style.css')
    favicon_path = url_for('static', filename='favicon.ico')
    return f'''
<!doctype html>
<html>
    <head>
        <title>Лабораторная 2 - Ссылки</title>
        <link rel="stylesheet" type="text/css" href="{css_path}">
        <link rel="icon" href="{favicon_path}" type="image/x-icon">
    </head>
    <body>
        <h1>Список доступных адресов для лабораторной 2:</h1>
        <ul>
            <li><a href="/lab2/calc/1/1">Калькулятор (1+1)</a></li>
            <li><a href="/lab2/calc/3">Калькулятор (3+1)</a></li>
            <li><a href="/lab2/calc">Калькулятор (по умолчанию 1+1)</a></li>
            <li><a href="/lab2/flowers">Список всех цветов</a></li>
            <li><a href="/lab2/clear_flowers">Очистить список цветов</a></li>
            <li><a href="/lab2/filter">Фильтры</a></li>
            <li><a href="/lab2/example">Пример</a></li>
            <li><a href="/lab2/berries">Ягоды</a></li>
            <li><a href="/lab2/books">Книги</a></li>
        </ul>
    </body>
</html>
'''

# Маршруты для добавления и вывода цветов
@app.route('/lab2/a')
def a():
    return 'без слэша'

@app.route('/lab2/a/')
def a2():
    return 'со слэшем'

flower_list = ['rose', 'tulip', 'violet', 'daisy']

# Маршрут для добавления цветка
@app.route('/lab2/add_flower/', defaults={'name': None})
@app.route('/lab2/add_flower/<string:name>')
def add_flower(name):
    favicon_path = url_for('static', filename='favicon.ico')
    if not name:
        return "Вы не задали имя цветка", 400

    flower_list.append(name)  # Добавляем цветок в список

    return f"""
        <html>
        <head>
            <link rel="icon" href="{favicon_path}" type="image/x-icon">
        </head>
        <body>
            <h1>Цветок {name} был успешно добавлен!</h1>
            <p>Теперь в списке {len(flower_list)} цветов.</p>
            <h2>Список всех цветов:</h2>
            <ul>
                {''.join(f"<li>{flower}</li>" for flower in flower_list)}
            </ul>
            <br>
            <a href='/lab2/flowers'>Посмотреть все цветы</a>
        </body>
        </html>
    """

# Маршрут для вывода всех цветов
@app.route('/lab2/flowers')
def show_flowers():
    favicon_path = url_for('static', filename='favicon.ico')
    if not flower_list:
        return f"""
            <html>
            <head>
                <link rel="icon" href="{favicon_path}" type="image/x-icon">
            </head>
            <body>
                <h1>Список цветов пуст.</h1>
                <br>
                <a href='/lab2/add_flower/'>Добавить первый цветок</a>
            </body>
            </html>
        """
    
    flowers_html = "<ul>"
    for flower in flower_list:
        flowers_html += f"<li>{flower}</li>"
    flowers_html += "</ul>"
    
    return f"""
        <html>
        <head>
            <link rel="icon" href="{favicon_path}" type="image/x-icon">
        </head>
        <body>
            <h1>Всего цветов: {len(flower_list)}</h1>
            <h2>Список всех цветов:</h2>
            {flowers_html}
            <br>
            <a href='/lab2/clear_flowers'>Очистить список цветов</a>
        </body>
        </html>
    """

# Маршрут для очистки списка цветов
@app.route('/lab2/clear_flowers')
def clear_flowers():
    favicon_path = url_for('static', filename='favicon.ico')
    flower_list.clear()

    return f"""
        <html>
        <head>
            <link rel="icon" href="{favicon_path}" type="image/x-icon">
        </head>
        <body>
            <h1>Список цветов был успешно очищен!</h1>
            <br>
            <a href='/lab2/flowers'>Посмотреть все цветы</a>
        </body>
        </html>
    """

# Маршрут для примера
@app.route('/lab2/example')
def example():
    name = 'Видергольд Ирина'
    lab_num1 = '2'
    lab_num2 = '2'
    group = 'ФБИ-22'
    number = '3'
    fruits = [
        {'name': 'apples', 'price': 100},
        {'name': 'pears', 'price': 150}, 
        {'name': 'oranges', 'price': 90}, 
        {'name': 'mangos', 'price': 120}, 
        {'name': 'cherries', 'price': 200}
    ]
    return render_template('example.html', 
                           name=name, lab_num1=lab_num1, lab_num2=lab_num2, 
                           group=group, number=number, fruits=fruits)

# Фильтр с фавиконкой
@app.route('/lab2/filter')
def filter():
    phrase = "0 <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase=phrase)

# Основной маршрут для вычислений с двумя числами
@app.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    favicon_path = url_for('static', filename='favicon.ico')
    result_add = a + b
    result_sub = a - b
    result_mul = a * b
    result_div = a / b if b != 0 else '∞'
    result_pow = a ** b

    return f"""
    <html>
    <head>
        <link rel="icon" href="{favicon_path}" type="image/x-icon">
    </head>
    <body>
        <h2>Расчёт с параметрами:</h2>
        <p>{a} + {b} = {result_add}</p>
        <p>{a} - {b} = {result_sub}</p>
        <p>{a} × {b} = {result_mul}</p>
        <p>{a} / {b} = {result_div}</p>
        <p>{a}<sup>{b}</sup> = {result_pow}</p>
    </body>
    </html>
    """

# Перенаправление с /lab2/calc/ на /lab2/calc/1/1
@app.route('/lab2/calc/', strict_slashes=False)
def default_calc():
    return redirect(url_for('calc', a=1, b=1))

# Перенаправление с /lab2/calc/<int:a> на /lab2/calc/a/1
@app.route('/lab2/calc/<int:a>', strict_slashes=False)
def calc_with_one(a):
    return redirect(url_for('calc', a=a, b=1))

# Список книг на стороне сервера
books = [
    {"author": "Джордж Оруэлл", "title": "1984", "genre": "Антиутопия", "pages": 328},
    {"author": "Фёдор Достоевский", "title": "Преступление и наказание", "genre": "Классика", "pages": 671},
    {"author": "Джейн Остин", "title": "Гордость и предубеждение", "genre": "Роман", "pages": 432},
    {"author": "Лев Толстой", "title": "Война и мир", "genre": "Классика", "pages": 1225},
    {"author": "Рей Брэдбери", "title": "451 градус по Фаренгейту", "genre": "Фантастика", "pages": 249},
    {"author": "Харуки Мураками", "title": "Норвежский лес", "genre": "Роман", "pages": 384},
    {"author": "Эрих Мария Ремарк", "title": "На Западном фронте без перемен", "genre": "Антивоенная", "pages": 295},
    {"author": "Михаил Булгаков", "title": "Мастер и Маргарита", "genre": "Фантастика", "pages": 560},
    {"author": "Франц Кафка", "title": "Процесс", "genre": "Экзистенциализм", "pages": 320},
    {"author": "Габриэль Гарсиа Маркес", "title": "Сто лет одиночества", "genre": "Магический реализм", "pages": 417}
]

# Маршрут для вывода списка книг с использованием шаблона
@app.route('/lab2/books')
def show_books():
    favicon_path = url_for('static', filename='favicon.ico')
    return render_template('books.html', books=books, favicon_path=favicon_path)

# Список ягод с информацией: название, описание, имя файла картинки
berries = [
    {"name": "Клубника", "description": "Сочная красная ягода, богата витаминами.", "image": "strawberry.jpg"},
    {"name": "Голубика", "description": "Мелкие синие ягоды, отлично подходят для десертов.", "image": "blueberry.jpg"},
    {"name": "Малина", "description": "Сладкая и ароматная ягода с лёгкой кислинкой.", "image": "raspberry.jpg"},
    {"name": "Ежевика", "description": "Тёмные, почти чёрные ягоды с насыщенным вкусом.", "image": "blackberry.jpg"},
    {"name": "Вишня", "description": "Кисло-сладкая ягода, популярная в выпечке.", "image": "cherry.jpg"}
]

@app.route('/lab2/berries')
def show_berries():
    favicon_path = url_for('static', filename='favicon.ico')
    return render_template('berries.html', berries=berries, favicon_path=favicon_path)
