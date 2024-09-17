from flask import Flask, url_for, redirect
app = Flask(__name__)

@app.route("/")
@app.route("/index")  # Маршруты для главной страницы
def index():
    return '''
<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
    </head>
    <body>
        <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
        <nav>
            <ul>
                <li><a href="/lab1">Первая лабораторная</a></li> <!-- Ссылка на первую лабораторную -->
            </ul>
        </nav>
        <footer>
            <p>ФИО: Видергольд Ирина Сергеевна</p>
            <p>Группа: ФБИ-22</p>
            <p>Курс: 2</p>
            <p>Год: 2024</p>
        </footer>
    </body>
</html>
'''

@app.route("/lab1")  # Маршрут для первой лабораторной
def lab1():
    return '''
<!doctype html>
<html>
    <head>
        <title>Лабораторная 1</title>
    </head>
    <body>
        <h1>Лабораторная 1</h1>
        <p>Flask — фреймворк для создания веб-приложений на языке программирования 
        Python, использующий набор инструментов Werkzeug, а также шаблонизатор Jinja2. 
        Относится к категории так называемых микрофреймворков — минималистичных каркасов 
        веб-приложений, сознательно предоставляющих лишь самые базовые возможности.</p>
        <a href="/">Вернуться на главную</a> <!-- Ссылка на корень сайта -->
    </body>
</html>
'''

@app.route("/lab1/web")
def web():
    return """<!doctype html>
        <html>
             <body>
                  <h1>web-сервер на flask</h1>
                  <a href="/author">author</a>
             </body>
        </html>""", 200, {
            'X-Server': 'sample',
            'Content-Type': 'text/plain; charset=utf-8'
        }

@app.route("/lab1/author")
def author():
    name = "Видергольд Ирина Сергеевна"
    group = "ФБИ-22"
    faculty = "ФБ"

    return """<!doctype html>
        <html>
            <body>
                <p>Студент: """ + name + """</p>
                <p>Группа: """ + group + """</p>
                <p>Факультет: """ + faculty + """</p>
                <a href="/lab1/web">web</a>
            </body>
        </html>"""

@app.route("/lab1/oak")
def oak():
    path = url_for("static", filename="oak.jpg")
    css_path = url_for("static", filename="lab1.css")
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="''' + css_path + '''">
    </head>
    <body>
        <h1>Дуб</h1>
        <img src="''' + path + '''">
    </body>
</html>
'''

count = 0

@app.route("/lab1/counter")
def counter():
    global count
    count += 1
    reset_url = url_for('reset_counter')  # URL для сброса счётчика
    return '''
<!doctype html>
<html>
    <body>
        Сколько раз вы сюда заходили: ''' + str(count) + '''
        <a href="''' + reset_url + '''">Очистить счётчик</a> <!-- Ссылка для сброса счётчика -->
    </body>
</html>
'''

@app.route("/lab1/reset_counter")
def reset_counter():
    global count
    count = 0  # Сброс значения счётчика
    return '''
<!doctype html>
<html>
    <body>
        <p>Счётчик был сброшен.</p>
        <a href="/lab1/counter">Вернуться на страницу счётчика</a>
    </body>
</html>
'''

@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@app.route("/lab1/created")
def created():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Создано успешно</h1>
        <div><i>что-то создано...</i></div>
    </body>
</html>
''', 201

@app.route("/400")
def bad_request():
    return '''
<!doctype html>
<html>
    <body>
        <h1>400 - Bad Request</h1>
        <p>Ваш запрос был неверен. Проверьте параметры и попробуйте 
        снова.</p>
    </body>
</html>
''', 400

@app.route("/401")
def unauthorized():
    return '''
<!doctype html>
<html>
    <body>
        <h1>401 - Unauthorized</h1>
        <p>Для доступа к этому ресурсу требуется аутентификация. 
        Пожалуйста, войдите в систему.</p>
    </body>
</html>
''', 401

@app.route("/402")
def payment_required():
    return '''
<!doctype html>
<html>
    <body>
        <h1>402 - Payment Required</h1>
        <p>Этот ресурс требует оплаты. Пожалуйста, произведите платеж, 
        чтобы продолжить.</p>
    </body>
</html>
''', 402

@app.route("/403")
def forbidden():
    return '''
<!doctype html>
<html>
    <body>
        <h1>403 - Forbidden</h1>
        <p>У вас нет прав доступа к этому ресурсу.</p>
    </body>
</html>
''', 403

@app.route("/405")
def method_not_allowed():
    return '''
<!doctype html>
<html>
    <body>
        <h1>405 - Method Not Allowed</h1>
        <p>Метод, использованный в запросе, не поддерживается 
        для этого ресурса.</p>
    </body>
</html>
''', 405

@app.route("/418")
def im_a_teapot():
    return '''
<!doctype html>
<html>
    <body>
        <h1>418 - I'm a teapot</h1>
        <p>Я — чайник. RFC 2324 гласит, что этот сервер не может заварить кофе, так как он является чайником.</p>
    </body>
</html>
''', 418

@app.errorhandler(404)
def page_not_found(e):
    image_path = url_for('static', filename='delulu.jpg')
    return '''
<!doctype html>
<html>
    <head>
        <title>404 - Страница не найдена</title>
        <style>
            body {
                background-color: #f8f9fa;
                color: #333;
                font-family: Arial, sans-serif;
                text-align: center;
                padding: 50px;
            }
            h1 {
                font-size: 3em;
                margin-bottom: 20px;
                color: #ff6f61;
            }
            p {
                font-size: 1.2em;
                margin-bottom: 30px;
            }
            img {
                width: 300px;
                height: auto;
                margin-bottom: 30px;
            }
            a {
                text-decoration: none;
                color: #007bff;
                font-weight: bold;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <h1>404 - Страница потерялась</h1>
        <p>Извините, но мы не можем найти нужную вам страницу.</p>
        <img src="''' + image_path + '''" alt="404 - Not Found">
        <p>Попробуйте вернуться на <a href="/">главную страницу</a> 
        и продолжить навигацию оттуда.</p>
    </body>
</html>
''', 404

@app.errorhandler(500)
def internal_server_error(e):
    return '''
<!doctype html>
<html>
    <head>
        <title>Ошибка 500 - Внутренняя ошибка сервера</title>
    </head>
    <body>
        <h1>500 - Внутренняя ошибка сервера</h1>
        <p>На сервере произошла ошибка. Мы работаем над её 
        исправлением.</p>
        <p>Пожалуйста, вернитесь на <a href="/">главную страницу</a> 
        и попробуйте снова позже.</p>
    </body>
</html>
''', 500

# Обработчик, который вызывает ошибку на сервере
@app.route("/cause-error")
def cause_error():
    return 1 / 0  # Ошибка деления на ноль


@app.route("/custom")
def custom_page():
    # Путь к изображению в папке static
    image_path = url_for('static', filename='duolingo.jpg')
    
    # HTML-контент
    content = f"""
    <!doctype html>
    <html>
        <head>
            <title>Текстовая страница с изображением</title>
        </head>
        <body>
            <h1>Добро пожаловать на нашу страницу!</h1>
            <p>Этот сайт посвящен всему, что связано с программированием
             на Python. 
            Python — это один из самых популярных языков программирования, 
            который используется для создания веб-приложений, анализа 
            данных, автоматизации задач и многого другого.</p>
            
            <p>Flask — это микрофреймворк для веб-программирования на 
            Python. Flask обеспечивает минимальный каркас, что позволяет 
            разработчикам добавлять нужные компоненты самостоятельно, 
            а не следовать за предопределённой архитектурой.</p>
            
            <p>На этой странице мы можем обсудить преимущества 
            микрофреймворков. Они предоставляют свободу разработчику в 
            выборе библиотек и подходов, делая систему гибкой и 
            расширяемой.</p>
            
            <p>Для начала работы с Flask вам потребуется только 
            минимальная установка, а базовый "Hello World" сервер 
            может быть запущен в считанные минуты.</p>
            
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
