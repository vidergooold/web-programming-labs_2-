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
    
    # Проверяем, были ли отправлены параметры
    user = request.args.get('user')
    if user == '':  # Проверяем, если поле имени пустое
        errors['user'] = 'Заполните поле!'

    age = request.args.get('age')
    if age == '':  # Проверяем, если поле возраста пустое
        errors['age'] = 'Заполните поле!'

    sex = request.args.get('sex')
    age = request.args.get('age')

    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)
