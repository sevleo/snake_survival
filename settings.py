class Settings:
    """A class to store all settings for the game."""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.tick_value = 200
        self.tick_value_default = 200


        # Snake settings
        self.snake_color = (50, 50, 50)
        
        self.headsize = 15
        self.bodysize = 15
        self.snake_body_margin = 5
        self.speedup_scale = 0.1
        self.growth_size = 25
        
        # Food settings
        self.foodsize = 20
        self.food_color = (50, 255, 50)

        self.initialize_dynamic_settings()

        # Game settings
        self.space_speed_scale = 1.2




    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.snake_speed = 1

        # Scoreboard
        self.snake_size = 1

    