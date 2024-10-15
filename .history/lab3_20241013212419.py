from flask import Blueprint, make_response, redirect

lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/cookie')
def cookie():
    # Создаем ответ с редиректом на /lab3/
    resp = make_response(redirect('/lab3/'))
    
    # Устанавливаем куки
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('color', 'magenta')
    
    # Возвращаем ответ
    return resp
