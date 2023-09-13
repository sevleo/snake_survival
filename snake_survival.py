import sys
import pygame
from settings import Settings
from snake_part import SnakeHead, EnemySnake
from food import Food
from scoreboard import Scoreboard
from button import Button
from time import sleep
from random import randint
import json
from pathlib import Path
import os

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
        self.play_button = Button(self,  "Play")
        self.sb = Scoreboard(self)
        self.snake = SnakeHead(self)
        self.enemy_snakes = []
        self.food = Food(self)
        self.leading_rect_direction = ""
        self.show_high_score = False

    
    def create_enemy_snakes(self, numOfSnakes):
        for _ in range(numOfSnakes):
            enemy_snake = EnemySnake(self)
            self.enemy_snakes.append(enemy_snake)
        self.settings.enemy_snake_count += numOfSnakes
        

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
        self.show_high_score = False
        self.create_enemy_snakes(self.settings.enemy_snake_count_default)
        self.sb.prep_images()
        self.sb.draw_score()


    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._save_progress()
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
            self._save_progress()
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
        elif event.key == pygame.K_i:
            print(f"{self.snake.body}")


    def _check_keyup_events(self, event):
        if event.key == pygame.K_DOWN:
            pass
        if event.key == pygame.K_UP:
            pass
        elif event.key == pygame.K_SPACE:
            self.settings.tick_value = self.settings.tick_value_default


    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked:
            self._start_game()


    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.sb.draw_score()
        
        if self.game_active:
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
            
        if self.show_high_score:
            self.sb.prep_high_score()
            self.sb.draw_high_score()

        pygame.display.flip()


    # Check for head/food collision.
    def _check_food_collision(self):
        if self.snake.rect.colliderect(self.food):
            self.food.generate_food()
            self.snake.grow_body(self)
            self.settings.snake_speed = self.settings.snake_speed + self.settings.speedup_scale

            self.create_enemy_snakes(randint(0,5))

            self.settings.enemy_snake_speed += 0.025
            
            # Update scoreboard
            self.settings.snake_size += 1
            self.sb.prep_images()



    def _check_body_collision(self):
        # for body_part in self.snake.body[25:]:
        #     self._check_collision_helper(body_part)
        enemies_to_remove = []
        for enemy_snake in self.enemy_snakes:
            for enemy_snake_body_part in enemy_snake.body:
                # self._check_collision_helper(enemy_snake_body_part)
                if enemy_snake_body_part.rect.colliderect(self.snake.rect):
                    self._reset_round()
            for body_part in self.snake.body:
                if enemy_snake.rect.colliderect(body_part):
                    enemies_to_remove.append(enemy_snake)
                    break
        for enemy_snake in enemies_to_remove:
            self.enemy_snakes.remove(enemy_snake)
            del enemy_snake
            if self.settings.snake_speed > 1:
                self.settings.snake_speed = self.settings.snake_speed - self.settings.speedup_scale/4
            self.settings.enemy_snake_count -= 1
            self.sb.prep_images()


    """ This method is no longer used. It was used to gracefully detect collision of snake's head with its own body. """
    # def _check_collision_helper(self, body_part):
    #     if self.leading_rect_direction == "up":
    #         if (body_part.rect.bottom > self.snake.rect.top > body_part.rect.top) and (body_part.rect.centerx == self.snake.rect.centerx):
    #             self._reset_round()
    #     if self.leading_rect_direction == "down":
    #         if (body_part.rect.top < self.snake.rect.bottom < body_part.rect.bottom) and (body_part.rect.centerx == self.snake.rect.centerx):
    #             self._reset_round()
    #     if self.leading_rect_direction == "right":
    #         if (body_part.rect.left < self.snake.rect.right < body_part.rect.right) and (body_part.rect.centery == self.snake.rect.centery):
    #             self._reset_round()
    #     if self.leading_rect_direction == "left":
    #         if (body_part.rect.right > self.snake.rect.right > body_part.rect.left) and (body_part.rect.centery == self.snake.rect.centery):
    #             self._reset_round()
                    

    def _reset_round(self):
        self.game_active = False
        sleep(0.5)
        self.snake.reset_snake()
        self.snake.moving_down = False
        self.snake.moving_right = False
        self.snake.moving_left = False
        self.snake.moving_up = False
        self.settings.snake_speed = 1
        self._save_progress()
        self.settings.snake_size = 1
        self.enemy_snakes.clear()
        self.settings.enemy_snake_count = 0
        self.show_high_score = True


    def _save_progress(self):
        # Save high score to the file.
        if self.settings.snake_size > self.settings.high_score:
            self.settings.high_score = self.settings.snake_size

            script_dir = os.path.dirname(os.path.abspath(__file__))
            # path = Path('high_score.json')
            path = os.path.join(script_dir, 'high_score.json')
            contents = json.dumps(self.settings.high_score)
            # path.write_text(contents)
            with open(path, 'w') as file:
                file.write(contents)


if __name__ == '__main__':
    # Make a game instance, and ru nthe game.
    snake_survival = SnakeSurvival()
    snake_survival.run_game()