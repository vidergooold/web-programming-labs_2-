from flask import Blueprint, render_template, jsonify, abort, request
import sqlite3
import hashlib

lab7 = Blueprint('lab7', __name__)
DB_PATH = 'laba.db'  # Путь к файлу базы данных

# Функция для подключения к базе данных
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Удобный формат для работы с результатами
    return conn

@lab7.route('/')
def lab():
    return render_template('lab7/lab7.html')

@lab7.route('/rest-api/films/', methods=['GET'])
def get_films():
    conn = get_db_connection()
    films = conn.execute('SELECT * FROM films').fetchall()
    conn.close()
    return jsonify([dict(film) for film in films])

@lab7.route('/rest-api/films/<int:id>/', methods=['GET'])
def get_film(id):
    conn = get_db_connection()
    film = conn.execute('SELECT * FROM films WHERE id = ?', (id,)).fetchone()
    conn.close()
    if film is None:
        abort(404, description="Фильм с таким ID не найден")
    return jsonify(dict(film))

@lab7.route('/rest-api/films/<int:id>/', methods=['DELETE'])
def del_film(id):
    conn = get_db_connection()
    film = conn.execute('SELECT * FROM films WHERE id = ?', (id,)).fetchone()
    if film is None:
        conn.close()
        abort(404, description="Фильм с таким ID не найден")
    conn.execute('DELETE FROM films WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return '', 204

@lab7.route('/rest-api/films/<int:id>/', methods=['PUT'])
def put_film(id):
    conn = get_db_connection()
    film = conn.execute('SELECT * FROM films WHERE id = ?', (id,)).fetchone()
    if film is None:
        conn.close()
        abort(404, description="Фильм с таким ID не найден")
    
    data = request.get_json()
    if not data:
        abort(400, description="Данные фильма отсутствуют")
    
    title = data.get('title', '').strip()
    title_ru = data.get('title_ru', '').strip()
    year = data.get('year', 0)
    description = data.get('description', '').strip()
    
    # Проверки данных
    if not title and not title_ru:
        abort(400, description="Название фильма (оригинальное или на русском) обязательно")
    if not title:
        title = title_ru
    if not title_ru:
        abort(400, description="Русское название фильма обязательно")
    if year < 1895 or year > 2024:
        abort(400, description="Год выпуска должен быть между 1895 и текущим годом")
    if not description or len(description) > 2000:
        abort(400, description="Описание должно быть непустым и не более 2000 символов")
    
    conn.execute(
        'UPDATE films SET title = ?, title_ru = ?, year = ?, description = ? WHERE id = ?',
        (title, title_ru, year, description, id)
    )
    conn.commit()
    conn.close()
    return jsonify(data)

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    data = request.get_json()
    if not data:
        abort(400, description="Данные фильма отсутствуют")
    
    title = data.get('title', '').strip()
    title_ru = data.get('title_ru', '').strip()
    year = data.get('year', 0)
    description = data.get('description', '').strip()
    
    # Проверки данных
    if not title and not title_ru:
        abort(400, description="Название фильма (оригинальное или на русском) обязательно")
    if not title:
        title = title_ru
    if not title_ru:
        abort(400, description="Русское название фильма обязательно")
    if year < 1895 or year > 2024:
        abort(400, description="Год выпуска должен быть между 1895 и текущим годом")
    if not description or len(description) > 2000:
        abort(400, description="Описание должно быть непустым и не более 2000 символов")
    
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO films (title, title_ru, year, description) VALUES (?, ?, ?, ?)',
        (title, title_ru, year, description)
    )
    conn.commit()
    new_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
    conn.close()
    return jsonify({"id": new_id}), 201
