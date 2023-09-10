import pygame
from time import sleep

class Snake_part:
    """A base class for snake parts."""
    def __init__(self, ss_game):
        self.screen = ss_game.screen
        self.screen_rect = ss_game.screen.get_rect()
        self.settings = ss_game.settings
        self.color = self.settings.snake_color

        self.rect = pygame.Rect(0, 0, self.settings.bodysize, self.settings.bodysize)
        self.rect.center = self.screen_rect.center
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)
        self.previous_position = ''

    def draw_snake(self):
        """Draw the snake to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)


class Snake_head(Snake_part):
    def __init__(self, ss_game):
        super().__init__(ss_game)
        self.moving_up = False
        self.moving_down = False
        self.moving_right = False
        self.moving_left = False

        self.speed_factor = 1 #Default value, changes when pressing Space


        self.body = []

    def update_head(self):
        if self.moving_up:
            self.y -= self.settings.snake_speed * self.speed_factor
            if self.rect.top <= self.screen_rect.top:
                self.y = self.screen_rect.bottom - self.settings.headsize

        elif self.moving_down:
            self.y += self.settings.snake_speed * self.speed_factor
            if self.rect.top+self.settings.headsize >= self.screen_rect.bottom:
                self.y = self.screen_rect.top

        elif self.moving_right:
            self.x += self.settings.snake_speed * self.speed_factor
            if self.rect.left+self.settings.headsize >= self.screen_rect.right:
                self.x = self.screen_rect.left

        elif self.moving_left:
            self.x -= self.settings.snake_speed * self.speed_factor
            if self.rect.left <= self.screen_rect.left:
                self.x = self.screen_rect.right - self.settings.headsize
                
        self.previous_position = self.rect.copy()
        self.rect.y = self.y
        self.rect.x = self.x

    # Add a body part
    def grow_body(self, ss_game):
        i = 0
        while i < self.settings.growth_size:
            # Create the first body part
            if not self.body:
                new_body_part = Snake_body(ss_game, self)
            # Create subsequent body parts
            else: 
                new_body_part = Snake_body(ss_game, self.body[-1])

            self.body.append(new_body_part)
            i+=1


    # Update position of each body part
    def update_body(self):
        for index, body_part in enumerate(self.body):
            if index == 0:
                body_part.update_position(self.previous_position)
            else:
                body_part.update_position(self.body[index-1].previous_position)


class Snake_body(Snake_part):
    def __init__(self, ss_game, preceding_part):
        super().__init__(ss_game)

        self.update_position(preceding_part)

    # Update the position of a bady part
    def update_position(self, preceding_part):
        self.x = preceding_part.x
        self.y = preceding_part.y

        self.previous_position = self.rect.copy()

        self.rect.y = self.y
        self.rect.x = self.x
