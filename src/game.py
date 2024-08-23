import os
import pygame
from gomoku import Gomoku

# Set the environment variable to place the window at the top-left corner
os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Gomoku")

# Define the GOBAN color and margin
GOBAN = (222, 184, 135)
MARGIN = 40  # Define a margin of 40 pixels
GRID_SIZE = 800 - 2 * MARGIN  # The size of the grid area inside the margins
CELL_SIZE = GRID_SIZE // 18  # Size of each cell in the grid

# Initialize game
game = Gomoku()
game.game_over = False  # Initialize game_over flag
game.win_message = ""  # Initialize the win message

# Set up the font for the win message and capture count display
font = pygame.font.SysFont(None, 74)
small_font = pygame.font.SysFont(None, 50)  # Smaller font for capture counts
purple = (153, 0, 255)  # Color for the win message
black_color = (0, 0, 0)  # Color for the black stone's capture count
white_color = (255, 255, 255)  # Color for the white stone's capture count

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not game.game_over:
            # Get mouse position and convert to nearest grid intersection coordinates
            x, y = pygame.mouse.get_pos()

            # Adjust coordinates based on the margin and cell size
            grid_x = round((x - MARGIN) / CELL_SIZE)
            grid_y = round((y - MARGIN) / CELL_SIZE)
            
            # Make the move with the calculated grid coordinates
            game.make_move(grid_x, grid_y)

    # Fill the board with the GOBAN color
    screen.fill(GOBAN)
    
    # Drawing the grid lines with the margin
    for i in range(19):
        pygame.draw.line(screen, (0, 0, 0), 
                         (MARGIN + i * CELL_SIZE, MARGIN), 
                         (MARGIN + i * CELL_SIZE, MARGIN + GRID_SIZE))
        pygame.draw.line(screen, (0, 0, 0), 
                         (MARGIN, MARGIN + i * CELL_SIZE), 
                         (MARGIN + GRID_SIZE, MARGIN + i * CELL_SIZE))

    # Drawing stones on intersections including edges
    for i in range(19):
        for j in range(19):
            if game.board[i][j] == 1:
                pygame.draw.circle(screen, (0, 0, 0), 
                                   (MARGIN + i * CELL_SIZE, 
                                    MARGIN + j * CELL_SIZE), 10)
            elif game.board[i][j] == -1:
                pygame.draw.circle(screen, (255, 255, 255), 
                                   (MARGIN + i * CELL_SIZE, 
                                    MARGIN + j * CELL_SIZE), 10)

    # Display the capture counts
    black_capture_text = small_font.render(str(game.captures[1]), True, black_color)
    white_capture_text = small_font.render(str(game.captures[-1]), True, white_color)

    # Adjust positions to be closer to the corners
    screen.blit(black_capture_text, (MARGIN // 4, MARGIN // 4))  # Top left for black
    screen.blit(white_capture_text, (800 - MARGIN // 4 - white_capture_text.get_width(), MARGIN // 4))  # Top right for white

    # If the game is over, display the win message
    if game.game_over:
        text_surface = font.render(game.win_message, True, purple)
        text_rect = text_surface.get_rect(center=(400, 400))  # Center the text on the board
        screen.blit(text_surface, text_rect)

    pygame.display.flip()

pygame.quit()
