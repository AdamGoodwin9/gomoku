const socket = io.connect('http://' + document.domain + ':' + location.port);
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const margin = 40;
const cellSize = (canvas.width - 2 * margin) / 18;

let board = null;
let gameMode = null;
let currentPlayer = 1;  // 1 for Black, -1 for White
let aiPlayer = null;

function getFreshBoard() {
    return Array(19).fill().map(() => Array(19).fill(0));
}

function startGame(mode) {
    gameMode = mode;
    board = getFreshBoard();
    document.getElementById('menu').style.display = 'none';
    document.getElementById('gameCanvas').style.display = 'block';

    // Start the game based on the mode
    if (gameMode === 'pvp') {
        // PvP logic
    } else if (gameMode === 'pve_black') {
        // AI plays as white, player is black
    } else if (gameMode === 'pve_white') {
        // AI plays as black, player is white
    }

    drawBoard();
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

function drawCaptureCount(black_captures, white_captures) {
    ctx.fillStyle = 'black';
    ctx.font = '30px Arial';
    ctx.fillText(black_captures, margin / 2, margin / 2);

    ctx.fillStyle = 'white';
    ctx.fillText(white_captures, canvas.width - margin / 2 - ctx.measureText(white_captures).width, margin / 2);
}


function drawStone(x, y, color) {
    ctx.beginPath();
    ctx.arc(margin + x * cellSize, margin + y * cellSize, 10, 0, 2 * Math.PI);
    ctx.fillStyle = color;
    ctx.fill();
}

// Handle player click
canvas.addEventListener('click', function(event) {
    const x = Math.floor((event.offsetX - margin) / cellSize);
    const y = Math.floor((event.offsetY - margin) / cellSize);

    handleClick(x, y);
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

function toggleSettings() {
    const settings = document.getElementById('settings');
    if (settings.style.display === 'none') {
        settings.style.display = 'block';
    } else {
        settings.style.display = 'none';
    }
}

function restartGame() {
    // Reset the board and restart the game
    board = Array(19).fill().map(() => Array(19).fill(0));
    blackCaptures = 0;
    whiteCaptures = 0;
    drawBoard();
    toggleSettings();  // Close the settings menu
}

function backToMainMenu() {
    // Return to the main menu
    document.getElementById('menu').style.display = 'block';
    document.getElementById('gameCanvas').style.display = 'none';
    toggleSettings();
}

function resumeGame() {
    // Simply close the settings menu and resume the game
    toggleSettings();
}

// Receive AI move from the server
socket.on('ai_move', function(data) {
    board = data.board;
    drawBoard();
});

// Initial drawing
drawBoard();
