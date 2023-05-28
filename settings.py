class Settings:
    """A class to store all settings for the game."""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Snake settings
        self.snake_color = (50, 50, 50)
        self.snake_speed = 15
        self.headsize = 15
        self.bodysize = 15
        self.snake_body_margin = 5
        
        # Food settings
        self.foodsize = 15
        self.food_color = (50, 50, 50)