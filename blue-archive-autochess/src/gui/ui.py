import pygame

class UI:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)

    def draw_button(self, text, x, y, width, height, color, hover_color):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x + width and y < mouse[1] < y + height:
            pygame.draw.rect(self.screen, hover_color, (x, y, width, height))
            if click[0] == 1:  # Left mouse button clicked
                return True
        else:
            pygame.draw.rect(self.screen, color, (x, y, width, height))

        button_text = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(button_text, (x + (width / 2 - button_text.get_width() / 2), 
                                        y + (height / 2 - button_text.get_height() / 2)))
        return False

    def draw_text(self, text, x, y):
        text_surface = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(text_surface, (x, y))