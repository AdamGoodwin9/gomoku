const socket = io.connect('http://' + document.domain + ':' + location.port);
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const margin = 75;
const cellSize = (canvas.width - 2 * margin) / 18;

let blackCaptures = 0;
let whiteCaptures = 0;
let board = null;
let gameMode = null;
let currentPlayer = 1;  // 1 for Black, -1 for White
let isAiMove = false; 
let aiStartTime;  // Variable to store the start time for the AI move
let aiTimerInterval;  // Variable to store the interval for updating the display

// Start the timer when the AI starts thinking
function startAiTimer() {
    aiStartTime = performance.now();  // More precise than Date()
    document.getElementById('ai-timer').style.display = 'inline';  // Make the timer visible
    
    // Clear any existing timer interval
    if (aiTimerInterval) {
        clearInterval(aiTimerInterval);
    }
    
    // Update the timer display every 100ms
    aiTimerInterval = setInterval(function() {
        const currentTime = performance.now();
        const elapsedTime = ((currentTime - aiStartTime) / 1000).toFixed(2);  // Calculate time in seconds with two decimal places
        document.getElementById('ai-timer').innerText = elapsedTime;
    }, 10);  // Update every 10ms
}

// Stop the timer when the AI move is made
function stopAiTimer() {
    if (aiTimerInterval) {
        clearInterval(aiTimerInterval);  // Stop updating the timer
    }
    
    const aiEndTime = performance.now();
    const totalTime = ((aiEndTime - aiStartTime) / 1000).toFixed(2);  // Total time in seconds
    document.getElementById('ai-timer').innerText = totalTime;  // Display final time
}

function getFreshBoard() {
    return Array(19).fill().map(() => Array(19).fill(0));
}

function startGame(mode) {
    gameMode = mode;
    socket.emit('start_game', { game_mode: mode });
}

socket.on('game_started', function() {
    board = getFreshBoard();
    currentPlayer = 1;
    
    document.getElementById('menu').style.display = 'none';
    document.getElementById('gameCanvas').style.display = 'block';
    showSettingsButton();

    if (gameMode === 'pve_white') {
        currentPlayer = -1;  // Player is White
        // AI makes the first move
        isAiMove = true;
        startAiTimer();
        showSpinner();
    }

    drawBoard();
});

// Handle player click
canvas.addEventListener('click', function(event) {
    const menuVisible = document.getElementById('menu').style.display === 'flex';
    const winPopupVisible = document.getElementById('win-popup').style.display === 'flex';
    const settingsMenuVisible = document.getElementById('settings-menu').style.display === 'flex';

    if (menuVisible || winPopupVisible || settingsMenuVisible || board === null || isAiMove) return;

    const x = Math.floor((event.offsetX - margin + cellSize / 2) / cellSize);
    const y = Math.floor((event.offsetY - margin + cellSize / 2) / cellSize);
    
    if (x < 0 || y < 0 || x > 18 || y > 18 || board[x][y] !== 0) return;
    
    if (gameMode !== 'pvp') {
        isAiMove = true;
        startAiTimer();
        showSpinner();
    }

    socket.emit('player_move', { move: [x, y], game_mode: gameMode });
});

// Draw the board and pieces
function drawBoard() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = '#DEB887';  // Goban color
    ctx.fillRect(0, 0, canvas.width, canvas.height);  // Fill background with Goban color

    // Draw grid lines
    for (let i = 0; i <= 18; i++) {
        ctx.moveTo(margin + i * cellSize, margin);
        ctx.lineTo(margin + i * cellSize, canvas.height - margin);
        ctx.moveTo(margin, margin + i * cellSize);
        ctx.lineTo(canvas.width - margin, margin + i * cellSize);
        ctx.stroke();
    }

    if (board !== null) {
        // Draw stones
        for (let i = 0; i < 19; i++) {
            for (let j = 0; j < 19; j++) {
                if (board[i][j] == 1) {
                    drawStone(i, j, 'black');
                } else if (board[i][j] == -1) {
                    drawStone(i, j, 'white');
                }
            }
        }

        drawCaptureCount(blackCaptures, whiteCaptures);
    }
}

function drawCaptureCount(blackCaptures, whiteCaptures) {
    ctx.font = '30px Arial';

    ctx.fillStyle = 'black';
    ctx.fillText(blackCaptures, margin / 1.5, margin / 1.5);

    ctx.fillStyle = 'white';
    ctx.fillText(whiteCaptures, canvas.width - margin / 1.5 - ctx.measureText(whiteCaptures).width, margin / 1.5);
}


function drawStone(x, y, color) {
    ctx.beginPath();
    ctx.arc(margin + x * cellSize, margin + y * cellSize, 10, 0, 2 * Math.PI);
    ctx.fillStyle = color;
    ctx.fill();
    ctx.stroke();
}

function toggleSettingsButton() {
    const settingsButton = document.getElementById('settings-button');
    if (settingsButton.style.display === 'none' || settingsButton.style.display === '') {
        settingsButton.style.display = 'flex';
    } else {
        settingsButton.style.display = 'none';
    }
}

function showSettingsButton() {
    const settingsButton = document.getElementById('settings-button');
    settingsButton.style.display = 'flex';
}

function hideSettingsButton() {
    const settingsButton = document.getElementById('settings-button');
    settingsButton.style.display = 'none';
}

function toggleSettingsMenu() {
    const settingsMenu = document.getElementById('settings-menu');
    if (settingsMenu.style.display === 'none' || settingsMenu.style.display === '') {
        settingsMenu.style.display = 'flex';
    } else {
        settingsMenu.style.display = 'none';
    }
}

function showSettingsMenu() {
    const settingsMenu = document.getElementById('settings-menu');
    settingsMenu.style.display = 'flex';
}

function hideSettingsMenu() {
    const settingsMenu = document.getElementById('settings-menu');
    settingsMenu.style.display = 'none';
}

function showSpinner() {
    document.getElementById('spinner').style.display = 'block';
}

function hideSpinner() {
    document.getElementById('spinner').style.display = 'none';
}

function restartGame() {
    socket.emit('restart_game');
    document.getElementById('win-popup').style.display = 'none';
    hideSettingsMenu();
    showSettingsButton();
}

function backToMainMenu() {
    socket.emit('end_game');

    board = Array(19).fill().map(() => Array(19).fill(0));  // Clear the board
    currentPlayer = null;  // Reset the current player
    gameMode = null;  // Reset the game mode
    isAiMove = false;  // Reset AI move flag
    
    document.getElementById('gameCanvas').style.display = '';
    document.getElementById('win-popup').style.display = 'none';
    hideSettingsButton();
    hideSettingsMenu();
    document.getElementById('menu').style.display = 'flex';  // Show main menu
    drawBoard();
}

// Resume the game by hiding the settings menu
function resumeGame() {
    hideSettingsMenu();
}

// Handle board updates in PvP mode
socket.on('board_update', function(data) {
    board = data.board;
    blackCaptures = data.blackCaptures;
    whiteCaptures = data.whiteCaptures;
    drawBoard();
});

// Handle AI move in PvE mode
socket.on('ai_move', function(data) {
    board = data.board;
    isAiMove = false;
    stopAiTimer();
    hideSpinner();
    drawBoard();
});

// Listen for 'game_over' event from the server
socket.on('game_over', function(data) {
    showWinPopup(data.winner);
});

// Function to show the win popup
function showWinPopup(message) {
    // Update the win message text
    document.getElementById('win-message').innerText = message;

    // Display the win popup
    document.getElementById('win-popup').style.display = 'flex';

    hideSpinner();
    hideSettingsButton();
}


// Initial drawing
drawBoard();
