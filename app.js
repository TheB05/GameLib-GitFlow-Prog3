let games = JSON.parse(localStorage.getItem('games')) || [];
let editIndex = null;

const USERNAME = "IchibanKasuga";
const PASSWORD = "ichiban12345";

function showLogin() {
    document.body.innerHTML = `
        <div class="login-container">
            <h2>Login</h2>
            <form id="login-form">
                <input type="text" id="login-username" placeholder="Username" required><br>
                <input type="password" id="login-password" placeholder="Password" required><br>
                <button type="submit">Login</button>
                <p id="login-error" style="color:red;"></p>
            </form>
        </div>
    `;
    document.getElementById('login-form').addEventListener('submit', function(e) {
        e.preventDefault();
        const username = document.getElementById('login-username').value;
        const password = document.getElementById('login-password').value;
        if (username === USERNAME && password === PASSWORD) {
            document.body.innerHTML = originalBody;
            attachGameFormEvents();
            updateGameList();
            setupToggleList();
        } else {
            document.getElementById('login-error').textContent = "Invalid username or password.";
        }
    });
}

const originalBody = document.body.innerHTML;

function attachGameFormEvents() {
    document.getElementById('game-form').addEventListener('submit', function(event) {
        event.preventDefault();
        const title = document.getElementById('game-title').value;
        const genre = document.getElementById('game-genre').value;
        const release = document.getElementById('game-release').value;
        const description = document.getElementById('game-description').value;
        const photo = document.getElementById('game-photo').value;
        addGame(title, genre, release, description, photo);
        this.reset();
        editIndex = null;
    });
}

function saveGames() {
    localStorage.setItem('games', JSON.stringify(games));
}

function addGame(title, genre, release, description, photo) {
    const game = { title, genre, release, description, photo };
    if (editIndex !== null) {
        games[editIndex] = game;
        editIndex = null;
    } else {
        games.push(game);
    }
    saveGames();
    updateGameList();
}

function updateGameList() {
    const tableBody = document.getElementById('game-table-body');
    tableBody.innerHTML = '';
    games.forEach((game, index) => {
        const row = document.createElement('tr');

        const photoCell = document.createElement('td');
        const img = document.createElement('img');
        img.src = game.photo;
        img.alt = game.title;
        img.style.width = '50px';
        img.style.height = '50px';
        photoCell.appendChild(img);

        const titleCell = document.createElement('td');
        const genreCell = document.createElement('td');
        const releaseCell = document.createElement('td');
        const descriptionCell = document.createElement('td');
        const optionsCell = document.createElement('td');

        titleCell.textContent = game.title;
        genreCell.textContent = game.genre;
        releaseCell.textContent = game.release;
        descriptionCell.textContent = game.description;

        //Create edit button
        const editBtn = document.createElement('button');
        editBtn.textContent = 'Edit';
        editBtn.onclick = function() {
            document.getElementById('game-title').value = game.title;
            document.getElementById('game-genre').value = game.genre;
            document.getElementById('game-release').value = game.release;
            document.getElementById('game-description').value = game.description;
            document.getElementById('game-photo').value = game.photo;
            editIndex = index;
        }; //Now you can actually edit the games, even if it is simple :D

        //Create delete button
        const deleteBtn = document.createElement('button');
        deleteBtn.textContent = 'Delete';
        deleteBtn.onclick = function() {
            games.splice(index, 1);
            saveGames();
            updateGameList();
        }; //Now you can delete the games from the list, yooho! :D

        optionsCell.appendChild(editBtn);
        optionsCell.appendChild(deleteBtn);

        row.appendChild(photoCell);
        row.appendChild(titleCell);
        row.appendChild(genreCell);
        row.appendChild(releaseCell);
        row.appendChild(descriptionCell);
        row.appendChild(optionsCell);

        tableBody.appendChild(row);
    }); 
}

function setupToggleList() {
    const toggleBtn = document.getElementById('toggle-list-btn');
    const gameTable = document.getElementById('game-table');
    toggleBtn.addEventListener('click', function() {
        if (gameTable.style.display === 'none') {
            gameTable.style.display = '';
            toggleBtn.textContent = 'Hide Game List';
        } else {
            gameTable.style.display = 'none';
            toggleBtn.textContent = 'Show Game List';
        }
    });
}

showLogin();