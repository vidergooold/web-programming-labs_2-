from flask import Blueprint, render_template, request, jsonify, session

lab6 = Blueprint('lab6', __name__)

# Глобальная переменная для хранения информации об офисах
offices = []
for i in range(1, 11):  # Создаем 10 офисов
    offices.append({"number": i, "tenant": ""})

@lab6.route('/lab6/')
def lab():
    return render_template('lab6/lab6.html')

@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    id = data['id']

    # Проверка на авторизацию
    login = session.get('login')
    if not login:
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': 1,
                'message': 'Unauthorized',
            },
            'id': id
        }

    # Обработка метода cancellation
    if data['method'] == 'cancellation':
        office_number = data['params']
        for office in offices:
            if office['number'] == office_number:
                # Проверка: офис должен быть арендован
                if office['tenant'] == "":
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 3,
                            'message': 'Office is not rented',
                        },
                        'id': id
                    }
                # Проверка: офис должен быть арендован текущим пользователем
                if office['tenant'] != login:
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 4,
                            'message': 'You cannot cancel someone else\'s rental',
                        },
                        'id': id
                    }
                # Освобождение офиса
                office['tenant'] = ""
                return {
                    'jsonrpc': '2.0',
                    'result': 'success',
                    'id': id
                }

        # Если офис с данным номером не найден
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': 5,
                'message': 'Office not found',
            },
            'id': id
        }

    # Если метод неизвестен
    return {
        'jsonrpc': '2.0',
        'error': {
            'code': -32601,
            'message': 'Method not found',
        },
        'id': id
    }

