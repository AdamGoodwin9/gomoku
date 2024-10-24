# ai.py

def is_there_another_in_radius(board, i, j, radius):
    for c in range(max(i - radius, 0), min(i + radius + 1, len(board))):
        for r in range(max(j - radius, 0), min(j + radius + 1, len(board[0]))):
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
        if board[9][9] == 0:
            return [(9,9)]
        else:
            print('explosion')
    
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
    #define function here: func(board, depth, is_maximizing_player, player, alpha=float('-inf'), beta=float('inf'))
    if depth == 0 or game_over(board):
        return evaluate_position(board)  # Evaluate the board state if depth is 0 or game ends
    
#define dictionary: key = move, value = eval

    if is_maximizing_player:
        max_eval = float('-inf')
        for move in get_all_valid_moves(board):
            #spawn thread 
            #wrap all this in a function, Thread(target=thatFunc, args=tuple of move -> eval)
            make_move(board, move[0], move[1], player)
            eval = minimax(board, depth - 1, False, -player, alpha, beta)  # Recurse for the opponent
            undo_move(board, move[0], move[1])
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:  # Prune branch
                break
            #kill thread
            #threads will be adding move-eval pairs to the dictionary
        #return max(dictionary.values())
        return max_eval
    else:
        min_eval = float('inf')
        for move in get_all_valid_moves(board):
            make_move(board, move[0], move[1], player)
            eval = minimax(board, depth - 1, True, -player, alpha, beta)  # Recurse for the AI
            undo_move(board, move[0], move[1])
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:  # Prune branch
                break
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
                #spawn thread for next two lines
                player = board[i][j]  # 1 for AI, -1 for opponent
                score += evaluate_patterns(board, i, j, player, directions)
    
    return score

def evaluate_patterns(board, x, y, player, directions):
    score = 0
    for dx, dy in directions:
        consecutive_stones, consecutive_spaces_f, consecutive_spaces_b = count_consecutive_spaces_or_stones(board, x, y, dx, dy, player)
        
        if consecutive_stones >= 5:
            return 1000000 * player # Winning move
        
        if consecutive_stones == 4:
            if consecutive_spaces_f >= 1 and consecutive_spaces_b >= 1:
                score += 100000 * player  # Strong position
            else: # maximum of one side can be free - opponent will block
                score += 0
        elif consecutive_stones == 3:
            if consecutive_spaces_f >= 2 and consecutive_spaces_b >= 2:
                score += 200 * player
            elif   (consecutive_spaces_f >= 2 and consecutive_spaces_b == 1) \
                or (consecutive_spaces_b >= 2 and consecutive_spaces_f == 1):
                score += 100 * player
            else:
                score += 0
        elif consecutive_stones == 2:
            if consecutive_spaces_f >= 3 and consecutive_spaces_b >= 3:
                score += 20 * player  # Developing position
            elif   (consecutive_spaces_f >= 3 and consecutive_spaces_b == 2) \
                or (consecutive_spaces_b >= 3 and consecutive_spaces_f == 2):
                score += 10 * player
            else:
                score += 0 * player
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

def count_consecutive_spaces_or_stones(board, x, y, dx, dy, player):
    stone_count = 0
    open_count_forward = 0
    open_count_backward = 0
    eval_forward = True
    eval_backward = True
    for step in range(5):
        i, j = x + step * dx, y + step * dy
        if eval_forward:
            if 0 <= i < 19 and 0 <= j < 19 and board[i][j] == player:
                stone_count += 1
            elif 0 <= i < 19 and 0 <= j < 19 and board[i][j] == 0:
                open_count_forward += 1
            else:
                eval_forward = False

        if step >= 1 and eval_backward:
            k, l = x - step * dx, y - step * dy
            if 0 <= k < 19 and 0 <= l < 19 and board[k][l] == player:
                stone_count += 1
            elif 0 <= k < 19 and 0 <= l < 19 and board[k][l] == 0:
                open_count_backward += 1
            else:
                eval_backward = False
    return (stone_count, open_count_forward, open_count_backward)

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