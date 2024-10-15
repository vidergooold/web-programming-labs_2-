from flask import Blueprint, render_template, request
lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/cookie')
def lab():
    name = request.cookies.get('name')
    return render_template('lab3/lab3.html', )
