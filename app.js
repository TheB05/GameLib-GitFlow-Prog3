// src/app.js

let games = [];

function addGame(title, genre, year) {
    const game = { title, genre, year };
    games.push(game);
    updateGameList();
}

function updateGameList() {
    const gameList = document.getElementById('game-list');
    gameList.innerHTML = '';
    games.forEach((game, index) => {
        const listItem = document.createElement('li');
        listItem.textContent = `${game.title} (${game.year}) - Genre: ${game.genre}`;
        gameList.appendChild(listItem);
    });
}

document.getElementById('add-game-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const title = document.getElementById('title').value;
    const genre = document.getElementById('genre').value;
    const year = document.getElementById('year').value;
    addGame(title, genre, year);
    this.reset();
});