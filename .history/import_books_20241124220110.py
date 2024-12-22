import sqlite3
import csv

# Путь к файлу базы данных
DATABASE = 'books.db'

# Путь к вашему файлу CSV
CSV_FILE = 'russian_books_data.csv'

# Подключение к базе данных
conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

# Открываем CSV файл и загружаем данные
with open(CSV_FILE, encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        cursor.execute('''
            INSERT INTO books (title, author, pages, publisher)
            VALUES (?, ?, ?, ?)
        ''', (row['title'], row['author'], int(row['pages']), row['publisher']))

# Сохраняем изменения и закрываем соединение
conn.commit()
conn.close()

print("Данные успешно загружены в таблицу 'books'.")
