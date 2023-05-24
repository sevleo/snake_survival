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
        self.previous_position = ''

        self.body = []

    # Update the position of the head
    def update(self):
        if self.moving_up:
            self.y -= self.settings.snake_speed
            if self.rect.bottom-self.settings.headsize < self.screen_rect.top:
                self.y = self.screen_rect.bottom

        elif self.moving_down:
            self.y += self.settings.snake_speed
            if self.rect.top+self.settings.headsize > self.screen_rect.bottom:
                self.y = self.screen_rect.top - self.settings.headsize


        elif self.moving_right:
            self.x += self.settings.snake_speed
            if self.rect.left+self.settings.headsize > self.screen_rect.right:
                self.x = self.screen_rect.left - self.settings.headsize

        elif self.moving_left:
            self.x -= self.settings.snake_speed
            if self.rect.right-self.settings.headsize < self.screen_rect.left:
                self.x = self.screen_rect.right
                
        self.previous_position = self.rect.copy()
        self.rect.y = self.y
        self.rect.x = self.x


    # Add a body part
    def grow_body(self, ss_game):
        # Create the first body part
        if not self.body:
            new_body_part = Snake_body(ss_game, self)
        # Create subsequent body parts
        else: 
           new_body_part = Snake_body(ss_game, self.body[-1])

        self.body.append(new_body_part)

    def update_body(self):
        for index, body_part in enumerate(self.body):
            if index == 0:
                body_part.update_position(self.previous_position)
            else:
                body_part.update_position(self.body[index-1].previous_position)

    
    def draw_snake(self):
        """Draw the snake to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)