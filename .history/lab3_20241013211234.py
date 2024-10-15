from flask import Blueprint, render_template, request, make_response
lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('color', 'magenta')
    return resp