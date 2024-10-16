from flask import Blueprint, redirect, url_for, render_template, request, abort
lab2 = Blueprint('lab2', __name__)

#routes for lab2

# Обработчик для ошибки 400
@lab2.route("/400")
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
@lab2.route("/401")
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
@lab2.route("/402")
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
@lab2.route("/403")
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
@lab2.route("/405")
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
@lab2.route("/418")
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

# Обработчик, который вызывает ошибку на сервере
@lab2.route("/cause-error")
def cause_error():
    return 1 / 0  # Ошибка деления на ноль

# Маршрут для лабораторной работы 2 с фавиконкой
@lab2.route('/', strict_slashes=False)
def lab_2():
    css_path = url_for('static', filename='main.css')
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
            <li><a href="/lab2/filter">Фильтры</a></li>
            <li><a href="/lab2/example">Пример</a></li>
            <li><a href="/lab2/berries">Ягоды</a></li>
            <li><a href="/lab2/books">Книги</a></li>
            <li><a href="/lab2/flowers">Список цветов</a></li>
        </ul>
    </body>
</html>
'''

# Маршруты для добавления и вывода цветов
@lab2.route('/a')
def a():
    return 'без слэша'

@lab2.route('/a/')
def a2():
    return 'со слэшем'

flower_list = [
    {"name": "Роза", "price": 300},
    {"name": "Тюльпан", "price": 310},
    {"name": "Ромашка", "price": 320},
    {"name": "Подсолнух", "price": 330},
    {"name": "Лилия", "price": 340}
]

@lab2.route('/add_flower', methods=['GET'])
def add_flower():
    name = request.args.get('name')
    price = request.args.get('price')

    if not name or not price:
        return "Неверные данные: необходимо указать название цветка и его цену", 400

    # Добавляем новый цветок в список
    flower_list.append({"name": name, "price": int(price)})

    # Перенаправляем на страницу с цветами
    return redirect(url_for('lab2.show_flowers'))

@lab2.route('/flowers')
def show_flowers():
    lab_num = 2  # Номер лабораторной работы
    return render_template('lab2/flowers.html', flower_list=flower_list, lab_num=lab_num)

@lab2.route('/del_flower/<int:flower_id>')
def delete_flower(flower_id):
    if 0 <= flower_id < len(flower_list):
        del flower_list[flower_id]
    else:
        return "Такого цветка нет", 404

    # После удаления цветка возвращаемся на страницу со списком цветов
    return redirect(url_for('lab2.show_flowers'))

@lab2.route('/clear_flowers')
def clear_flowers():
    global flower_list
    flower_list.clear()

    # Возвращаемся на страницу со списком цветов после очистки
    return redirect(url_for('lab2.show_flowers'))

# Маршрут для примера
@lab2.route('/example')
def example():
    name = 'Видергольд Ирина'
    lab_num1 = '2'
    lab_num2 = '2'
    group = 'ФБИ-22'
    number = '3'
    fruits = [
        {'name': 'lab2les', 'price': 100},
        {'name': 'pears', 'price': 150}, 
        {'name': 'oranges', 'price': 90}, 
        {'name': 'mangos', 'price': 120}, 
        {'name': 'cherries', 'price': 200}
    ]
    return render_template('lab2/example.html', 
                           name=name, lab_num1=lab_num1, lab_num2=lab_num2, 
                           group=group, number=number, fruits=fruits)

# Фильтр с фавиконкой
@lab2.route('/filter')
def filter():
    phrase = "0 <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('lab2/filter.html', phrase=phrase)

# Основной маршрут для вычислений с двумя числами
@lab2.route('/calc/<int:a>/<int:b>')
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
@lab2.route('/calc/', strict_slashes=False)
def default_calc():
    return redirect(url_for('lab2.calc', a=1, b=1))

# Перенаправление с /lab2/calc/<int:a> на /lab2/calc/a/1
@lab2.route('/calc/<int:a>', strict_slashes=False)
def calc_with_one(a):
    return redirect(url_for('lab2.calc', a=a, b=1))

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
@lab2.route('/books')
def show_books():
    favicon_path = url_for('static', filename='favicon.ico')
    return render_template('lab2/books.html', books=books, favicon_path=favicon_path)

# Список ягод с информацией: название, описание, имя файла картинки
berries = [
    {"name": "Клубника", "description": "Сочная красная ягода, богата витаминами.", "image": "strawberry.jpg"},
    {"name": "Голубика", "description": "Мелкие синие ягоды, отлично подходят для десертов.", "image": "blueberry.jpg"},
    {"name": "Малина", "description": "Сладкая и ароматная ягода с лёгкой кислинкой.", "image": "raspberry.jpg"},
    {"name": "Ежевика", "description": "Тёмные, почти чёрные ягоды с насыщенным вкусом.", "image": "blackberry.jpg"},
    {"name": "Вишня", "description": "Кисло-сладкая ягода, популярная в выпечке.", "image": "cherry.jpg"}
]

@lab2.route('/berries')
def show_berries():
    favicon_path = url_for('static', filename='favicon.ico')
    return render_template('berries.html', berries=berries, favicon_path=favicon_path)
