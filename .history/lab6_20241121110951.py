from flask import Blueprint, render_template, request, session

lab6 = Blueprint('lab6', __name__)

# Список офисов с добавлением стоимости аренды
offices = []
for i in range(1, 11):
    offices.append({"number": i, "tenant": "", "price": 900 + i * 3})

@lab6.route('/lab6/')
def lab():
    return render_template('lab6/lab6.html')

@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    id = data['id']

    # Метод info: возвращаем список офисов
    if data['method'] == 'info':
        return {
            'jsonrpc': '2.0',
            'result': offices,
            'id': id
        }

    # Проверка на авторизацию
    login = session.get('login')
    if not login:
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': 1,
                'message': 'Unauthorized'
            },
            'id': id
        }

    # Метод booking: резервирование офиса
    if data['method'] == 'booking':
        office_number = data['params']
        for office in offices:
            if office['number'] == office_number:
                if office['tenant'] != "":
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 2,
                            'message': 'Already booked'
                        },
                        'id': id
                    }
                office['tenant'] = login
                return {
                    'jsonrpc': '2.0',
                    'result': 'success',
                    'id': id
                }

    # Метод cancellation: снятие брони
    if data['method'] == 'cancellation':
        office_number = data['params']
        for office in offices:
            if office['number'] == office_number:
                if office['tenant'] == "":
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': -32601,
                            'message': 'Office not booked'
                        },
                        'id': id
                    }
                if office['tenant'] != login:
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 4,
                            'message': 'Cannot cancel others booking'
                        },
                        'id': id
                    }
                office['tenant'] = ""
                return {
                    'jsonrpc': '2.0',
                    'result': 'success',
                    'id': id
                }

    # Неверный метод
    return {
        'jsonrpc': '2.0',
        'error': {
            'code': -32601,
            'message': 'Method not found'
        },
        'id': id
    }
