from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3

rgz = Blueprint('rgz', __name__, template_folder='templates', static_folder='static')

DATABASE = 'books.db'  # Имя файла базы данных SQLite

# Функция для подключения к базе данных
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Главная страница RGZ - список книг с фильтрами и пагинацией
@rgz.route('/')
def books_list():
    conn = get_db_connection()
    query = "SELECT * FROM books"
    
    # Фильтры
    filters = []
    title = request.args.get('title')
    author = request.args.get('author')
    min_pages = request.args.get('min_pages')
    max_pages = request.args.get('max_pages')

    if title:
        filters.append(f"title LIKE '%{title}%'")
    if author:
        filters.append(f"author LIKE '%{author}%'")
    if min_pages:
        filters.append(f"pages >= {min_pages}")
    if max_pages:
        filters.append(f"pages <= {max_pages}")

    if filters:
        query += " WHERE " + " AND ".join(filters)

    # Сортировка
    sort_by = request.args.get('sort_by', 'title')
    query += f" ORDER BY {sort_by}"

    # Пагинация
    page = int(request.args.get('page', 1))
    books_per_page = 20
    offset = (page - 1) * books_per_page
    query += f" LIMIT {books_per_page} OFFSET {offset}"

    books = conn.execute(query).fetchall()
    conn.close()

    return render_template('rgz/books_list.html', books=books, page=page)

# Страница для администратора - добавление, редактирование, удаление книг
@rgz.route('/admin')
def admin_dashboard():
    return "Здесь будет панель администратора"

# Добавление книги
@rgz.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        # Логика добавления книги
        pass
    return render_template('rgz/add_book.html')
