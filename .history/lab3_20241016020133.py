from flask import Blueprint, make_response, redirect, render_template, request

lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name')
    name_color = request.cookies.get('name_color')
    return render_template('lab3/lab3.html', name=name, name_color=name_color)

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

@lab3.route('/lab3/settings', methods=['POST', 'GET'])
def settings():
    color = request.args.get('color')
    bg_color = request.args.get('bg_color')
    font_size = request.args.get('font_size')
    bold = request.args.get('bold')

    # Создаем ответ с редиректом после установки куков
    resp = make_response(redirect('/lab3/settings'))
    
    # Устанавливаем куки, если параметры переданы
    if color:
        resp.set_cookie('color', color)
    if bg_color:
        resp.set_cookie('bg_color', bg_color)
    if font_size:
        resp.set_cookie('font_size', font_size)
    if bold == 'on':
        resp.set_cookie('bold', 'on')
    else:
        # Удаляем куки жирного шрифта, если опция не выбрана
        resp.set_cookie('bold', '', max_age=0)

    return resp

@lab3.route('/lab3/settings', methods=['GET'])
def show_settings():
    color = request.cookies.get('color', '#000000')
    bg_color = request.cookies.get('bg_color', '#ffffff')
    font_size = request.cookies.get('font_size', '16')
    bold = request.cookies.get('bold', '')

    return render_template('lab3/settings.html', color=color, bg_color=bg_color, font_size=font_size, bold=bold)

