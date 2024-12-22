from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3
from functools import wraps
import logging

logging.basicConfig(level=logging.DEBUG)

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
            return redirect(url_for('rgz.admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@rgz.route('/')
def books_list():
    conn = get_db_connection()

    filters = []
    if not session.get('is_admin'):  # Для обычных пользователей
        filters.append("is_deleted = 0")

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

    # Подсчёт общего числа книг
    total_books_query = "SELECT COUNT(*) as count FROM books"
    if filters:
        total_books_query += " WHERE " + " AND ".join(filters)
    logging.debug(f"Total books query: {total_books_query}")

    total_books = conn.execute(total_books_query).fetchone()['count']

    # Пагинация
    page = int(request.args.get('page', 1))
    books_per_page = 20
    total_pages = (total_books + books_per_page - 1) // books_per_page
    offset = (page - 1) * books_per_page

    # Получение книг
    query = "SELECT * FROM books"
    if filters:
        query += " WHERE " + " AND ".join(filters)
    sort_by = request.args.get('sort_by', 'title')
    query += f" ORDER BY {sort_by} LIMIT {books_per_page} OFFSET {offset}"

    logging.debug(f"Filters: {filters}")
    logging.debug(f"Final query: {query}")

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

    if not book:
        flash('Книга не найдена.')
        return redirect(url_for('rgz.books_list'))

    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        pages = request.form['pages']
        publisher = request.form['publisher']
        cover = request.form['cover']

        if not title or not author or not pages or not publisher or not cover:
            flash('Все поля обязательны для заполнения!')
            return redirect(url_for('rgz.edit_book', book_id=book_id))

        try:
            pages = int(pages)
        except ValueError:
            flash('Количество страниц должно быть числом!')
            return redirect(url_for('rgz.edit_book', book_id=book_id))

        conn.execute('UPDATE books SET title = ?, author = ?, pages = ?, publisher = ?, cover = ? WHERE id = ?',
                     (title, author, pages, publisher, cover, book_id))
        conn.commit()
        conn.close()

        flash('Книга успешно обновлена!')
        return redirect(url_for('rgz.books_list'))

    conn.close()
    return render_template('rgz/edit_book.html', book=book)

@rgz.route('/delete/<int:book_id>', methods=['POST'])
@admin_required
def delete_book(book_id):
    logging.debug(f"Attempting to delete book with ID: {book_id}")

    conn = get_db_connection()

    # Проверяем, существует ли книга
    book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
    if not book:
        logging.debug(f"Book with ID {book_id} not found in the database.")
        flash('Книга не найдена.')
        logging.debug(f"Book with ID {book_id} not found in the database.")
        conn.close()
        return redirect(url_for('rgz.books_list'))

    # Помечаем книгу как удалённую
    conn.execute('UPDATE books SET is_deleted = 1 WHERE id = ?', (book_id,))
    conn.commit()
    logging.debug(f"Book with ID {book_id} successfully marked as deleted.")
    conn.close()

    flash('Книга успешно помечена как удалённая!')
    return redirect('rgz/rgz/books_list')


@rgz.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Логин и пароль администратора
        if username == 'admin' and password == 'admin123':
            session['is_admin'] = True
            flash('Вы успешно вошли как администратор!')
            return redirect('rgz/rgz/books_list')
        else:
            flash('Неверный логин или пароль!')
    return render_template('rgz/admin_login.html')

@rgz.route('/admin-logout')
def admin_logout():
    conn = get_db_connection()
    conn.execute('UPDATE books SET is_deleted = 0 WHERE is_deleted = 1')
    conn.commit()
    conn.close()

    session.pop('is_admin', None)
    flash('Вы вышли из учётной записи администратора. Удалённые книги восстановлены.')
    return redirect('rgz/rgz/books_list') 


