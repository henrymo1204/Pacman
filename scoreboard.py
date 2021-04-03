import pygame as pg
from pygame.sprite import Group, Sprite
from character import Pacman

class Scoreboard():
    def __init__(self, settings, screen, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = settings
        self.stats = stats

        self.text_color = (230, 230, 230)
        self.font = pg.font.SysFont(None, 40)
        self.score_image, self.score_rect = None, None
        self.high_score_image, self.high_score_rect = None, None
        self.level_image, self.level_rect = None, None
        self.score_string_image, self.score_string_rect = None, None
        self.lives_string_image, self.lives_string_rect = None, None
        self.high_score_string_image, self.high_score_string_rect = None, None

        self.prep_high_score_string()
        self.prep_high_score()
        self.prep_score_string()
        self.prep_score()
        self.prep_level()
        self.prep_lives_string()
        self.prep_lives()

    def prep_score_string(self):
        self.score_string_image = self.font.render("Score:", True, self.text_color,
                                            self.settings.bg_color)
        self.score_string_rect = self.score_string_image.get_rect()
        self.score_string_rect.right = self.screen_rect.right - 20
        self.score_string_rect.top = self.high_score_rect.bottom + 10

    def prep_score(self):
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color,
                                            self.settings.bg_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = self.score_string_rect.bottom + 10

    def prep_high_score_string(self):
        self.high_score_string_image = self.font.render("High Score:", True, self.text_color,
                                            self.settings.bg_color)
        self.high_score_string_rect = self.high_score_string_image.get_rect()
        self.high_score_string_rect.right = self.screen_rect.right - 20
        self.high_score_string_rect.top = 20

    def check_high_score(self, score):
        if score > self.stats.high_score:
            self.stats.high_score = score
            self.prep_high_score()

    def prep_high_score(self):
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color,
                                                 self.settings.bg_color)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.right = self.screen_rect.right - 20
        self.high_score_rect.top = self.high_score_string_rect.bottom
        #print('high_score', high_score_str)

    def prep_level(self):
        level = 'Level: ' + str(self.stats.level)
        self.level_image = self.font.render(level, True, self.text_color,
                                            self.settings.bg_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.screen_rect.right - 20
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_lives_string(self):
        self.lives_string_image = self.font.render("Lives:", True, self.text_color,
                                            self.settings.bg_color)
        self.lives_string_rect = self.lives_string_image.get_rect()
        self.lives_string_rect.right = self.screen_rect.right - 20
        self.lives_string_rect.top = self.level_rect.bottom + 10

    def prep_lives(self):
        self.pacman_lives = Group()
        for i in range(self.stats.lives_left):
            ship = Pacman(settings=self.settings, screen=self.screen)
            ship.rect.x = 1020 + i * ship.rect.width
            ship.rect.y = self.lives_string_rect.bottom + 10
            self.pacman_lives.add(ship)

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.screen.blit(self.score_string_image, self.score_string_rect)
        self.screen.blit(self.high_score_string_image, self.high_score_string_rect)
        self.screen.blit(self.lives_string_image, self.lives_string_rect)

        self.pacman_lives.draw(self.screen)

class Pacman(Sprite):
    def __init__(self, settings, screen):
        """Initialize the ship and set its starting position."""
        super().__init__()
        self.screen = screen
        self.settings = settings

        self.image = pg.image.load('images/pacman_right14.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.center = 0
        self.center_ship()


    def center_ship(self):
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.center = float(self.rect.centerx)


    def draw(self):
        self.screen.blit(self.image, self.rect)
