from flask import Blueprint, render_template, request, redirect, session

lab4 = Blueprint('lab4', __name__)

@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')

@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')

@lab4.route('/lab4/div', methods=['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error='Оба поля должны быть заполнены!')

    try:
        x1 = int(x1)
        x2 = int(x2)
        if x2 == 0:
            raise ValueError("Деление на ноль")
        result = x1 / x2
        return render_template('lab4/div.html', x1=x1, x2=x2, result=result)
    except ValueError:
        return render_template('lab4/div.html', error='Некорректный ввод или деление на ноль!')

@lab4.route('/lab4/sum-form')
def sum_form():
    return render_template('lab4/sum-form.html')

@lab4.route('/lab4/sum', methods=['POST'])
def summation():
    x1 = request.form.get('x1') or 0
    x2 = request.form.get('x2') or 0
    x1 = int(x1)
    x2 = int(x2)
    result = x1 + x2
    return render_template('lab4/sum.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/multiply-form')
def multiply_form():
    return render_template('lab4/multiply-form.html')

@lab4.route('/lab4/multiply', methods=['POST'])
def multiplication():
    x1 = request.form.get('x1') or 1
    x2 = request.form.get('x2') or 1
    x1 = int(x1)
    x2 = int(x2)
    result = x1 * x2
    return render_template('lab4/multiply.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/subtract-form')
def subtract_form():
    return render_template('lab4/subtract-form.html')

@lab4.route('/lab4/subtract', methods=['POST'])
def subtraction():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/subtract.html', error='Оба поля должны быть заполнены!')

    x1 = int(x1)
    x2 = int(x2)
    result = x1 - x2
    return render_template('lab4/subtract.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/power-form')
def power_form():
    return render_template('lab4/power-form.html')

@lab4.route('/lab4/power', methods=['POST'])
def power():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '' or (int(x1) == 0 and int(x2) == 0):
        return render_template('lab4/power.html', error='Поля не должны быть пустыми, и оба числа не должны быть равны нулю!')

    x1 = int(x1)
    x2 = int(x2)
    result = x1 ** x2
    return render_template('lab4/power.html', x1=x1, x2=x2, result=result)

tree_count = 0

@lab4.route('/lab4/tree', methods=['GET', 'POST'])
def tree():
    global tree_count
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count)

    operation = request.form.get('operation')

    if operation == 'cut' and tree_count > 0:
        tree_count -= 1
    elif operation == 'plant' and tree_count < 10:
        tree_count += 1

    return redirect('/lab4/lab4/tree')

users = [
    {'login': 'alex', 'password': '123', 'name': 'Александр Иванов', 'gender': 'male'},
    {'login': 'bob', 'password': '555', 'name': 'Боб Смит', 'gender': 'male'},
    {'login': 'alice', 'password': 'qwerty', 'name': 'Алиса Петрова', 'gender': 'female'},
    {'login': 'charlie', 'password': 'zxcvbn', 'name': 'Чарли Браун', 'gender': 'male'}
]

@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            user = next((u for u in users if u['login'] == session['login']), None)
            if user:
                return render_template('lab4/login.html', authorized=True, login=user['login'], name=user['name'])
        return render_template('lab4/login.html', authorized=False)

    login = request.form.get('login')
    password = request.form.get('password')

    # Проверка на пустые значения
    if not login:
        error = 'Не введён логин'
        return render_template('lab4/login.html', error=error, authorized=False, login=login)
    if not password:
        error = 'Не введён пароль'
        return render_template('lab4/login.html', error=error, authorized=False, login=login)

    # Проверка логина и пароля в списке пользователей
    for user in users:
        if login == user['login'] and password == user['password']:
            session['login'] = login
            return redirect('/lab4/lab4/login')

    # Если логин и пароль не совпали
    error = 'Неверные логин и/или пароль'
    return render_template('lab4/login.html', error=error, authorized=False, login=login)

@lab4.route('/lab4/logout', methods=['POST'])
def logout():
    session.pop('login', None)  # Удаляем логин из сессии
    return redirect('/lab4/lab4/login')

@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    temperature = request.form.get('temperature')

    # Проверка, задана ли температура
    if temperature is None or temperature == '':
        error = 'Ошибка: не задана температура'
        return render_template('lab4/fridge.html', error=error)

    try:
        temp = float(temperature)
    except ValueError:
        error = 'Ошибка: некорректное значение температуры'
        return render_template('lab4/fridge.html', error=error)

    # Проверка температуры и определение состояния
    if temp < -12:
        message = 'Не удалось установить температуру — слишком низкое значение'
        snowflakes = 0
    elif temp > -1:
        message = 'Не удалось установить температуру — слишком высокое значение'
        snowflakes = 0
    elif -12 <= temp <= -9:
        message = f'Установлена температура: {temp}°С'
        snowflakes = 3
    elif -8 <= temp <= -5:
        message = f'Установлена температура: {temp}°С'
        snowflakes = 2
    elif -4 <= temp <= -1:
        message = f'Установлена температура: {temp}°С'
        snowflakes = 1

    return render_template('lab4/fridge.html', message=message, snowflakes=snowflakes)

@lab4.route('/lab4/grain_order', methods=['GET', 'POST'])
def grain_order():
    prices = {
        'ячмень': 12345,
        'овёс': 8522,
        'пшеница': 8722,
        'рожь': 14111
    }
    discount_threshold = 50
    discount_rate = 0.10
    max_order = 500

    if request.method == 'POST':
        grain = request.form.get('grain')
        weight = request.form.get('weight')

        if not grain or grain not in prices:
            error = "Ошибка: неверный выбор зерна"
            return render_template('lab4/grain_order.html', error=error)

        if not weight or weight == '':
            error = "Ошибка: не указан вес"
            return render_template('lab4/grain_order.html', error=error)

        try:
            weight = float(weight)
        except ValueError:
            error = "Ошибка: вес должен быть числом"
            return render_template('lab4/grain_order.html', error=error)

        if weight <= 0:
            error = "Ошибка: вес должен быть больше нуля"
            return render_template('lab4/grain_order.html', error=error)

        if weight > max_order:
            error = "Ошибка: такого объёма сейчас нет в наличии"
            return render_template('lab4/grain_order.html', error=error)

        price_per_ton = prices[grain]
        total_price = weight * price_per_ton
        discount_message = None

        # Применяем скидку, если вес превышает порог
        if weight > discount_threshold:
            discount = total_price * discount_rate
            total_price -= discount
            discount_message = f"Применена скидка за большой объём: {discount_rate * 100}% (скидка: {round(discount, 2)} руб)"

        message = f"Заказ успешно сформирован. Вы заказали {grain}. Вес: {weight} т. Сумма к оплате: {round(total_price, 2)} руб."

        return render_template('lab4/grain_order.html', message=message, discount_message=discount_message)

    return render_template('lab4/grain_order.html')

@lab4.route('/lab4/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        name = request.form.get('name')
        gender = request.form.get('gender')

        # Проверка на пустые значения
        if not login or not password or not name:
            error = 'Все поля должны быть заполнены'
            return render_template('lab4/register.html', error=error)

        # Проверка, существует ли логин
        if any(user['login'] == login for user in users):
            error = 'Пользователь с таким логином уже существует'
            return render_template('lab4/register.html', error=error)

        # Добавляем нового пользователя
        users.append({'login': login, 'password': password, 'name': name, 'gender': gender})
        success_message = 'Регистрация прошла успешно'
        return render_template('lab4/register.html', success_message=success_message)

    return render_template('lab4/register.html')

@lab4.route('/lab4/users', methods=['GET', 'POST'])
def users_list():
    if 'login' not in session:
        return redirect('/lab4/lab4/login')
    
    current_user = next((user for user in users if user['login'] == session['login']), None)

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'delete':
            users.remove(current_user)
            session.pop('login', None)
            return redirect('/lab4/lab4/login')
        elif action == 'edit':
            new_name = request.form.get('name')
            new_password = request.form.get('password')
            if new_name:
                current_user['name'] = new_name
            if new_password:
                current_user['password'] = new_password
            success_message = 'Данные успешно обновлены'
            return render_template('lab4/users.html', users=users, success_message=success_message)
    
    return render_template('lab4/users.html', users=users)
