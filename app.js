let games = JSON.parse(localStorage.getItem('games')) || [];
let editIndex = null;

const USERNAME = "IchibanKasuga";
const PASSWORD = "ichiban12345";

let originalBody = "";

window.addEventListener('DOMContentLoaded', () => {
    originalBody = document.body.innerHTML;
    showLogin();
});

//Fixin the login form...
function showLogin() {
    document.body.innerHTML = `
    <div class="login-container">
        <h2>Login</h2>
        <form id="login-form">
            <input type="text" id="login-username" placeholder="Username" maxlength="25" required>
            <input type="password" id="login-password" placeholder="Password" maxlength="25" required>
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
            showApp();
        } else {
            document.getElementById('login-error').textContent = "Invalid username or password.";
        }
    });
}

function showApp() {
    document.body.innerHTML = originalBody;
    addLogoutButton();
    attachGameFormEvents();
    updateGameList();
    setupToggleList();
    setupLogout();
    showDashboard();
}

function addLogoutButton() {
    const container = document.querySelector('.container');
    if (container && !document.getElementById('logout-btn')) {
        const logoutBtn = document.createElement('button');
        logoutBtn.id = 'logout-btn';
        logoutBtn.textContent = 'Logout';
        logoutBtn.style.cssText = 'position:absolute;top:24px;right:40px;background:#6366f1;color:#fff;border:none;padding:10px 18px;border-radius:8px;font-size:15px;cursor:pointer;';
        container.prepend(logoutBtn);
    }
}

function setupLogout() {
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function() {
            showLogin();
        });
    }
}

function attachGameFormEvents() {
    const form = document.getElementById('game-form');
    if (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            const title = document.getElementById('game-title').value;
            const genre = document.getElementById('game-genre').value;
            const release = document.getElementById('game-release').value;
            const description = document.getElementById('game-description').value;
            const achievements = document.getElementById('game-achievements').value;
            const playtime = document.getElementById('game-playtime').value;
            const photo = document.getElementById('game-photo').value;
            addGame(title, genre, release, description, achievements, playtime, photo);
            this.reset();
            editIndex = null;
        });
    }
}

function saveGames() {
    localStorage.setItem('games', JSON.stringify(games));
}

function addGame(title, genre, release, description, achievements, playtime, photo) {
    const game = { title, genre, release, description, achievements, playtime, photo };
    if (editIndex !== null) {
        games[editIndex] = game;
        editIndex = null;
    } else {
        games.push(game);
    }
    saveGames();
    updateGameList();
    showDashboard();
}

function updateGameList() {
    const tableBody = document.getElementById('game-table-body');
    if (!tableBody) return;
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
        const achievementsCell = document.createElement('td');
        const playtimeCell = document.createElement('td');
        const optionsCell = document.createElement('td');

        titleCell.textContent = game.title;
        genreCell.textContent = game.genre;
        releaseCell.textContent = game.release;
        descriptionCell.textContent = game.description;
        achievementsCell.textContent = game.achievements;
        playtimeCell.textContent = game.playtime;

        //Edit button
        const editBtn = document.createElement('button');
        editBtn.textContent = 'Edit';
        editBtn.onclick = function() {
            document.getElementById('game-title').value = game.title;
            document.getElementById('game-genre').value = game.genre;
            document.getElementById('game-release').value = game.release;
            document.getElementById('game-description').value = game.description;
            document.getElementById('game-achievements').value = game.achievements;
            document.getElementById('game-playtime').value = game.playtime;
            document.getElementById('game-photo').value = game.photo;
            editIndex = index;
        };

        //Delete button
        const deleteBtn = document.createElement('button');
        deleteBtn.textContent = 'Delete';
        deleteBtn.onclick = function() {
            games.splice(index, 1);
            saveGames();
            updateGameList();
            showDashboard();
        };

        optionsCell.appendChild(editBtn);
        optionsCell.appendChild(deleteBtn);

        row.appendChild(photoCell);
        row.appendChild(titleCell);
        row.appendChild(genreCell);
        row.appendChild(releaseCell);
        row.appendChild(descriptionCell);
        row.appendChild(achievementsCell);
        row.appendChild(playtimeCell);
        row.appendChild(optionsCell);

        tableBody.appendChild(row);
    });
}

function setupToggleList() {
    const toggleBtn = document.getElementById('toggle-list-btn');
    const gameTable = document.getElementById('game-table');
    if (toggleBtn && gameTable) {
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
}

//DASHBOARD: Show top 3 most played genres.
function showDashboard() {
    let dashboard = document.getElementById('dashboard');
    if (!dashboard) return;

    //This Calculates the top 3 genres by total playtime.
    const genrePlaytime = {};
    games.forEach(game => {
        const genre = game.genre || "Unknown";
        const playtime = parseInt(game.playtime) || 0;
        if (!genrePlaytime[genre]) genrePlaytime[genre] = 0;
        genrePlaytime[genre] += playtime;
    });

    const sortedGenres = Object.entries(genrePlaytime)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 3);

    let html = `<h3 style="margin-top:0;">Top 3 Most Played Genres</h3>`;
    if (sortedGenres.length === 0) {
        html += `<p>No games added yet.</p>`;
    } else {
        html += `<ol style="padding-left:20px;">`;
        sortedGenres.forEach(([genre, playtime]) => {
            html += `<li><strong>${genre}</strong> - ${playtime} hrs</li>`;
        });
        html += `</ol>`;
    }
    dashboard.innerHTML = html;
}