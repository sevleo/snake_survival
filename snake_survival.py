import sys
import pygame
from settings import Settings
from snake_part import SnakeHead, EnemySnake
from food import Food
from scoreboard import Scoreboard
from button import Button
from time import sleep

class SnakeSurvival:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()

        self.game_active = False

        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        pygame.display.set_caption("Snake Survival")
        self.screen_rect = self.screen.get_rect()
        
        self.sb = Scoreboard(self)
        self.snake = SnakeHead(self)

        self.enemy_snakes = []

        for _ in range(self.settings.enemy_snake_count_default):
            enemy_snake = EnemySnake(self)
            self.enemy_snakes.append(enemy_snake)

        self.food = Food(self)

        self.leading_rect_direction = ""

        self.play_button = Button(self,  "Play")

        
        

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            if self.game_active:
                self.snake.update_head()
                self.snake.update_body()

                for snake in self.enemy_snakes:
                    snake.update_head()
                    snake.update_body()

                self._check_food_collision()
                self._check_body_collision()
            self._update_screen()
            self.clock.tick(self.settings.tick_value)


    def _start_game(self):
        self.game_active = True
        self.sb.prep_images()
        self.sb.show_score()

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)


    def _check_keydown_events(self, event):
        if event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_DOWN and self.snake.moving_up == False and self.game_active == True:
            self.snake.moving_down = True
            self.snake.moving_right = False
            self.snake.moving_left = False
            self.snake.moving_up = False
            self.leading_rect_direction = "down"
        elif event.key == pygame.K_UP and self.snake.moving_down == False and self.game_active == True:
            self.snake.moving_down = False
            self.snake.moving_right = False
            self.snake.moving_left = False
            self.snake.moving_up = True
            self.leading_rect_direction = "up"
        elif event.key == pygame.K_RIGHT and self.snake.moving_left == False and self.game_active == True:
            self.snake.moving_down = False
            self.snake.moving_right = True
            self.snake.moving_left = False
            self.snake.moving_up = False
            self.leading_rect_direction = "right"        
        elif event.key == pygame.K_LEFT and self.snake.moving_right == False and self.game_active == True:
            self.snake.moving_down = False
            self.snake.moving_right = False
            self.snake.moving_left = True
            self.snake.moving_up = False
            self.leading_rect_direction = "left"

        elif event.key == pygame.K_p:
            self._start_game()

        # Temporary buttons to simplify testing
        elif event.key == pygame.K_SPACE:
            self.settings.tick_value = int(self.settings.tick_value * self.settings.space_speed_scale)
            # self.settings.enemy_snake_speed = self.settings.enemy_snake_speed / self.settings.space_speed_scale
        elif event.key == pygame.K_i:
            print(f"{self.snake.body}")


    def _check_keyup_events(self, event):
        if event.key == pygame.K_DOWN:
            pass
        if event.key == pygame.K_UP:
            pass
        elif event.key == pygame.K_SPACE:
            self.settings.tick_value = self.settings.tick_value_default
            # self.settings.enemy_snake_speed = self.settings.enemy_snake_speed * self.settings.space_speed_scale

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked:
            self._start_game()


    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.sb.show_score()
        self.snake.draw_snake()

        for body_part in self.snake.body:
            body_part.draw_snake()

        for snake in self.enemy_snakes:
            snake.draw_snake()
            for body_part in snake.body:
                body_part.draw_snake()




        self.snake.draw_eyes()
        self.food.draw_food()

         # Draw the play button if the game is inactive.
        if not self.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


    # Check for head/food collision.
    def _check_food_collision(self):
        if self.snake.rect.colliderect(self.food):
            self.food.generate_food()
            self.snake.grow_body(self)
            self.settings.snake_speed = self.settings.snake_speed + self.settings.speedup_scale

            # Update scoreboard
            self.settings.snake_size += 1
            self.sb.prep_images()


    def _check_body_collision(self):
        for body_part in self.snake.body[25:]:
            if self.leading_rect_direction == "up":
                if (body_part.rect.bottom > self.snake.rect.top > body_part.rect.top) and (body_part.rect.centerx == self.snake.rect.centerx):
                    self._reset_round()
            if self.leading_rect_direction == "down":
                if (body_part.rect.top < self.snake.rect.bottom < body_part.rect.bottom) and (body_part.rect.centerx == self.snake.rect.centerx):
                    self._reset_round()
            if self.leading_rect_direction == "right":
                if (body_part.rect.left < self.snake.rect.right < body_part.rect.right) and (body_part.rect.centery == self.snake.rect.centery):
                    self._reset_round()
            if self.leading_rect_direction == "left":
                if (body_part.rect.right > self.snake.rect.right > body_part.rect.left) and (body_part.rect.centery == self.snake.rect.centery):
                    self._reset_round()
                    

    def _reset_round(self):
        self.game_active = False
        sleep(0.5)
        self.snake.reset_snake()
        self.snake.moving_down = False
        self.snake.moving_right = False
        self.snake.moving_left = False
        self.snake.moving_up = False
        self.settings.snake_speed = 1
        self.settings.snake_size = 1


if __name__ == '__main__':
    # Make a game instance, and ru nthe game.
    snake_survival = SnakeSurvival()
    snake_survival.run_game()