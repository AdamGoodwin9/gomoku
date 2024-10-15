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
let aiPlayer = 0;
let isAiMove = false; 

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
    aiPlayer = 0;
    
    document.getElementById('menu').style.display = 'none';
    document.getElementById('gameCanvas').style.display = 'block';
    toggleSettingsButton();

    if (gameMode === 'pve_white') {
        currentPlayer = -1;  // Player is White
        aiPlayer = 1;  // AI is Black
        // AI makes the first move
        let aiMove = findBestAIMove();
        board[aiMove[0]][aiMove[1]] = aiPlayer;
    }

    drawBoard();
});

// Handle player click
canvas.addEventListener('click', function(event) {
    if (gameMode == "mainMenu") return;

    const x = Math.floor((event.offsetX - margin + cellSize / 2) / cellSize);
    const y = Math.floor((event.offsetY - margin + cellSize / 2) / cellSize);
    
    if (!isAiMove && board[x][y] === 0) {  // Only send if it's a valid move
        socket.emit('player_move', { move: [x, y], game_mode: gameMode });
    }
});

function handleClick(x, y) {
    if (gameMode === 'pvp') {
        if (board[x][y] === 0) {
            board[x][y] = currentPlayer; //needs socket emit?
            // socket.emit('player_move', {
            //     board: board,
            //     move: [x, y],
            //     currentPlayer: currentPlayer
            // });
            drawBoard();

            if (checkWin(x, y, currentPlayer)) {
                alert((currentPlayer === 1 ? 'Black' : 'White') + ' wins!');
                return;
            }
            currentPlayer *= -1;
        }
    }
    else {
        if (currentPlayer !== aiPlayer) { // Player's turn vs AI
            if (board[x][y]=== 0) {
                board[x][y] = currentPlayer; //needs socket emit?
                drawBoard();

                if (checkWin(x, y, currentPlayer)) {
                    alert((currentPlayer === 1 ? 'Black' : 'White') + ' wins!');
                    return;
                }
                
                currentPlayer *= -1;

                let aiMove = findBestAIMove();  // AI move calculation
                board[aiMove[0]][aiMove[1]] = currentPlayer;
                drawBoard();

                if (checkWin(aiMove[0], aiMove[1], currentPlayer)) { // Check AI win
                    alert((currentPlayer === 1 ? 'Black' : 'White') + ' wins!');
                    return;
                }

                currentPlayer *= -1;
            }
        }
    }
}

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

    if (gameMode != "mainMenu") {
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
}

function toggleSettingsButton() {
    const settingsButton = document.getElementById('settings-button');
    if (settingsButton.style.display === 'none' || settingsButton.style.display === '') {
        settingsButton.style.display = 'flex';
    } else {
        settingsButton.style.display = 'none';
    }
}

function toggleSettingsMenu() {
    const settingsMenu = document.getElementById('settings-menu');
    if (settingsMenu.style.display === 'none' || settingsMenu.style.display === '') {
        settingsMenu.style.display = 'flex';
    } else {
        settingsMenu.style.display = 'none';
    }
}

// Restart the game
function restartGame() {
    // Reset the game board and variables
    board = Array(19).fill().map(() => Array(19).fill(0));
    currentPlayer = 1;
    toggleSettingsMenu();
    drawBoard();
}

// Go back to the main menu
function backToMainMenu() {
    document.getElementById('gameCanvas').style.display = '';
    toggleSettingsButton();
    toggleSettingsMenu();
    document.getElementById('menu').style.display = 'flex';  // Show main menu
}

// Resume the game by hiding the settings menu
function resumeGame() {
    toggleSettingsMenu();
}

// Handle board updates in PvP mode
socket.on('board_update', function(data) {
    board = data.board;
    drawBoard();
});

// Handle AI move in PvE mode
socket.on('ai_move', function(data) {
    board = data.board;
    drawBoard();
});

// Handle game over
socket.on('game_over', function(data) {
    alert(data.winner);
});

// Initial drawing
drawBoard();
