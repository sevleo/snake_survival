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
        self.prep_enemies_count()
        self.prep_high_score()

 

    def prep_snake_speed(self):
        """Turn the snake speed into a rendered image."""
        snake_speed = round(self.settings.snake_speed, 2)
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
        self.snake_size_rect = self.snake_size_image.get_rect()
        self.snake_size_rect.right = self.snake_speed_rect.left - 20
        self.snake_size_rect.top = 20

    def prep_enemies_count(self):
        """Turn the enemy snakes count into a rendered image."""
        enemies_count = self.settings.enemy_snake_count
        enemies_count_str = f"Enemies count: {enemies_count}"
        self.enemies_count_image = self.font.render(enemies_count_str, True, self.text_color, self.settings.bg_color)

        # Display the snake size at the top right of the screen.
        self.enemies_count_rect = self.enemies_count_image.get_rect()
        self.enemies_count_rect.right = self.snake_size_rect.left - 20
        self.enemies_count_rect.top = 20

    def prep_high_score(self):
        high_score = self.settings.high_score
        high_score_str = f"High Score: {high_score}"
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, (0, 255, 25))
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.bottom = self.ss_game.play_button.rect.top
        self.high_score_rect.centerx = self.ss_game.play_button.msg_image_rect.centerx

    def draw_score(self):
        """Draw score to the screen."""
        self.screen.blit(self.snake_speed_image, self.snake_speed_rect)
        self.screen.blit(self.snake_size_image, self.snake_size_rect)
        self.screen.blit(self.enemies_count_image, self.enemies_count_rect)
    
    def draw_high_score(self):
        self.screen.blit(self.high_score_image, self.high_score_rect)