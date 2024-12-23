from flask import Blueprint, render_template, request, session, redirect, url_for

lab9 = Blueprint('lab9', __name__)

@lab9.route('/lab9/lab')
def lab():
    return render_template('lab9/index.html')

@lab9.route('/lab9/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session.clear()  # Сброс данных
        return redirect(url_for('lab9.name_input'))
    return render_template('lab9/index.html', result=session.get('result'))

@lab9.route('/lab9/name', methods=['GET', 'POST'])
def name_input():
    if request.method == 'POST':
        session['name'] = request.form['name']
        return redirect(url_for('lab9.age_input'))
    return render_template('lab9/name.html')

@lab9.route('/lab9/age', methods=['GET', 'POST'])
def age_input():
    if request.method == 'POST':
        session['age'] = request.form['age']
        return redirect(url_for('lab9.gender_input'))
    return render_template('lab9/age.html')

@lab9.route('/lab9/gender', methods=['GET', 'POST'])
def gender_input():
    if request.method == 'POST':
        session['gender'] = request.form['gender']
        return redirect(url_for('lab9.preference_input'))
    return render_template('lab9/gender.html')

@lab9.route('/lab9/preference', methods=['GET', 'POST'])
def preference_input():
    if request.method == 'POST':
        preference = request.form.get('preference')
        print(f"Selected preference: {preference}")  # Отладочный вывод
        session['preference'] = preference
        return redirect(url_for('lab9.final'))
    return render_template('lab9/preference.html')

@lab9.route('/lab9/final')
def final():
    # Генерация поздравления
    name = session.get('name')
    age = session.get('age')
    gender = session.get('gender')
    preference = session.get('preference')

    print(f"Gender: {gender}, Preference: {preference}")  # Отладочный вывод

    # Определение поздравления и картинки
    if gender == 'male':
        pronoun = 'ты вырос'
        was_smart = 'был умным'
        if preference == 'что-то вкусное':
            gift = 'мешочек конфет'
            image = url_for('static', filename='images/candy.jpg')
        else:
            gift = 'коробка сладостей'
            image = url_for('static', filename='images/cake.jpg')
    else:
        pronoun = 'ты выросла'
        was_smart = 'была умной'
        if preference == 'что-то вкусное':
            gift = 'мешочек конфет'
            image = url_for('static', filename='images/candy.jpg')
        else:
            gift = 'коробка сладостей'
            image = url_for('static', filename='images/cake.jpg')

    result = f"Поздравляю тебя, {name}! Желаю, чтобы {pronoun} и {was_smart}. Вот тебе подарок — {gift}!"
    session['result'] = result

    # Передача результата и картинки в шаблон
    return render_template('lab9/final.html', result=result, image=image)

@lab9.route('/lab9/reset')
def reset():
    # Очистка данных сессии
    session.clear()
    return redirect(url_for('lab9.index'))  # Перенаправление на главную страницу Lab9
