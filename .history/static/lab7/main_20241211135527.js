<script>
    async function loadFilms() {
        const response = await fetch('/lab7/rest-api/films/');
        const films = await response.json();

        const filmList = document.getElementById('film-list');
        filmList.innerHTML = '';

        films.forEach(film => {
            const li = document.createElement('li');
            li.innerHTML = `<strong>${film.title} (${film.title_ru})</strong> - ${film.year}<br>${film.description}`;
            filmList.appendChild(li);
        });
    }

    document.addEventListener('DOMContentLoaded', loadFilms);
</script>