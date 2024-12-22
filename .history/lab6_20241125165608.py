from flask import Blueprint, render_template, request, jsonify, session
import sqlite3

lab6 = Blueprint('lab6', __name__)

@lab6.route('/')
def lab():
    return render_template('lab6/lab6.html')

@lab6.route('/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    id = data.get('id')
    method = data.get('method')

    if not method:
        return jsonify({'jsonrpc': '2.0', 'error': {'code': -32601, 'message': 'Method not found'}, 'id': id})

    try:
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()

            if method == 'info':
                cur.execute('SELECT number, tenant, price FROM offices')
                offices = [{'number': row[0], 'tenant': row[1], 'price': row[2]} for row in cur.fetchall()]
                return jsonify({'jsonrpc': '2.0', 'result': offices, 'id': id})

            login = session.get('login')
            if not login:
                return jsonify({'jsonrpc': '2.0', 'error': {'code': 1, 'message': 'Unauthorized'}, 'id': id})

            if method == 'booking':
                office_number = data.get('params')
                if not office_number:
                    return jsonify({'jsonrpc': '2.0', 'error': {'code': -32602, 'message': 'Invalid params'}, 'id': id})
                cur.execute('SELECT tenant FROM offices WHERE number = ?', (office_number,))
                tenant = cur.fetchone()
                if tenant and tenant[0]:
                    return jsonify({'jsonrpc': '2.0', 'error': {'code': 2, 'message': 'Already booked'}, 'id': id})
                cur.execute('UPDATE offices SET tenant = ? WHERE number = ?', (login, office_number))
                conn.commit()
                return jsonify({'jsonrpc': '2.0', 'result': 'success', 'id': id})

            if method == 'cancellation':
                office_number = data.get('params')
                if not office_number:
                    return jsonify({'jsonrpc': '2.0', 'error': {'code': -32602, 'message': 'Invalid params'}, 'id': id})
                cur.execute('SELECT tenant FROM offices WHERE number = ?', (office_number,))
                tenant = cur.fetchone()
                if not tenant or tenant[0] != login:
                    return jsonify({'jsonrpc': '2.0', 'error': {'code': 3, 'message': 'Cannot cancel, not your booking'}, 'id': id})
                cur.execute('UPDATE offices SET tenant = NULL WHERE number = ?', (office_number,))
                conn.commit()
                return jsonify({'jsonrpc': '2.0', 'result': 'success', 'id': id})

            # Новый метод: общая стоимость аренды
            if method == 'total_cost':
                cur.execute('SELECT SUM(price) FROM offices WHERE tenant = ?', (login,))
                total = cur.fetchone()[0] or 0
                return jsonify({'jsonrpc': '2.0', 'result': total, 'id': id})

            return jsonify({'jsonrpc': '2.0', 'error': {'code': -32601, 'message': 'Method not found'}, 'id': id})
    except sqlite3.Error as e:
        return jsonify({'jsonrpc': '2.0', 'error': {'code': 500, 'message': str(e)}, 'id': id})
