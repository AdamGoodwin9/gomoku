from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from ai import find_best_move, make_move, capture_stones

app = Flask(__name__)
socketio = SocketIO(app)

# Game state
black_captures = 0
white_captures = 0

@app.route('/')
def index():
    return render_template('index.html')

# Handle player moves
@socketio.on('player_move')
def handle_player_move(data):
    global black_captures, white_captures
    board = data['board']
    player_move = data['move']
    current_player = data['currentPlayer']

    make_move(board, player_move[0], player_move[1], current_player)

    # Check for captures and update counts
    captures = capture_stones(board, player_move[0], player_move[1], 1)
    black_captures += captures

    # Check for game end (win by row or capture count)
    if check_win_by_row(board, player_move[0], player_move[1], 1) or black_captures >= 10:
        emit('game_over', {'winner': 'black'})

    # AI makes a move
    ai_move = find_best_move(board, -1)
    make_move(board, ai_move[0], ai_move[1], -1)

    # Check for captures and update counts
    captures = capture_stones(board, ai_move[0], ai_move[1], -1)
    white_captures += captures

    # Check for game end (win by row or capture count)
    if check_win_by_row(board, ai_move[0], ai_move[1], -1) or white_captures >= 10:
        emit('game_over', {'winner': 'white'})

    # Send the updated board and capture count back to the client
    emit('ai_move', {
        'board': board, 
        'ai_move': ai_move,
        'black_captures': black_captures,
        'white_captures': white_captures
    })

if __name__ == '__main__':
    socketio.run(app, debug=True)
