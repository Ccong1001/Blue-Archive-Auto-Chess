import pygame
from game.game import Game

def main():
    pygame.init()
    
    # Set up the game window
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Blue Archive Auto Chess")

    # Create a game instance
    game = Game(screen)

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        game.update()
        game.draw()
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()