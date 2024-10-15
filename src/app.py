from flask import Flask, render_template, session
from flask_socketio import SocketIO, emit
from gomoku import Gomoku, Player  # Import the Gomoku class
from ai import find_best_move  # Assuming AI logic is in ai.py

app = Flask(__name__)
app.secret_key = 'gomoku_gaming_glory_goomba_guacamole'
socketio = SocketIO(app)

# Create an instance of the Gomoku game
game = Gomoku()

@app.route('/')
def index():
    session['game'] = None
    session['mode'] = None
    return render_template('index.html')

@socketio.on('start_game')
def start_game(data):
    # Create a new game instance and store it in the session
    session['game'] = Gomoku()
    session['mode'] = data['game_mode']

    emit('game_started')

@socketio.on('player_move')
def handle_player_move(data):
    x, y = data['move']
    game = session['game']
    mode = session['mode']

    if game.make_move(x, y):
        # Send the updated board back to the client
        emit('board_update', {
            'board': game.board,
            'currentPlayer': game.current_player.value
        })

        # Check if the game is over
        if game.game_over:
            emit('game_over', {'winner': game.win_message})
            return
        
        # If we're in PvE mode, make the AI move next
        if mode in ['pve_black', 'pve_white']:
            ai_player = -1 if mode == 'pve_white' else 1  # AI is White if player chose Black
            ai_move = find_best_move(game.board, ai_player)
            game.make_move(ai_move[0], ai_move[1])

            emit('ai_move', {
                'board': game.board,
                'ai_move': ai_move
            })
        
            if game.game_over:
                    emit('game_over', {'winner': game.win_message})

@socketio.on('restart_game')
def restart_game():
    # Reset the game state when the client requests a restart
    session['game'] = Gomoku()
    emit('game_restarted')

if __name__ == '__main__':
    socketio.run(app, debug=True)
