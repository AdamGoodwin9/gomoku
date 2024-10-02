from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from gomoku import Gomoku  # Import the Gomoku class
from ai import find_best_move  # Assuming AI logic is in ai.py

app = Flask(__name__)
socketio = SocketIO(app)

# Create an instance of the Gomoku game
game = Gomoku()

@app.route('/')
def index():
    return render_template('index.html')

# Handle player move via WebSocket
@socketio.on('player_move')
def handle_player_move(data):
    print('on move')
    x, y = data['move']
    current_player = game.current_player

    # Make the player's move
    if game.make_move(x, y):
        # Check for a win or game over
        if game.game_over:
            emit('game_over', {'winner': game.win_message})
            return

        # If in PvE mode, AI makes its move
        if data['game_mode'] == 'pve':
            ai_move = find_best_move(game.board, -game.current_player)
            game.make_move(ai_move[0], ai_move[1])

            # Check if AI wins
            if game.game_over:
                emit('game_over', {'winner': game.win_message})
            else:
                emit('ai_move', {'board': game.board, 'ai_move': ai_move})

        else:
            # In PvP, emit updated board for the other player
            emit('board_update', {'board': game.board})

if __name__ == '__main__':
    socketio.run(app, debug=True)
