from flask import Blueprint, render_template, request

lab4 = Blueprint('lab4', __name__)

@lab3.route('/lab4/')
def lab():
    name = request.cookies.get('name')
    name_color = request.cookies.get('name_color')
    age = request.cookies.get('age')  # Добавляем получение возраста
    return render_template('lab3/lab3.html', name=name, name_color=name_color, age=age)
