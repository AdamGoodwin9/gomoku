from flask import Flask, render_template, session
from flask_socketio import SocketIO, emit
from gomoku import Gomoku, Player  # Import the Gomoku class and Player enum
from ai import find_best_move  # Assuming AI logic is in ai.py

app = Flask(__name__, static_folder='docs', template_folder='docs')
app.secret_key = 'gomoku_gaming_glory_goomba_guacamole'  # Simple secret key for development
socketio = SocketIO(app)

@app.route('/')
def index():
    session['game_state'] = None  # Clear any existing game state when the page is loaded
    session['mode'] = None  # Store game mode (pvp, pve_black, pve_white)
    return render_template('index.html')

@socketio.on('start_game')
def start_game(data):
    # Create a new game instance
    game = Gomoku()
    # Store the game mode
    session['mode'] = data['game_mode']
    # Save the initial game state to the session
    save_game_state(game)
    # Notify the client that the game has started
    emit('game_started', {
        'board': game.board,
        'currentPlayer': game.current_player.value
    })

    if session['mode'] == 'pve_white':
        ai_player = Player.WHITE
        ai_move = find_best_move(game.board, ai_player.value)
        if ai_move:
            game.make_move(ai_move[0], ai_move[1])
            # Save the updated game state after AI move
            save_game_state(game)
            # Emit the AI's move to the client
            emit('ai_move', {
                'board': game.board,
                'ai_move': ai_move,
                'currentPlayer': game.current_player.value
            })

@socketio.on('player_move')
def handle_player_move(data):
    x, y = data['move']
    game = load_game_state()  # Load the game state from the session
    mode = session.get('mode')

    if not game:
        emit('error', {'message': 'Game not initialized.'})
        return

    if game.make_move(x, y):
        # Save the updated game state
        save_game_state(game)
        # Emit the updated board to the client
        emit('board_update', {
            'board': game.board,
            'currentPlayer': game.current_player.value,
            'blackCaptures': game.captures[Player.BLACK],
            'whiteCaptures': game.captures[Player.WHITE]
        })

        # Check if the game is over after the player's move
        if game.game_over:
            emit('game_over', {'winner': game.win_message})
            return

        # If in PvE mode, let the AI make its move
        if mode in ['pve_black', 'pve_white']:
            ai_player = Player.WHITE if mode == 'pve_black' else Player.BLACK
            ai_move = find_best_move(game.board, ai_player.value)
            if ai_move:
                game.make_move(ai_move[0], ai_move[1])
                # Save the updated game state after AI move
                save_game_state(game)
                # Emit the AI's move to the client
                emit('ai_move', {
                    'board': game.board,
                    'ai_move': ai_move,
                    'currentPlayer': game.current_player.value
                })

                # Check if the game is over after the AI's move
                if game.game_over:
                    emit('game_over', {'winner': game.win_message})

@socketio.on('restart_game')
def restart_game():
    game = Gomoku()
    save_game_state(game)
    emit('board_update', {
        'board': game.board,
        'currentPlayer': game.current_player.value,
        'blackCaptures': game.captures[Player.BLACK],
        'whiteCaptures': game.captures[Player.WHITE]
    })

@socketio.on('end_game')
def end_game():
    session['game_state'] = None
    session['mode'] = None

def save_game_state(game):
    session['game_state'] = {
        'board': game.board,
        'current_player': game.current_player.value,  # Save enum as value
        'captures': game.captures,
        'game_over': game.game_over,
        'win_message': game.win_message
    }


def load_game_state():
    if 'game_state' not in session or session['game_state'] is None:
        print("No game state in session, returning None")
        return None
    game_state = session['game_state']
    game = Gomoku()
    game.board = game_state['board']
    game.current_player = Player(game_state['current_player'])  # Reconstruct enum
    game.captures = game_state['captures']
    game.game_over = game_state.get('game_over', False)
    game.win_message = game_state.get('win_message', '')
    return game

if __name__ == '__main__':
    socketio.run(app, debug=True)
