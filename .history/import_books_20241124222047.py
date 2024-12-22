import sqlite3
import csv

# Подключение к базе данных
conn = sqlite3.connect('books.db')
cursor = conn.cursor()

# Путь к вашему файлу CSV
csv_file = 'russian_books_data.csv'

# Чтение данных из CSV
with open(csv_file, 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        # Проверяем, существует ли уже книга с таким названием
        cursor.execute("SELECT * FROM books WHERE title = ?", (row['title'],))
        result = cursor.fetchone()
        if not result:  # Если книги ещё нет, добавляем её
            cursor.execute('''
                INSERT INTO books (title, author, pages, publisher)
                VALUES (?, ?, ?, ?)
            ''', (row['title'], row['author'], int(row['pages']), row['publisher']))

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()

print("Данные успешно загружены.")
