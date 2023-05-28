import random
import pygame

class Food:
    """A class to manage food."""

    def __init__(self, ss_game):
        """Initialize a food unit."""
        self.game = ss_game
        self.snake = ss_game.snake

        self.screen = ss_game.screen
        self.screen_rect = ss_game.screen.get_rect()
        self.settings = ss_game.settings
        self.color = self.settings.food_color
        self.rect = pygame.Rect(0, 0, self.settings.foodsize, self.settings.foodsize)
        self.generate_food()
        
        
    def generate_food(self):
        self.rect.x = random.randint(15, self.settings.screen_width-15)
        self.rect.y = random.randint(15, self.settings.screen_height-15)


    def draw_food(self):
        pygame.draw.rect(self.screen, self.color, self.rect)