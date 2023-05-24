import sys
import pygame
from settings import Settings
from snake_head import Snake_head

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

        self.snake = Snake_head(self)


    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self.snake.update()
            self._update_screen()
            self.clock.tick(60)


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
        elif event.key == pygame.K_SPACE:
            self.snake.grow_body(self)
        elif event.key == pygame.K_i:
            print(f"{self.snake.body}")


    def _check_keyup_events(self, event):
        if event.key == pygame.K_DOWN:
            #self.ship.moving_down = False
            pass
        if event.key == pygame.K_UP:
            #self.ship.moving_up = False
            pass


    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.snake.draw_snake()


        for index, body_part in enumerate(self.snake.body):
            if index == 0:
                body_part.update_position(self.snake.previous_position)
                body_part.draw_body_part()
            else:
                previous_body_part = self.snake.body[index-1]
                body_part.update_position(previous_body_part.previous_position)
                body_part.draw_body_part()
       
        pygame.display.flip()
    

    
if __name__ == '__main__':
    # Make a game instance, and ru nthe game.
    snake_survival = SnakeSurvival()
    snake_survival.run_game()