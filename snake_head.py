import pygame
from snake_body import Snake_body

class Snake_head:
    """A class to manage the snake."""

    def __init__(self, ss_game):
        """Initialize the snake and set its starting position."""
        self.screen = ss_game.screen
        self.screen_rect = ss_game.screen.get_rect()
        self.settings = ss_game.settings
        self.color = self.settings.snake_color
        self.moving_up = False
        self.moving_down = False
        self.moving_right = False
        self.moving_left = False

        self.rect = pygame.Rect(0, 0, self.settings.headsize, self.settings.headsize)
        self.rect.center = self.screen_rect.center
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

        self.body = []


    def update(self):
        if self.moving_up == True:
            if self.rect.bottom < self.screen_rect.top:
                self.y = self.screen_rect.bottom
                self.y -= self.settings.snake_speed
            else: 
                self.y -= self.settings.snake_speed

        elif self.moving_down == True:
            if self.rect.top > self.screen_rect.bottom:
                self.y = self.screen_rect.top - self.settings.headsize
                self.y += self.settings.snake_speed
            else:
                self.y += self.settings.snake_speed

        elif self.moving_right == True:
            if self.rect.left > self.screen_rect.right:
                self.x = self.screen_rect.left - self.settings.headsize
                self.x += self.settings.snake_speed
            else:
                self.x += self.settings.snake_speed

        elif self.moving_left == True:
            if self.rect.right < self.screen_rect.left:
                self.x = self.screen_rect.right
                self.x -= self.settings.snake_speed
            else:
                self.x -= self.settings.snake_speed

        self.rect.y = self.y
        self.rect.x = self.x

    
    def grow_body(self, ss_game):
        if not self.body:
            new_body_part = Snake_body(ss_game, self)
            print(f"getting head {self}")
        else: 
            new_body_part = Snake_body(ss_game, self.body[-1])
            print(f"getting preceding body part {self.body[-1]}")


        self.body.append(new_body_part)

    
    def draw_snake(self):
        """Draw the snake to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)