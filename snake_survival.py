import sys
import pygame
from settings import Settings
from snake_part import Snake_head
from food import Food
from scoreboard import Scoreboard

class SnakeSurvival:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()

        self.game_active = True

        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        pygame.display.set_caption("Snake Survival")
        self.screen_rect = self.screen.get_rect()
        
        self.sb = Scoreboard(self)
        self.snake = Snake_head(self)
        self.snake.grow_body(self)
        self.food = Food(self)
        

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self.snake.update_head()
            self.snake.update_body()
            self._check_food_collision()
            self._update_screen()
            self.clock.tick(self.settings.tick_value)
            


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


    def _check_keydown_events(self, event):
        if event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_DOWN:
            self.snake.moving_down = True
            self.snake.moving_right = False
            self.snake.moving_left = False
            self.snake.moving_up = False
        elif event.key == pygame.K_UP:
            self.snake.moving_down = False
            self.snake.moving_right = False
            self.snake.moving_left = False
            self.snake.moving_up = True
        elif event.key == pygame.K_RIGHT:
            self.snake.moving_down = False
            self.snake.moving_right = True
            self.snake.moving_left = False
            self.snake.moving_up = False            
        elif event.key == pygame.K_LEFT:
            self.snake.moving_down = False
            self.snake.moving_right = False
            self.snake.moving_left = True
            self.snake.moving_up = False

        # Temporary buttons to simplify testing
        elif event.key == pygame.K_SPACE:
            #self.snake.speed_factor = 1.5
            self.settings.tick_value = int(self.settings.tick_value * self.settings.space_speed_scale)
        elif event.key == pygame.K_i:
            print(f"{self.snake.body}")


    def _check_keyup_events(self, event):
        if event.key == pygame.K_DOWN:
            #self.ship.moving_down = False
            pass
        if event.key == pygame.K_UP:
            #self.ship.moving_up = False
            pass
        elif event.key == pygame.K_SPACE:
            #self.snake.speed_factor = 1
            self.settings.tick_value = self.settings.tick_value_default


    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.snake.draw_snake()
        for body_part in self.snake.body:
            body_part.draw_snake()
        self.food.draw_food()
        self.sb.show_score()

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
    
    
if __name__ == '__main__':
    # Make a game instance, and ru nthe game.
    snake_survival = SnakeSurvival()
    snake_survival.run_game()