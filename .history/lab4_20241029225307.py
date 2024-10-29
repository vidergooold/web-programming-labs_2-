from flask import Blueprint, render_template, request

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

