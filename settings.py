class Settings():
    """A class to store all settings for PacMan."""

    def __init__(self):
        """Initialize the game's settings."""
        self.screen_width = 1100 # 910
        self.screen_height = 1000
        self.bg_color = (0, 0, 0)

        self.lives_limit = 2
        self.bullet_width = 5
        self.bullet_height = 30
        self.bullet_color = 255, 0, 0
        self.bullets_every = 300
        self.speed = 5

        """ Points """
        self.score_scale = 1.5
        self.points = 20
        self.fruit_points = 50
        self.ghost_points = 100
        self.init_dynamic_settings()

    def reset_speed(self):
        self.speed = 5

    def init_dynamic_settings(self):
        self.ship_speed_factor = 9
        self.bullet_speed_factor = 5
        self.alien_speed = 1
        self.ufo_speed = 1
        self.fleet_direction = 1
        self.ufo_fleet_direction = 1
        self.alien_points = 50
        self.speedup_scale = 1.1

    def increase_speed(self):
        scale = self.speedup_scale
        self.ship_speed_factor *= scale
        self.bullet_speed_factor *= scale
        self.alien_speed *= scale
