from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3
from functools import wraps
import bcrypt

rgz = Blueprint('rgz', __name__)

DATABASE = 'books.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not session.get('is_admin'):
            flash("Требуются права администратора!")
            return redirect(url_for('rgz.login'))
        return func(*args, **kwargs)
    return decorated_view

@rgz.route('/')
def books_list():
    conn = get_db_connection()

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

    query = "SELECT * FROM books"
    if filters:
        query += " WHERE " + " AND ".join(filters)
    query += " ORDER BY title LIMIT 20"

    books = conn.execute(query).fetchall()
    conn.close()

    return render_template('rgz/books_list.html', books=books)

@rgz.route('/add', methods=['GET', 'POST'])
@admin_required
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        pages = request.form['pages']
        publisher = request.form['publisher']
        cover = request.form['cover']

        if not title or not author or not pages or not publisher:
            flash('Все поля обязательны для заполнения!')
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
        flash('Книга не найдена!')
        return redirect(url_for('rgz.books_list'))

    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        pages = request.form['pages']
        publisher = request.form['publisher']
        cover = request.form['cover']

        conn.execute('UPDATE books SET title = ?, author = ?, pages = ?, publisher = ?, cover = ? WHERE id = ?',
                     (title, author, pages, publisher, cover, book_id))
        conn.commit()
        conn.close()

        flash('Книга успешно обновлена!')
        return redirect(url_for('rgz.books_list'))

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

@rgz.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            session['user_id'] = user['id']
            session['is_admin'] = user['is_admin']
            flash('Успешный вход!')
            return redirect(url_for('rgz.books_list'))
        else:
            flash('Неверный логин или пароль.')

    return render_template('rgz/login.html')

@rgz.route('/logout')
def logout():
    session.clear()
    flash('Вы вышли из системы.')
    return redirect(url_for('rgz.books_list'))
