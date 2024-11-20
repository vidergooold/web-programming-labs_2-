from flask import Blueprint, render_template, request, jsonify, session

lab6 = Blueprint('lab6', __name__)

# Глобальная переменная для хранения информации об офисах
offices = []
for i in range(1, 11):  # Создаем 10 офисов
    offices.append({"number": i, "tenant": ""})

@lab6.route('/lab6/lab/')
def ():
    return render_template('lab6/lab6.html')

@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.json  # Получаем JSON из запроса
    id = data['id']  # Идентификатор запроса

    if data['method'] == 'info':  # Метод info возвращает список офисов
        return {
            "jsonrpc": "2.0",
            "result": offices,
            "id": id
        }

    # Проверка авторизации
    login = session.get('login')
    if not login:
        return {
            "jsonrpc": "2.0",
            "error": {
                "code": 1,
                "message": "Unauthorized"
            },
            "id": id
        }

    if data['method'] == 'booking':  # Метод booking
        office_number = data['params']['number']  # Номер офиса из параметров
        for office in offices:
            if office['number'] == office_number:
                if office['tenant'] != '':  # Если офис уже занят
                    return {
                        "jsonrpc": "2.0",
                        "error": {
                            "code": 2,
                            "message": "Already booked"
                        },
                        "id": id
                    }
                office['tenant'] = login  # Бронируем офис для текущего пользователя
                return {
                    "jsonrpc": "2.0",
                    "result": "success",
                    "id": id
                }
        return {
            "jsonrpc": "2.0",
            "error": {
                "code": -32601,
                "message": "Office not found"
            },
            "id": id
        }

    return {
        "jsonrpc": "2.0",
        "error": {
            "code": -32601,
            "message": "Method not found"
        },
        "id": id
    }
