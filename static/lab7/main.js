// Функция для отображения модального окна
function showModal() {
    document.querySelector('div.modal').style.display = 'block';
}

// Функция для скрытия модального окна
function hideModal() {
    document.querySelector('div.modal').style.display = 'none';
}

// Функция отмены (скрывает модальное окно)
function cancel() {
    hideModal();
}

// Функция для отображения модального окна при добавлении нового фильма
function addFilm() {
    document.getElementById('id').value = ''; // Очищаем скрытое поле ID
    document.getElementById('title').value = '';
    document.getElementById('title-ru').value = '';
    document.getElementById('year').value = '';
    document.getElementById('description').value = '';
    showModal();
}

// Функция для отправки нового фильма на сервер
function sendFilm() {
    const film = {
        title: document.getElementById('title').value,
        title_ru: document.getElementById('title-ru').value,
        year: document.getElementById('year').value,
        description: document.getElementById('description').value
    };

    const url = '/lab7/rest-api/films/';
    const method = 'POST';

    fetch(url, {
        method: method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(film)
    })
        .then(() => {
            fillFilmList(); // Перезагружаем таблицу фильмов
            hideModal(); // Скрываем модальное окно
        })
        .catch(error => {
            console.error('Ошибка при добавлении фильма:', error);
        });
}

// Функция для загрузки списка фильмов
function fillFilmList() {
    fetch('/lab7/rest-api/films/')
        .then(data => data.json())
        .then(films => {
            let tbody = document.getElementById('film-list');
            tbody.innerHTML = ''; // Очищаем таблицу перед заполнением

            films.forEach((film, index) => {
                let tr = document.createElement('tr');

                // Создаем ячейки
                let tdTitle = document.createElement('td');
                let tdTitleRus = document.createElement('td');
                let tdYear = document.createElement('td');
                let tdActions = document.createElement('td');

                // Заполняем ячейки данными
                tdTitle.innerText = film.title === film.title_ru ? '' : film.title;
                tdTitleRus.innerText = film.title_ru;
                tdYear.innerText = film.year;

                // Создаем кнопки "Редактировать" и "Удалить"
                let editButton = document.createElement('button');
                editButton.innerText = 'редактировать';
                editButton.onclick = function () {
                    document.getElementById('id').value = index;
                    document.getElementById('title').value = film.title;
                    document.getElementById('title-ru').value = film.title_ru;
                    document.getElementById('year').value = film.year;
                    document.getElementById('description').value = film.description;
                    showModal();
                };

                let delButton = document.createElement('button');
                delButton.innerText = 'удалить';
                delButton.onclick = function () {
                    deleteFilm(index, film.title_ru);
                };

                // Добавляем кнопки в ячейку действий
                tdActions.appendChild(editButton);
                tdActions.appendChild(delButton);

                // Добавляем ячейки в строку
                tr.appendChild(tdTitle);
                tr.appendChild(tdTitleRus);
                tr.appendChild(tdYear);
                tr.appendChild(tdActions);

                // Добавляем строку в таблицу
                tbody.appendChild(tr);
            });
        });
}

// Функция для удаления фильма
function deleteFilm(id, title) {
    if (!confirm(`Вы точно хотите удалить фильм "${title}"?`)) return;

    fetch(`/lab7/rest-api/films/${id}/`, { method: 'DELETE' })
        .then(() => {
            fillFilmList(); // Перезагружаем список фильмов
        })
        .catch(error => {
            console.error('Ошибка при удалении фильма:', error);
        });
}
