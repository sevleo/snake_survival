import pygame.font
from snake_part import SnakeHead


class Scoreboard:
    """A class to report scoring information."""

    def __init__(self, ss_game):
        """Initialize scorekeeping attributes."""
        self.ss_game = ss_game
        self.screen = ss_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ss_game.settings
        

        # Font settings for scoring information.
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont("monospace", 20)
        
        self.prep_images()

    def prep_images(self):
        self.prep_snake_speed()
        self.prep_snake_size()

 

    def prep_snake_speed(self):
        """Turn the snake speed into a rendered image."""
        snake_speed = round(self.settings.snake_speed, 1)
        snake_speed_str = f"Speed: {snake_speed}"
        self.snake_speed_image = self.font.render(snake_speed_str, True, self.text_color, self.settings.bg_color)

        # Display the snake speed at the top right of the screen.
        self.snake_speed_rect = self.snake_speed_image.get_rect()
        self.snake_speed_rect.right = self.screen_rect.right - 20
        self.snake_speed_rect.top = 20

    def prep_snake_size(self):
        """Turn the snake size into a rendered image."""
        snake_size = self.settings.snake_size
        snake_size_str = f"Size: {snake_size}"
        self.snake_size_image = self.font.render(snake_size_str, True, self.text_color, self.settings.bg_color)

        # Display the snake size at the top right of the screen.
        self.snake_size_rect = self.snake_speed_image.get_rect()
        self.snake_size_rect.right = self.snake_speed_rect.left - 20
        self.snake_size_rect.top = 20

    def show_score(self):
        """Draw score to the screen."""
        self.screen.blit(self.snake_speed_image, self.snake_speed_rect)
        self.screen.blit(self.snake_size_image, self.snake_size_rect)
