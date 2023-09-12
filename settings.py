from pathlib import Path
import json
import os

class Settings:
    """A class to store all settings for the game."""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (93, 158, 130)
        self.tick_value = 200
        self.tick_value_default = 200

        # Snake settings
        self.snake_color = (50, 50, 50)
        
        self.headsize = 15
        self.bodysize = 15
        self.snake_body_margin = 5
        self.speedup_scale = 0.1
        self.growth_size = 25

        self.eye_width = 5
        self.eye_height = 5
        
        # Food settings
        self.foodsize = 20
        self.food_color = (50, 255, 50)

        self.initialize_dynamic_settings()

        # Enemy settings
        self.enemy_snake_speed = 1
        self.enemy_snake_count_default = 10
        self.enemy_snake_color = (94, 0, 0)
        self.enemy_snake_direction_change_interval = 50

        # Game settings
        self.space_speed_scale = 3


    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.snake_speed = 1

        # Scoreboard
        self.snake_size = 1

        # Enemy snakes
        self.enemy_snake_count = 0

        # High score
        self._extract_high_score()

    
    def _extract_high_score(self):
        """Extract the high score from the file."""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(script_dir, 'high_score.json')
        try:
            with open(path, 'r') as file:
                contents = file.read()
                high_score = json.loads(contents)
                self.high_score = int(high_score)
        except FileNotFoundError:
            self.high_score = 0
        

        

    