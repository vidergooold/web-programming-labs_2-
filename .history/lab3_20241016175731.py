from flask import Blueprint, make_response, redirect, render_template, request

lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name')
    name_color = request.cookies.get('name_color')
    age = request.cookies.get('age')  # Добавляем получение возраста
    return render_template('lab3/lab3.html', name=name, name_color=name_color, age=age)

@lab3.route('/cookie')
def cookie():
    resp = make_response(redirect('/lab3/lab3'))
    resp.set_cookie('name', 'Alex', max_age=5) 
    resp.set_cookie('age', '20')  # Устанавливаем возраст
    resp.set_cookie('name_color', 'magenta')
    return resp

@lab3.route('/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/lab3'))
    resp.delete_cookie('name') 
    resp.delete_cookie('age')  # Удаляем возраст
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

@lab3.route('/lab3/settings', methods=['GET''])
def settings():
    if request.method == 'POST':
        # Получаем выбранные настройки из формы
        color = request.form.get('color')
        background_color = request.form.get('background_color')
        font_size = request.form.get('font_size')
        font_style = request.form.get('font_style')

        # Устанавливаем куки с настройками и перенаправляем на эту же страницу
        resp = make_response(redirect('/lab3/settings.html'))
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
    return make_response(render_template('lab3/settings.html', color=color, background_color=background_color, font_size=font_size, font_style=font_style))

@lab3.route('/lab3/ticket_form', methods=['GET', 'POST'])
def ticket_form():
    if request.method == 'POST':
        fio = request.form.get('fio')
        shelf = request.form.get('shelf')
        bedding = 'bedding' in request.form
        baggage = 'baggage' in request.form
        age = int(request.form.get('age'))
        departure = request.form.get('departure')
        destination = request.form.get('destination')
        date = request.form.get('date')
        insurance = 'insurance' in request.form

        errors = {}

        if not fio:
            errors['fio'] = 'Заполните поле ФИО!'
        if not shelf:
            errors['shelf'] = 'Выберите полку!'
        if not departure:
            errors['departure'] = 'Заполните пункт выезда!'
        if not destination:
            errors['destination'] = 'Заполните пункт назначения!'
        if not date:
            errors['date'] = 'Выберите дату поездки!'
        if age < 1 or age > 120:
            errors['age'] = 'Возраст должен быть от 1 до 120 лет!'

        if errors:
            return render_template('lab3/ticket_form.html', errors=errors)

        # Расчет цены билета
        base_price = 700 if age < 18 else 1000
        if shelf in ['нижняя', 'нижняя боковая']:
            base_price += 100
        if bedding:
            base_price += 75
        if baggage:
            base_price += 250
        if insurance:
            base_price += 150

        return render_template('lab3/ticket.html', fio=fio, shelf=shelf, bedding=bedding, baggage=baggage, age=age, departure=departure, destination=destination, date=date, insurance=insurance, price=base_price)

    return render_template('lab3/ticket_form.html')

products = [
    {"name": "Смартфон Apple iPhone 13", "price": 79990, "brand": "Apple", "color": "синий"},
    {"name": "Смартфон Samsung Galaxy S21", "price": 64990, "brand": "Samsung", "color": "черный"},
    {"name": "Смартфон Xiaomi Mi 11", "price": 49990, "brand": "Xiaomi", "color": "белый"},
    {"name": "Смартфон Huawei P40 Pro", "price": 59990, "brand": "Huawei", "color": "серебристый"},
    {"name": "Смартфон OnePlus 9 Pro", "price": 69990, "brand": "OnePlus", "color": "зеленый"},
    {"name": "Смартфон Google Pixel 6", "price": 54990, "brand": "Google", "color": "серый"},
    {"name": "Смартфон Sony Xperia 1 III", "price": 89990, "brand": "Sony", "color": "черный"},
    {"name": "Смартфон Motorola Edge 20", "price": 39990, "brand": "Motorola", "color": "синий"},
    {"name": "Смартфон Oppo Reno 6", "price": 44990, "brand": "Oppo", "color": "золотой"},
    {"name": "Смартфон Vivo X60", "price": 47990, "brand": "Vivo", "color": "черный"},
    {"name": "Смартфон Realme GT", "price": 34990, "brand": "Realme", "color": "желтый"},
    {"name": "Смартфон Nokia 8.3", "price": 32990, "brand": "Nokia", "color": "синий"},
    {"name": "Смартфон LG Velvet", "price": 29990, "brand": "LG", "color": "белый"},
    {"name": "Смартфон Asus ROG Phone 5", "price": 59990, "brand": "Asus", "color": "черный"},
    {"name": "Смартфон ZTE Axon 30", "price": 37990, "brand": "ZTE", "color": "синий"},
    {"name": "Смартфон Lenovo Legion Duel 2", "price": 54990, "brand": "Lenovo", "color": "серый"},
    {"name": "Смартфон TCL 20 Pro 5G", "price": 42990, "brand": "TCL", "color": "синий"},
    {"name": "Смартфон Alcatel 3X", "price": 14990, "brand": "Alcatel", "color": "черный"},
    {"name": "Смартфон Honor 50", "price": 39990, "brand": "Honor", "color": "синий"},
    {"name": "Смартфон Tecno Camon 17", "price": 12990, "brand": "Tecno", "color": "синий"},
]

@lab3.route('/lab3/search_form', methods=['GET', 'POST'])
def search_form():
    if request.method == 'POST':
        min_price = float(request.form.get('min_price'))
        max_price = float(request.form.get('max_price'))

        filtered_products = [product for product in products if min_price <= product['price'] <= max_price]

        return render_template('lab3/search_results.html', products=filtered_products)

    return render_template('lab3/search_form.html')

@lab3.route('/lab3/clear_cookies')
def clear_cookies():
    resp = make_response(redirect('/lab3/settings'))
    resp.delete_cookie('color')
    resp.delete_cookie('background_color')
    resp.delete_cookie('font_size')
    resp.delete_cookie('font_style')
    return resp
