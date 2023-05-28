import random
import pygame

class Food:
    """A class to manage food."""

    def __init__(self, ss_game):
        """Initialize a food unit."""
        self.screen = ss_game.screen
        self.screen_rect = ss_game.screen.get_rect()
        self.settings = ss_game.settings
        self.color = self.settings.food_color

        self.rect = pygame.Rect(0, 0, self.settings.headsize, self.settings.headsize)
        self.rect.center = self.screen_rect.center
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)
        self.previous_position = ''