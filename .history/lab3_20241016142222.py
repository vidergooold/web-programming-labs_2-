from flask import Blueprint, make_response, redirect, render_template, request

lab3 = Blueprint('lab3', __name__)

from flask import Flask, render_template, request, make_response

app = Flask(__name__)

@app.route('/lab3/', methods=['GET', 'POST'])
def lab3():
    # Получение данных из формы или cookies
    name = request.cookies.get('name')
    age = request.cookies.get('age')

    # Если имя или возраст не заданы, подставляем значения по умолчанию
    if not name:
        name = "аноним"  # Используем "аноним" вместо None
    if not age:
        age = "неизвестен"  # Используем "неизвестен" для возраста

    name_color = request.cookies.get('name_color', 'black')  # Цвет имени по умолчанию

    return render_template('lab3.html', name=name, age=age, name_color=name_color)

@app.route('/lab3/settings', methods=['POST'])
def save_settings():
    # Получение данных из формы
    name = request.form.get('name', 'аноним')
    age = request.form.get('age', 'неизвестен')
    name_color = request.form.get('name_color', 'black')

    # Создание ответа с установкой cookies
    resp = make_response(render_template('lab3.html', name=name, age=age, name_color=name_color))
    resp.set_cookie('name', name)
    resp.set_cookie('age', age)
    resp.set_cookie('name_color', name_color)

    return resp


@lab3.route('/cookie')
def cookie():
    resp = make_response(redirect('/lab3/lab3'))
    resp.set_cookie('name', 'Alex', max_age=5) 
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp

@lab3.route('/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/lab3'))
    resp.delete_cookie('name') 
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp

@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'
    
    age = request.args.get('age')
    if age == '':
        errors['age'] = 'Заполните поле!'

    age = request.args.get('age')
    sex = request.args.get('sex')
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)

@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')

@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    # Пусть кофе стоит 120 рублей, черный чай - 80, зеленый - 70 рублей
    if drink == 'coffee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    # Добавка молока удоражает напиток на 30 рублей, а сахара - на 10
    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10

    return render_template('lab3/pay.html', price=price)

@lab3.route('/lab3/success')
def success():
    # Получаем сумму из запроса (она была рассчитана на странице оплаты)
    price = request.args.get('price')
    return render_template('lab3/success.html', price=price)

@lab3.route('/lab3/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        # Получаем выбранные настройки из формы
        color = request.form.get('color')
        background_color = request.form.get('background_color')
        font_size = request.form.get('font_size')
        font_style = request.form.get('font_style')

        # Устанавливаем куки с настройками и перенаправляем на эту же страницу
        resp = make_response(redirect('/lab3/settings'))
        if color:
            resp.set_cookie('color', color)
        if background_color:
            resp.set_cookie('background_color', background_color)
        if font_size:
            resp.set_cookie('font_size', font_size)
        if font_style:
            resp.set_cookie('font_style', font_style)
        return resp

    # Получаем настройки из куки, если они есть
    color = request.cookies.get('color')
    background_color = request.cookies.get('background_color')
    font_size = request.cookies.get('font_size')
    font_style = request.cookies.get('font_style')

    # Рендерим страницу с текущими настройками из куки
    return make_response(render_template('/lab3/settings.html', color=color, background_color=background_color, font_size=font_size, font_style=font_style))

