import pygame

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.BLUE = (0, 120, 255)
        
        # Game state
        self.state = "shopping"  # shopping, battle, results
        
        # Game board
        self.board_rows = 8
        self.board_cols = 6
        self.cell_size = 60
        self.board_offset_x = (self.screen_width - self.board_cols * self.cell_size) // 2
        self.board_offset_y = 50

    def update(self):
        # Handle game logic updates
        pass

    def draw(self):
        # Clear screen
        self.screen.fill(self.BLACK)
        
        # Draw game board
        for row in range(self.board_rows):
            for col in range(self.board_cols):
                rect = pygame.Rect(
                    self.board_offset_x + col * self.cell_size,
                    self.board_offset_y + row * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                pygame.draw.rect(self.screen, self.WHITE, rect, 1)