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
