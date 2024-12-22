async function fillFilmList() {
    const response = await fetch('/lab7/rest-api/films/');
    const films = await response.json();
    const tbody = document.getElementById('film-list');
    tbody.innerHTML = '';
    films.forEach((film, index) => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${film.title}</td>
            <td>${film.title_ru}</td>
            <td>${film.year}</td>
            <td>
                <button onclick="editFilm(${film.id})">редактировать</button>
                <button onclick="deleteFilm(${film.id}, '${film.title}')">удалить</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

function showModal() {
    document.querySelector('.modal').style.display = 'block';
    document.getElementById('description-error').innerText = '';
}

function hideModal() {
    document.querySelector('.modal').style.display = 'none';
}

function cancel() {
    hideModal();
}

function addFilm() {
    document.getElementById('id').value = '';
    document.getElementById('title').value = '';
    document.getElementById('title-ru').value = '';
    document.getElementById('year').value = '';
    document.getElementById('description').value = '';
    showModal();
}

function editFilm(id) {
    fetch(`/lab7/rest-api/films/${id}`)
        .then(response => response.json())
        .then(film => {
            document.getElementById('id').value = id;
            document.getElementById('title').value = film.title;
            document.getElementById('title-ru').value = film.title_ru;
            document.getElementById('year').value = film.year;
            document.getElementById('description').value = film.description;
            showModal();
        });
}

function sendFilm() {
    const id = document.getElementById('id').value;
    const film = {
        title: document.getElementById('title').value,
        title_ru: document.getElementById('title-ru').value,
        year: parseInt(document.getElementById('year').value, 10),
        description: document.getElementById('description').value
    };
    const url = id ? `/lab7/rest-api/films/${id}` : '/lab7/rest-api/films/';
    const method = id ? 'PUT' : 'POST';

    fetch(url, {
        method: method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(film)
    })
        .then(resp => {
            if (resp.ok) {
                fillFilmList();
                hideModal();
                return {};
            }
            return resp.json();
        })
        .then(errors => {
            if (errors.description) {
                document.getElementById('description-error').innerText = errors.description;
            }
        });
}

function deleteFilm(id, title) {
    if (!confirm(`Вы точно хотите удалить фильм "${title}"?`)) return;
    fetch(`/lab7/rest-api/films/${id}`, { method: 'DELETE' }).then(() => fillFilmList());
}

document.addEventListener('DOMContentLoaded', fillFilmList);

