from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3
from functools import wraps

rgz = Blueprint('rgz', __name__, template_folder='templates', static_folder='static')

DATABASE = 'books.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def is_admin():
    return session.get('is_admin', False)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_admin():
            flash('Требуется авторизация администратора!')
            return redirect(url_for('rgz.books_list'))
        return f(*args, **kwargs)
    return decorated_function

@rgz.route('/')
def books_list():
    conn = get_db_connection()

    # Подсчёт общего количества книг
    total_books_query = "SELECT COUNT(*) as count FROM books"
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
        total_books_query += " WHERE " + " AND ".join(filters)

    total_books = conn.execute(total_books_query).fetchone()['count']

    # Параметры пагинации
    page = int(request.args.get('page', 1))  # Текущая страница, по умолчанию 1
    books_per_page = 20  # Ограничение на 20 книг
    total_pages = (total_books + books_per_page - 1) // books_per_page  # Общее количество страниц
    offset = (page - 1) * books_per_page

    # Запрос на выборку книг с учётом фильтров
    query = "SELECT * FROM books"
    if filters:
        query += " WHERE " + " AND ".join(filters)
    sort_by = request.args.get('sort_by', 'title')  # Сортировка по названию по умолчанию
    query += f" ORDER BY {sort_by} LIMIT {books_per_page} OFFSET {offset}"

    books = conn.execute(query).fetchall()
    conn.close()

    return render_template(
        'rgz/books_list.html',
        books=books,
        page=page,
        total_pages=total_pages,
        filters=request.args
    )


@rgz.route('/add', methods=['GET', 'POST'])
@admin_required
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        pages = request.form['pages']
        publisher = request.form['publisher']
        cover = request.form['cover']  # Получаем путь к обложке

        if not title or not author or not pages or not publisher or not cover:
            flash('Все поля обязательны для заполнения!')
            return redirect(url_for('rgz.add_book'))

        try:
            pages = int(pages)
        except ValueError:
            flash('Количество страниц должно быть числом!')
            return redirect(url_for('rgz.add_book'))

        conn = get_db_connection()
        conn.execute('INSERT INTO books (title, author, pages, publisher, cover) VALUES (?, ?, ?, ?, ?)',
                     (title, author, pages, publisher, cover))
        conn.commit()
        conn.close()

        flash('Книга успешно добавлена!')
        return redirect(url_for('rgz.books_list'))

    return render_template('rgz/add_book.html')

@rgz.route('/edit/<int:book_id>', methods=['GET', 'POST'])
@admin_required
def edit_book(book_id):
    conn = get_db_connection()
    book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()

    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        pages = request.form['pages']
        publisher = request.form['publisher']

        if not title or not author or not pages or not publisher:
            flash('Все поля обязательны для заполнения!')
            return redirect(url_for('rgz.edit_book', book_id=book_id))

        try:
            pages = int(pages)
        except ValueError:
            flash('Количество страниц должно быть числом!')
            return redirect(url_for('rgz.edit_book', book_id=book_id))

        conn.execute('UPDATE books SET title = ?, author = ?, pages = ?, publisher = ? WHERE id = ?',
                     (title, author, pages, publisher, book_id))
        conn.commit()
        conn.close()

        flash('Книга успешно обновлена!')
        return redirect(url_for('rgz.books_list'))

    conn.close()
    return render_template('rgz/edit_book.html', book=book)

@rgz.route('/delete/<int:book_id>', methods=['POST'])
@admin_required
def delete_book(book_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM books WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()
    flash('Книга успешно удалена!')
    return redirect(url_for('rgz.books_list'))

@rgz.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == 'admin123':
            session['is_admin'] = True
            flash('Вы успешно вошли как администратор!')
            return redirect(url_for('rgz.books_list'))
        else:
            flash('Неверный логин или пароль!')
    return render_template('rgz/admin_login.html')

@rgz.route('/admin-logout')
def admin_logout():
    session.pop('is_admin', None)
    flash('Вы вышли из учётной записи администратора.')
    return redirect(url_for('rgz.books_list'))

@rgz.route('/book/<int:book_id>')
def book_details(book_id):
    conn = get_db_connection()
    book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
    conn.close()
    if book is None:
        flash('Книга не найдена.')
        return redirect(url_for('rgz.books_list'))
    return render_template('rgz/book_details.html', book=book)
