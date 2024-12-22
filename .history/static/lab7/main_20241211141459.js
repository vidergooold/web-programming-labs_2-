function fillFilmList() {
    fetch('/lab7/rest-api/films/')
        .then(function (data) {
            return data.json();
        })
        .then(function (films) {
            let tbody = document.getElementById('film-list');
            tbody.innerHTML = ''; // Очищаем таблицу перед заполнением

            films.forEach((film, index) => {
                let tr = document.createElement('tr'); // Создаем строку таблицы

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
                    alert(`Редактировать фильм: ${film.title_ru}`);
                    // Здесь можно реализовать редактирование
                };

                let delButton = document.createElement('button');
                delButton.innerText = 'удалить';
                delButton.onclick = function () {
                    deleteFilm(index); // Удаление фильма
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


// Функция для добавления нового фильма
function addFilm() {
    const title = prompt("Введите оригинальное название фильма:");
    const title_ru = prompt("Введите название фильма на русском:");
    const year = prompt("Введите год выпуска фильма:");
    const description = prompt("Введите описание фильма:");

    if (!title || !title_ru || !year || !description) {
        alert("Все поля должны быть заполнены!");
        return;
    }

    const newFilm = {
        title: title,
        title_ru: title_ru,
        year: parseInt(year),
        description: description
    };

    fetch('/lab7/rest-api/films/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newFilm)
    })
        .then(response => {
            if (response.ok) {
                fillFilmList(); // Перезагружаем список фильмов
            } else {
                alert("Ошибка при добавлении фильма!");
            }
        });
}

// Функция для удаления фильма
function deleteFilm(id) {
    fetch(`/lab7/rest-api/films/${id}/`, {
        method: 'DELETE'
    })
        .then(response => {
            if (response.ok) {
                fillFilmList(); // Перезагружаем список фильмов
            } else {
                alert("Ошибка при удалении фильма!");
            }
        });
}
