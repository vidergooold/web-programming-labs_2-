from flask import Blueprint, render_template

lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/')
def lab():
    # Рендерим шаблон lab3.html
    return render_template('lab3/lab3.html')
