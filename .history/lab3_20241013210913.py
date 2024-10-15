from flask import Blueprint, render_template, request, make_response
lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response('установка cookie', 200)
    resp.set_cookie('')