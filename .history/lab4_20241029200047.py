from flask import Blueprint, render_template, request

lab4 = Blueprint('lab4', __name__)

@lab3.route('/lab4/')
def lab():
    return render_template('lab4/lab3.html', name=name, name_color=name_color, age=age)
