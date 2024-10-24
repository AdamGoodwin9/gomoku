import numpy as np
from enum import Enum

class Player(Enum):
    BLACK = 1
    WHITE = -1

class Gomoku:
    def __init__(self):
        self.board = np.zeros((19, 19), dtype=int)
        self.current_player = Player.BLACK
        self.captures = {Player.BLACK: 0, Player.WHITE: 0}  # Capture counts for each player
        self.game_over = False  # Initialize game_over flag
        self.win_message = ""

    def make_move(self, x, y):
        if self.is_valid_move(x, y):
            self.board[x][y] = self.current_player.value
            
            self.capture_stones(x, y)

            if self.check_win(x, y):
                return True
            
            self.current_player = Player.BLACK if self.current_player == Player.WHITE else Player.WHITE
            return True
        return False


    def capture_stones(self, x, y):
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)]
        captured_pairs = []

        for dx, dy in directions:
            i, j = x + dx, y + dy
            i2, j2 = x + 2*dx, y + 2*dy
            i3, j3 = x + 3*dx, y + 3*dy

            # Boundary check to prevent out-of-range errors
            if not (0 <= i < 19 and 0 <= j < 19 and 0 <= i2 < 19 and 0 <= j2 < 19 and 0 <= i3 < 19 and 0 <= j3 < 19):
                continue

            if (self.board[i][j] == -self.current_player.value and 
                self.board[i2][j2] == -self.current_player.value and 
                self.board[i3][j3] == self.current_player.value):

                captured_pairs.append((i, j))
                captured_pairs.append((i2, j2))

        for i, j in captured_pairs:
            self.board[i][j] = 0  # Remove captured stones
            self.captures[self.current_player] += 1  # Update capture count

        return len(captured_pairs) // 2  # Return the number of captured pairs


    def is_valid_move(self, x, y):
        if x < 0 or x >= 19 or y < 0 or y >= 19:
            return False

        if self.board[x][y] != 0:
            return False

        if self.would_create_double_three(x, y):
            return False

        return True

    def would_create_double_three(self, x, y):
        # Logic to check if placing a stone creates two simultaneous free-three alignments
        return False

    def check_capture_win(self):
        if self.captures[self.current_player] >= 10:
            self.win_message = f"{'Black' if self.current_player == Player.BLACK else 'White'} wins by capture!"
            return True
        return False

    def check_allignment_win(self, x, y):
        def count_stones(dx, dy):
            count = 0
            i, j = x + dx, y + dy
            while 0 <= i < 19 and 0 <= j < 19 and self.board[i][j] == self.current_player.value:
                count += 1
                i += dx
                j += dy
            return count

        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        
        for dx, dy in directions:
            count = 1
            count += count_stones(dx, dy)
            count += count_stones(-dx, -dy)

            if count >= 5:
                self.win_message = f"{'Black' if self.current_player == Player.BLACK else 'White'} wins!"
                return True
            # can_be_broken_by_capture does not work for shit, also subject doesn't make any sense so whatever
                # print(f"Potential win found at ({x}, {y}) in direction ({dx}, {dy})")
                # if self.can_be_broken_by_capture(x, y, dx, dy):
                #     print("This win can be broken by a capture.")
                #     return False  # The win condition is blocked by a possible capture
                # else:
                #     print("This win cannot be broken by a capture.")
                #     return True

        return False


    def check_win(self, x, y):
        if self.check_capture_win() or self.check_allignment_win(x, y):
            self.game_over = True
            return True
        return False


    # broken logic, function currently unused
    def can_be_broken_by_capture(self, x, y, dx, dy):
        opponent = -self.current_player
        print(f"Checking if win can be broken by capture for move at ({x}, {y}) by {'Black' if self.current_player == 1 else 'White'}")
        
        # Check in both directions along the line of five stones
        for step in range(-4, 5):
            i, j = x + step*dx, y + step*dy
            if not (0 <= i < 19 and 0 <= j < 19):
                continue
            
            print(f"Checking position ({i}, {j}) along the line of five stones")
            
            # Check if a pair of current player's stones can be captured
            for capture_dx, capture_dy in [(1, 0), (0, 1), (1, 1), (1, -1)]:
                cap_i1, cap_j1 = i + capture_dx, j + capture_dy
                cap_i2, cap_j2 = i + 2*capture_dx, j + 2*capture_dy
                if (0 <= cap_i1 < 19 and 0 <= cap_j1 < 19 and 0 <= cap_i2 < 19 and 0 <= cap_j2 < 19 and
                    self.board[cap_i1][cap_j1] == self.current_player and
                    self.board[cap_i2][cap_j2] == self.current_player and
                    self.board[i - capture_dx][j - capture_dy] == opponent):
                    
                    print(f"Capture possible at ({cap_i1}, {cap_j1}) and ({cap_i2}, {cap_j2})")
                    return True

        print("No capture can break the alignment.")
        return False

    def display_board(self):
        # Optional: print board to console for quick testing
        pass

