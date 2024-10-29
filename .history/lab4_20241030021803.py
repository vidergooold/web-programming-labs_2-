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
