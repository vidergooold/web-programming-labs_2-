// Функция для загрузки списка фильмов и отображения их в таблице
function fillFilmList() {
    console.log("Функция fillFilmList вызвана");

    fetch('/lab7/rest-api/films/')
        .then(function (data) {
            return data.json();
        })
        .then(function (films) {
            console.log("Полученные фильмы:", films);

            let tbody = document.getElementById('film-list');
            tbody.innerHTML = ''; // Очищаем таблицу перед заполнением

            for (let i = 0; i < films.length; i++) {
                let tr = document.createElement('tr'); // Создаем строку таблицы

                // Создаем ячейки
                let tdTitle = document.createElement('td');
                let tdTitleRus = document.createElement('td');
                let tdYear = document.createElement('td');
                let tdActions = document.createElement('td');

                // Заполняем ячейки данными
                tdTitle.innerText = films[i].title === films[i].title_ru ? '' : films[i].title;
                tdTitleRus.innerText = films[i].title_ru;
                tdYear.innerText = films[i].year;

                // Создаем кнопки
                let editButton = document.createElement('button');
                editButton.innerText = 'Редактировать';
                editButton.onclick = function () {
                    alert(`Редактировать фильм с ID ${i}`);
                    // Здесь можно реализовать функцию редактирования
                };

                let delButton = document.createElement('button');
                delButton.innerText = 'Удалить';
                delButton.onclick = function () {
                    deleteFilm(i); // Удаление фильма
                };

                // Добавляем кнопки в ячейку действий
                tdActions.append(editButton);
                tdActions.append(delButton);

                // Добавляем ячейки в строку
                tr.append(tdTitle);
                tr.append(tdTitleRus);
                tr.append(tdYear);
                tr.append(tdActions);

                // Добавляем строку в таблицу
                tbody.append(tr);
            }
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
