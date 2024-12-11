from flask import Blueprint, render_template, jsonify, abort

lab7 = Blueprint('lab7', __name__)

# Данные о фильмах
films = [
    {
        "title": "Interstellar",
        "title_ru": "Интерстеллар",
        "year": 2014,
        "description": "Когда засуха, пыльные бури и вымирание растений приводят человечество к продовольственному кризису..."
    },
    {
        "title": "The Shawshank Redemption",
        "title_ru": "Побег из Шоушенка",
        "year": 1994,
        "description": "Бухгалтер Энди Дюфрейн обвинён в убийстве собственной жены и её любовника..."
    },
    {
        "title": "The Green Mile",
        "title_ru": "Зеленая миля",
        "year": 1999,
        "description": "Пол Эджкомб — начальник блока смертников в тюрьме 'Холодная гора'..."
    }
]

@lab7.route('/')
def lab():
    return render_template('lab7/lab7.html')

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return jsonify(films)

@lab7.route('/lab7/rest-api/films/<int:id>/', methods=['GET'])
def get_film(id):
    if 0 <= id < len(films):
        return jsonify(films[id])
    else:
        abort(404, description="Фильм с таким ID не найден")

@lab7.route('/lab7/rest-api/films/<int:id>/', methods=['DELETE'])
def del_film(id):
    # Проверяем, находится ли ID в допустимом диапазоне
    if 0 <= id < len(films):
        del films[id]  # Удаляем фильм с заданным ID
        return '', 204  # Возвращаем пустой ответ с кодом 204 No Content
    else:
        # Если ID не корректен, возвращаем ошибку 404
        abort(404, description="Фильм с таким ID не найден")


