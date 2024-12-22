from flask import Blueprint, render_template, jsonify, abort, request
from datetime import datetime

lab7 = Blueprint('lab7', __name__)

# База данных в виде списка для упрощения
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

def validate_film_data(film):
    """Валидация данных фильма"""
    if not film:
        abort(400, description="Данные фильма отсутствуют")
    
    if not film.get("title") and not film.get("title_ru"):
        abort(400, description="Должно быть задано хотя бы одно название (на русском или оригинальное)")
    
    if not film.get("title_ru"):
        abort(400, description="Русское название обязательно")
    
    if not 1895 <= film.get("year", 0) <= datetime.now().year:
        abort(400, description=f"Год выпуска должен быть в диапазоне от 1895 до {datetime.now().year}")
    
    if not film.get("description") or len(film["description"]) > 2000:
        abort(400, description="Описание должно быть заполнено и не более 2000 символов")
    
    # Если оригинальное название пустое, заполняем его русским названием
    if not film.get("title"):
        film["title"] = film["title_ru"]

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
    if 0 <= id < len(films):
        del films[id]
        return '', 204
    else:
        abort(404, description="Фильм с таким ID не найден")

@lab7.route('/lab7/rest-api/films/<int:id>/', methods=['PUT'])
def put_film(id):
    if 0 <= id < len(films):
        film = request.get_json()
        validate_film_data(film)
        films[id] = film
        return jsonify(films[id])
    else:
        abort(404, description="Фильм с таким ID не найден")

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()
    validate_film_data(film)
    films.append(film)
    return jsonify({"id": len(films) - 1}), 201

