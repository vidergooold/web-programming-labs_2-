from flask import Blueprint, render_template, request, jsonify, session
import sqlite3

lab6 = Blueprint('lab6', __name__)

# Инициализация базы данных и создание таблицы offices
def init_db():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS offices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            number INTEGER NOT NULL UNIQUE,
            tenant TEXT,
            price INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Добавить данные в таблицу offices (если данные еще не добавлены)
def populate_offices():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) FROM offices')
    if cur.fetchone()[0] == 0:
        offices = [
            {"number": i, "tenant": "", "price": 900 + i * 10} for i in range(1, 11)
        ]
        for office in offices:
            cur.execute('INSERT INTO offices (number, tenant, price) VALUES (?, ?, ?)', 
                        (office['number'], office['tenant'], office['price']))
        conn.commit()
    conn.close()

# Выполнить инициализацию и заполнение базы данных
init_db()
populate_offices()

@lab6.route('/lab6/')
def main():
    return render_template('lab6/lab6.html')

@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    id = data.get('id')
    method = data.get('method')

    if not method:
        return jsonify({'jsonrpc': '2.0', 'error': {'code': -32601, 'message': 'Method not found'}, 'id': id})

    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    # Обработчик метода info
    if method == 'info':
        cur.execute('SELECT number, tenant, price FROM offices')
        offices = [{'number': row[0], 'tenant': row[1], 'price': row[2]} for row in cur.fetchall()]
        conn.close()
        return jsonify({'jsonrpc': '2.0', 'result': offices, 'id': id})

    # Проверка авторизации
    login = session.get('login')
    if not login:
        return jsonify({'jsonrpc': '2.0', 'error': {'code': 1, 'message': 'Unauthorized'}, 'id': id})

    # Обработчик метода booking
    if method == 'booking':
        office_number = data['params']
        cur.execute('SELECT tenant FROM offices WHERE number = ?', (office_number,))
        tenant = cur.fetchone()
        if tenant and tenant[0]:
            conn.close()
            return jsonify({'jsonrpc': '2.0', 'error': {'code': 2, 'message': 'Already booked'}, 'id': id})
        cur.execute('UPDATE offices SET tenant = ? WHERE number = ?', (login, office_number))
        conn.commit()
        conn.close()
        return jsonify({'jsonrpc': '2.0', 'result': 'success', 'id': id})

    # Обработчик метода cancellation
    if method == 'cancellation':
        office_number = data['params']
        cur.execute('SELECT tenant FROM offices WHERE number = ?', (office_number,))
        tenant = cur.fetchone()
        if not tenant or tenant[0] != login:
            conn.close()
            return jsonify({'jsonrpc': '2.0', 'error': {'code': 3, 'message': 'Cannot cancel, not your booking'}, 'id': id})
        cur.execute('UPDATE offices SET tenant = "" WHERE number = ?', (office_number,))
        conn.commit()
        conn.close()
        return jsonify({'jsonrpc': '2.0', 'result': 'success', 'id': id})

    conn.close()
    return jsonify({'jsonrpc': '2.0', 'error': {'code': -32601, 'message': 'Method not found'}, 'id': id})
