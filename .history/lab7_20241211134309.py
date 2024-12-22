from flask import Blueprint, render_template, jsonify, abort, request

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
    # Проверяем, находится ли ID в допустимом диапазоне
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
        abort(404, description="Фильм с таким ID не найден")

@lab7.route('/lab7/rest-api/films/<int:id>/', methods=['PUT'])
def put_film(id):
    # Проверяем, находится ли ID в допустимом диапазоне
    if 0 <= id < len(films):
        # Получаем данные из тела запроса в формате JSON
        film = request.get_json()

        # Проверяем, содержит ли тело запроса все необходимые поля
        if not film or not all(key in film for key in ["title", "title_ru", "year", "description"]):
            abort(400, description="Неполные данные фильма. Ожидаются: title, title_ru, year, description")

        # Обновляем данные фильма
        films[id] = film
        return jsonify(films[id])  # Возвращаем обновленный фильм
    else:
        # Если ID некорректен, возвращаем ошибку 404
        abort(404, description="Фильм с таким ID не найден")
