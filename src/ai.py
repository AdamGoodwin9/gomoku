# ai.py

def is_there_another_in_radius(board, i, j, radius):
    for c in range(max(i - radius, 0), min(i + radius, len(board) - 1)):
        for r in range(max(j - radius, 0), min(j + radius, len(board[0]) - 1)):
            if board[c][r] != 0:
                return True
    return False

def filtered_valid_moves(board):
    valid_moves = []
    radius = 1
    for i in range(19):
        for j in range(19):
            if board[i][j] == 0 and is_there_another_in_radius(board, i, j, radius):  # Empty spot
                valid_moves.append((i, j))
    if valid_moves == []:
        if board[10][10] == 0:
            return [(10,10)]
        else:
            return get_all_valid_moves_old(board)
    
    return valid_moves


def get_all_valid_moves(board):
    return filtered_valid_moves(board)


# Helper function to get all valid moves
def get_all_valid_movesa(board):
    valid_moves = []
    for i in range(19):
        for j in range(19):
            if board[i][j] == 0:  # Empty spot
                valid_moves.append((i, j))
    return valid_moves

# Helper function to make a move
def make_move(board, x, y, player):
    board[x][y] = player  # Place the player's stone (1 for black, -1 for white)

# Helper function to undo a move
def undo_move(board, x, y):
    board[x][y] = 0  # Reset the position to empty

def minimax(board, depth, is_maximizing_player, player, alpha=float('-inf'), beta=float('inf')):
    if depth == 0 or game_over(board):
        return evaluate_position(board)  # Evaluate the board state if depth is 0 or game ends
    
    if is_maximizing_player:
        max_eval = float('-inf')
        for move in get_all_valid_moves(board):
            make_move(board, move[0], move[1], player)
            eval = minimax(board, depth - 1, False, -player, alpha, beta)  # Recurse for the opponent
            undo_move(board, move[0], move[1])
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            # if beta <= alpha:  # Prune branch
            #     break
        return max_eval
    else:
        min_eval = float('inf')
        for move in get_all_valid_moves(board):
            make_move(board, move[0], move[1], player)
            eval = minimax(board, depth - 1, True, -player, alpha, beta)  # Recurse for the AI
            undo_move(board, move[0], move[1])
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            # if beta <= alpha:  # Prune branch
            #     break
        return min_eval

# contender (found )
def evaluate_position1(board):
    score = 0
    for col in board:
        for p in col:
            score += p
    return score

# worst heuristic functions world record holder (found below)
def evaluate_position(board):
    score = 0
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # Horizontal, Vertical, Diagonal
    
    for i in range(19):
        for j in range(19):
            if board[i][j] != 0:  # Only evaluate if there's a stone here
                player = board[i][j]  # 1 for AI, -1 for opponent
                score += evaluate_patterns(board, i, j, player, directions)
    
    return score

def evaluate_patterns(board, x, y, player, directions):
    score = 0
    for dx, dy in directions:
        consecutive_stones = count_consecutive_stones(board, x, y, dx, dy, player)
        # print(f"consec stones: {consecutive_stones} for {player}")
        
        if consecutive_stones >= 5:
            score += 10000 * player  # Winning move
        if consecutive_stones == 4:
            score += 1000 * player  # Strong position
        elif consecutive_stones == 3:
            score += 100 * player  # Good position
        elif consecutive_stones == 2:
            score += 10 * player  # Developing position
    return score

def count_consecutive_stones(board, x, y, dx, dy, player):
    count = 0
    for step in range(5):
        i, j = x + step * dx, y + step * dy
        if 0 <= i < 19 and 0 <= j < 19 and board[i][j] == player:
            count += 1
        else:
            break
    return count

def game_over(board):
    # Check if any player has won
    for i in range(19):
        for j in range(19):
            if board[i][j] != 0:
                if check_win(board, i, j, board[i][j]):
                    print("its joever")
                    return True

    # Check if the board is full (draw)
    if all(board[i][j] != 0 for i in range(19) for j in range(19)):
        print("its COMPLETELY joever")
        return True
    
    return False

def check_win(board, x, y, player):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # Horizontal, Vertical, Diagonal
    
    for dx, dy in directions:
        if count_consecutive_stones(board, x, y, dx, dy, player) >= 5:
            return True
    
    return False

# Find the best move for the AI using Minimax
def find_best_move(board, player):
    best_move = None
    if player == 1:
        best_value = float('-inf')
    else: 
        best_value = float('+inf')

    print('begin')
    for move in get_all_valid_moves(board):
        make_move(board, move[0], move[1], player)
        move_value = minimax(board, 2, False, -player)  # Limiting depth to 3
        # move_value = evaluate_position(board)  # Limiting depth to 3
        print(f'Move: {move}, score: {move_value}')
        undo_move(board, move[0], move[1])
        
        if player == 1:
            if move_value > best_value:
                best_value = move_value
                best_move = move
        else: 
            if move_value < best_value:
                best_value = move_value
                best_move = move
    
    return best_move