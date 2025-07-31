let games = [];

function addGame(title, genre, release, description) {
    const game = { title, genre, release, description };
    games.push(game);
    updateGameList();
}

function updateGameList() {
    const tableBody = document.getElementById('game-table-body');
    tableBody.innerHTML = '';
    games.forEach((game, index) => {
        const row = document.createElement('tr');

        const titleCell = document.createElement('td');
        const genreCell = document.createElement('td');
        const releaseCell = document.createElement('td');
        const descriptionCell = document.createElement('td');
        const optionsCell = document.createElement('td');

        titleCell.textContent = game.title;
        genreCell.textContent = game.genre;
        releaseCell.textContent = game.release;
        descriptionCell.textContent = game.description;
        optionsCell.textContent = 'Edit | Delete'; // Placeholder for now, options do not work yet.

        row.appendChild(titleCell);
        row.appendChild(genreCell);
        row.appendChild(releaseCell);
        row.appendChild(descriptionCell);
        row.appendChild(optionsCell);

        tableBody.appendChild(row);
    });
}

document.getElementById('game-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const title = document.getElementById('game-title').value;
    const genre = document.getElementById('game-genre').value;
    const release = document.getElementById('game-release').value;
    const description = document.getElementById('game-description').value;
    addGame(title, genre, release, description);
    this.reset();
});