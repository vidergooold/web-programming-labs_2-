from flask import Blueprint, make_response, redirect, render_template, request

lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/')
def lab():
    # Получаем значение куки 'name', если кука отсутствует, используется None
    name = request.cookies.get('name')
    return render_template('lab3/lab3.html', name=name)

@lab3.route('/cookie')
def cookie():
    # Создаем ответ с редиректом на /lab3/
    resp = make_response(redirect('/lab3/lab3'))
    
    # Устанавливаем куки с большим временем жизни (60 секунд)
    resp.set_cookie('name', 'Alex', max_age=5) 
    resp.set_cookie('age', '20')
    resp.set_cookie('color', 'magenta')
    
    return resp
