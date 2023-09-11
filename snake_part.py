import pygame
from time import sleep
from random import choice, randint

class SnakePart:
    """A base class for snake parts."""
    def __init__(self, ss_game):
        self.screen = ss_game.screen
        self.screen_rect = ss_game.screen.get_rect()
        self.settings = ss_game.settings
        self.color = self.settings.snake_color

        self.define_rect()

        self.previous_position = ''

    def draw_snake(self):
        """Draw the snake to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)

    def define_rect(self):
        self.rect = pygame.Rect(0, 0, self.settings.bodysize, self.settings.bodysize)
        self.rect.center = self.screen_rect.center
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)


class SnakeHead(SnakePart):
    def __init__(self, ss_game):
        super().__init__(ss_game)
        self.moving_up = False
        self.moving_down = False
        self.moving_right = False
        self.moving_left = False

        self.left_eye_rect = pygame.Rect(0, 0, self.settings.eye_width, self.settings.eye_height)
        self.right_eye_rect = pygame.Rect(0, 0, self.settings.eye_width, self.settings.eye_height)

        self.update_eyes()
        self.body = []
        self.grow_body(self)
    
    def update_eyes(self, direction="up"):
        if direction == "up":
            self.left_eye_rect.centerx = self.rect.centerx - 5
            self.left_eye_rect.centery = self.rect.centery - 2
            self.right_eye_rect.centerx = self.rect.centerx + 5
            self.right_eye_rect.centery = self.rect.centery - 2
        if direction == "down":
            self.left_eye_rect.centerx = self.rect.centerx - 5 
            self.left_eye_rect.centery = self.rect.centery + 2 
            self.right_eye_rect.centerx = self.rect.centerx + 5
            self.right_eye_rect.centery = self.rect.centery + 2
        if direction == "right":
            self.left_eye_rect.centerx = self.rect.centerx + 2 
            self.left_eye_rect.centery = self.rect.centery - 5 
            self.right_eye_rect.centerx = self.rect.centerx + 2
            self.right_eye_rect.centery = self.rect.centery + 5
        if direction == "left":
            self.left_eye_rect.centerx = self.rect.centerx - 2 
            self.left_eye_rect.centery = self.rect.centery - 5 
            self.right_eye_rect.centerx = self.rect.centerx - 2
            self.right_eye_rect.centery = self.rect.centery + 5

    def draw_eyes(self):
        pygame.draw.rect(self.screen, (255,0,0), self.left_eye_rect)
        pygame.draw.rect(self.screen, (255,0,0), self.right_eye_rect)

    def update_head(self):
        if self.moving_up:
            self.y -= self.settings.snake_speed
            if self.rect.top <= self.screen_rect.top:
                self.y = self.screen_rect.bottom - self.settings.headsize
            self.update_eyes("up")

        elif self.moving_down:
            self.y += self.settings.snake_speed
            if self.rect.top+self.settings.headsize >= self.screen_rect.bottom:
                self.y = self.screen_rect.top
            self.update_eyes("down")

        elif self.moving_right:
            self.x += self.settings.snake_speed
            if self.rect.left+self.settings.headsize >= self.screen_rect.right:
                self.x = self.screen_rect.left
            self.update_eyes("right")

        elif self.moving_left:
            self.x -= self.settings.snake_speed
            if self.rect.left <= self.screen_rect.left:
                self.x = self.screen_rect.right - self.settings.headsize
            self.update_eyes("left")
                
        self.previous_position = self.rect.copy()
        self.rect.y = self.y
        self.rect.x = self.x
        

    # Add a body part
    def grow_body(self, ss_game):
        i = 0
        while i < self.settings.growth_size:
            # Create the first body part
            if not self.body:
                new_body_part = SnakeBody(ss_game, self)
            # Create subsequent body parts
            else: 
                new_body_part = SnakeBody(ss_game, self.body[-1])

            self.body.append(new_body_part)
            i+=1


    # Update position of each body part
    def update_body(self):
        for index, body_part in enumerate(self.body):
            if index == 0:
                body_part.update_position(self.previous_position)
            else:
                body_part.update_position(self.body[index-1].previous_position)


    def reset_snake(self):
        self.rect.center = self.screen_rect.center
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)
        self.draw_snake()
        self.draw_eyes()
        self.update_eyes()
        self.body = []
        self.grow_body(self)



class SnakeBody(SnakePart):
    def __init__(self, ss_game, preceding_part, color=None):
        super().__init__(ss_game)
        if color:
            self.color = color
        self.update_position(preceding_part)

    # Update the position of a bady part
    def update_position(self, preceding_part):
        self.x = preceding_part.x
        self.y = preceding_part.y

        self.previous_position = self.rect.copy()

        self.rect.y = self.y
        self.rect.x = self.x


class EnemySnake(SnakeHead):
    def __init__(self, ss_game):
        super().__init__(ss_game)
        self.color = self.settings.enemy_snake_color

        self.tick_counter = 0
        self.direction_change_interval = 100
        self.x_direction = 1
        self.y_direction = 1
        self.direction = "right"

    def define_rect(self):
        self.rect = pygame.Rect(0, 0, self.settings.bodysize, self.settings.bodysize)
        self.rect.y = self.screen_rect.y + 100
        self.rect.x = self.screen_rect.x + 100
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

    def update_head(self):
        if self.tick_counter == self.direction_change_interval:
            if self.direction == "right":
                self.direction = choice(['right', 'top', 'bottom'])
            elif self.direction == "left":
                self.direction = choice(['left', 'top', 'bottom'])
            elif self.direction == "top":
                self.direction = choice(['right', 'left', 'top'])
            elif self.direction == "bottom":
                self.direction = choice(['right', 'bottom', 'left'])
            self.tick_counter = 0

        if self.direction == "right":
            self.x = self.x + self.settings.enemy_snake_speed
            if self.rect.left+self.settings.headsize >= self.screen_rect.right:
                self.x = self.screen_rect.left
        elif self.direction == "left":
            self.x = self.x - self.settings.enemy_snake_speed
            if self.rect.left <= self.screen_rect.left:
                self.x = self.screen_rect.right - self.settings.headsize
        elif self.direction == "bottom":
            self.y = self.y + self.settings.enemy_snake_speed
            if self.rect.top+self.settings.headsize >= self.screen_rect.bottom:
                self.y = self.screen_rect.top
        elif self.direction == "top":
            self.y = self.y - self.settings.enemy_snake_speed
            if self.rect.top <= self.screen_rect.top:
                self.y = self.screen_rect.bottom - self.settings.headsize

        self.previous_position = self.rect.copy()
        self.rect.y = self.y
        self.rect.x = self.x
        self.tick_counter += 1

    # Add a body part
    def grow_body(self, ss_game):
        size = randint(25, 250)
        i = 0
        while i < size:
            # Create the first body part
            if not self.body:
                new_body_part = SnakeBody(ss_game, self, self.settings.enemy_snake_color)
            # Create subsequent body parts
            else: 
                new_body_part = SnakeBody(ss_game, self.body[-1], self.settings.enemy_snake_color)

            self.body.append(new_body_part)
            i+=1