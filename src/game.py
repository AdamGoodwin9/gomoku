import os
import pygame
from gomoku import Gomoku
from ai import find_best_move  # Assuming you have implemented the AI logic here.

def show_menu():
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    font = pygame.font.SysFont(None, 50)
    menu_active = True
    
    while menu_active:
        screen.fill((222, 184, 135))  # GOBAN color

        # Title
        title = font.render("Gomoku - Choose Game Mode", True, (0, 0, 0))
        screen.blit(title, (200, 100))

        # Player vs Player Option
        pvp_option = font.render("1. Player vs Player", True, (0, 0, 0))
        screen.blit(pvp_option, (200, 200))

        # Player vs AI Option (Play as Black or White)
        pve_option_black = font.render("2. Player vs AI (Play as Black)", True, (0, 0, 0))
        screen.blit(pve_option_black, (200, 300))
        
        pve_option_white = font.render("3. Player vs AI (Play as White)", True, (0, 0, 0))
        screen.blit(pve_option_white, (200, 400))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "pvp"  # Player vs Player
                elif event.key == pygame.K_2:
                    return "pve_black"  # Player vs AI (Player as Black)
                elif event.key == pygame.K_3:
                    return "pve_white"  # Player vs AI (Player as White)


# The main game loop
def main():
    os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
    
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Gomoku")

    # Define board layout constants
    MARGIN = 40  # Margin around the board
    GRID_SIZE = 800 - 2 * MARGIN  # Grid size for 19x19 board within the margin
    CELL_SIZE = GRID_SIZE // 18  # Each cell's size (spacing between lines)

    # Show the menu and get the game mode
    game_mode = show_menu()

    # Initialize game
    game = Gomoku()
    game.game_over = False  # Initialize game_over flag
    game.win_message = ""

    # Set up the display fonts
    font = pygame.font.SysFont(None, 74)
    small_font = pygame.font.SysFont(None, 50)

    # Set up colors
    purple = (153, 0, 255)
    black_color = (0, 0, 0)
    white_color = (255, 255, 255)

    running = True
    current_player = 1  # 1 for Black, -1 for White

    # AI settings
    ai_enabled = False
    player_color = None

    if game_mode == "pve_black":
        ai_enabled = True
        player_color = 1  # Player is Black, AI is White
    elif game_mode == "pve_white":
        ai_enabled = True
        player_color = -1  # Player is White, AI is Black

    # Main game loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and not game.game_over:
                if ai_enabled and current_player == player_color:
                    # Player's turn when playing vs AI
                    x, y = pygame.mouse.get_pos()
                    grid_x = round((x - MARGIN) / CELL_SIZE)
                    grid_y = round((y - MARGIN) / CELL_SIZE)

                    if game.board[grid_x][grid_y] == 0:
                        game.make_move(grid_x, grid_y)
                        
                        if not game.game_over:
                            current_player *= -1  # Switch to AI

                elif game_mode == "pvp" or current_player == player_color:
                    # Player vs Player or Player's turn in PvE
                    x, y = pygame.mouse.get_pos()
                    grid_x = round((x - MARGIN) / CELL_SIZE)
                    grid_y = round((y - MARGIN) / CELL_SIZE)
                    game.make_move(grid_x, grid_y)

                    current_player *= -1  # Switch turn

        # AI's turn
        if ai_enabled and current_player != player_color and not game.game_over:
            best_move = find_best_move(game.board, current_player)  # AI move generation
            game.make_move(best_move[0], best_move[1])

            current_player *= -1  # Switch turn
            
        # Draw the board and game elements (Grid, Stones, Capture Counts, etc.)
        screen.fill((222, 184, 135))  # GOBAN background color

        # Draw the grid
        for i in range(19):
            pygame.draw.line(screen, black_color,
                             (MARGIN + i * CELL_SIZE, MARGIN),
                             (MARGIN + i * CELL_SIZE, MARGIN + GRID_SIZE))
            pygame.draw.line(screen, black_color,
                             (MARGIN, MARGIN + i * CELL_SIZE),
                             (MARGIN + GRID_SIZE, MARGIN + i * CELL_SIZE))

        # Draw the stones
        for i in range(19):
            for j in range(19):
                if game.board[i][j] == 1:  # Black stone
                    pygame.draw.circle(screen, black_color,
                                       (MARGIN + i * CELL_SIZE, MARGIN + j * CELL_SIZE), 10)
                elif game.board[i][j] == -1:  # White stone
                    pygame.draw.circle(screen, white_color,
                                       (MARGIN + i * CELL_SIZE, MARGIN + j * CELL_SIZE), 10)
        
        # Display the capture counts 
        black_capture_text = small_font.render(str(game.captures[1]), True, black_color)
        white_capture_text = small_font.render(str(game.captures[-1]), True, white_color)

        # Adjust positions to be closer to the corners
        screen.blit(black_capture_text, (MARGIN // 4, MARGIN // 4))  # Top left for black
        screen.blit(white_capture_text, (800 - MARGIN // 4 - white_capture_text.get_width(), MARGIN // 4))  # Top right for white

        # Check if game is over and display win message if necessary
        if game.game_over:
            text_surface = font.render(game.win_message, True, purple)
            text_rect = text_surface.get_rect(center=(400, 400))
            screen.blit(text_surface, text_rect)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
