import pygame
from time import sleep

class Snake_body:
    """A class to manage body parts of the snake."""

    def __init__(self, ss_game, preceding_part):
        """Initialize a body part and set its starting position."""
        self.screen = ss_game.screen
        self.screen_rect = ss_game.screen.get_rect()
        self.settings = ss_game.settings
        self.color = self.settings.snake_color
        self.margin = self.settings.snake_body_margin
        
        self.rect = pygame.Rect(0, 0, self.settings.bodysize, self.settings.bodysize) 
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)
        self.previous_position = ''

        self.update_position(preceding_part)


    def update_position(self, preceding_part):
        self.x = preceding_part.x
        self.y = preceding_part.y

        self.previous_position = self.rect.copy()

        self.rect.y = self.y
        self.rect.x = self.x


    def draw_body_part(self):
        pygame.draw.rect(self.screen, self.color, self.rect)