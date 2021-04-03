import pygame as pg

from pygame.sysfont import SysFont
from pygame.sprite import Sprite, Group
from timer import Timer
from math import atan2, sqrt
from vector import Vector
from timer import Timer
from settings import Settings
import time
import random
from block import Block


class Button:
    """Represents a click-able button style text, with altering text color"""

    def __init__(self, settings, screen, msg, y_factor=0.65):
        self.settings = settings
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Dimensions and properties of the button
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.alt_color = (255, 215, 0)
        self.font = SysFont(None, 48)
        self.y_factor = y_factor

        # Prep button message
        self.msg = msg
        self.msg_image, self.msg_image_rect = None, None
        self.prep_msg(self.text_color)

    def check_button(self, mouse_x, mouse_y):
        """Check if the given button has been pressed"""
        if self.msg_image_rect.collidepoint(mouse_x, mouse_y):
            return True
        else:
            return False

    def alter_text_color(self, mouse_x, mouse_y):
        """Change text color if the mouse coordinates collide with the button"""
        if self.check_button(mouse_x, mouse_y):
            self.prep_msg(self.alt_color)
        else:
            self.prep_msg(self.text_color)

    def prep_msg(self, color):
        """Turn msg into a rendered image and center it on the button"""
        self.msg_image = self.font.render(self.msg, True, color, self.settings.bg_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.centerx = (self.settings.screen_width // 2)
        self.msg_image_rect.centery = int(self.settings.screen_height * self.y_factor)

    def draw_button(self):
        """blit message to the screen"""
        self.screen.blit(self.msg_image, self.msg_image_rect)


class Title:
    """Represents the title text to be displayed on screen"""

    def __init__(self, bg_color, screen, text, text_size=56, text_color=(255, 255, 255)):
        self.bg_color = bg_color
        self.screen = screen
        self.text = text
        self.text_color = text_color
        self.font = SysFont("Broadway", text_size)
        self.image = None
        self.image_rect = None

    def prep_image(self):
        """Render the subtitle text as an image"""
        self.image = self.font.render(self.text, True, self.text_color, self.bg_color)
        self.image_rect = self.image.get_rect()

    def draw(self):
        """Draw the subtitle's image to the screen"""
        self.screen.blit(self.image, self.image_rect)


class Points:
    """Represents the subtitle text displayed on screen"""

    def __init__(self, bg_color, screen, text, text_size=48, text_color=(255, 255, 255)):
        self.bg_color = bg_color
        self.screen = screen
        self.text = text
        self.text_color = text_color
        self.font = SysFont(None, text_size)
        self.image = None
        self.image_rect = None

    def prep_image(self):
        """Render the subtitle text as an image"""
        self.image = self.font.render(self.text, True, self.text_color, self.bg_color)
        self.image_rect = self.image.get_rect()

    def draw(self):
        """Draw the subtitle's image to the screen"""
        self.screen.blit(self.image, self.image_rect)


class Intro:
    """Contains information and methods relating to the start menu"""

    def __init__(self, settings, stats, screen):
        # settings, settings, stats
        self.settings = settings
        self.game_stats = stats
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # text/image information
        self.title = Title(settings.bg_color, self.screen, 'PacMan', text_size=72)
        self.subtitle = Title(settings.bg_color, self.screen, 'Portal', text_size=72, text_color=(255, 255, 0))

        self.prep_image()

    def prep_image(self):
        """Render the title as an image"""
        # title ALIEN
        self.title.prep_image()
        self.title.image_rect.centerx = self.screen_rect.centerx
        self.title.image_rect.top = self.screen_rect.top
        # subtitle INVASION
        self.subtitle.prep_image()
        self.subtitle.image_rect.centerx = self.screen_rect.centerx
        self.subtitle.image_rect.top = self.title.image_rect.bottom

    def draw(self):
        """Draw the title to the screen"""
        self.title.draw()
        self.subtitle.draw()


class Ufos:
    def __init__(self, settings, screen):
        self.settings = settings
        ufo_group = Group()
        self.ufos = ufo_group
        self.screen = screen

    def create_fleet(self):
        settings, screen = self.settings, self.screen
        ufos = Ufo(settings=settings, screen=self.screen)

    def add(self, ufo):
        self.ufos.add(ufo)

    def remove(self, ufo):
        self.ufos.ufos.remove(ufo)

    def change_direction(self):
        self.settings.fleet_direction *= -1

    def check_edges(self):
        for ufo in self.ufos:
            if ufo.check_edges():
                Ufo.images_boom.clear()
                return True
        return False

    def update(self):
        self.ufos.update()
        now = pg.time.get_ticks()

        if self.check_edges():
            for ufo in self.ufos.copy():
                ufo.update()
                self.ufos.remove(ufo)

        for ufo in self.ufos.copy():
            ufo.update()
            if ufo.reallydead:
                self.ufos.remove(ufo)

    def draw(self):
        for ufo in self.ufos.sprites():
            ufo.draw()



class Ufo(Sprite):  # INHERITS from SPRITE
    images = []

    images = [[pg.image.load('images/menu_animation/menu_animation' + str(i) + '.png') for i in range(0, 82)]]
    timers = []
    for i in range(1):
        timers.append(Timer(frames=images[i], wait=550))

    def __init__(self, settings, screen, number=0, speed=0):
        super().__init__()
        self.screen = screen
        self.settings = settings
        self.number = number
        self.update_requests = 0
        self.timer_switched = False

        self.timer = Ufo.timers[number]
        # self.timer = Timer(frames=self.frames, wait=700)
        self.rect = self.timer.imagerect().get_rect()

        # moving direction of image block
        self.ufo_direction = self.settings.ufo_fleet_direction #* (choice([-1, 1]))

        self.rect.x = self.x = 0 if self.ufo_direction > 0 else settings.screen_width - 80
        self.rect.y = self.y = 500 # y location of animation
        # self.rect.x = self.rect.width
        # self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def set_timer_zero(self):
        self.timer = Ufo.timers[self.number]


    def check_edges(self):
        r, rscreen = self.rect, self.screen.get_rect()
        return r.right > rscreen.right or r.left < 0

    def move_right(self):
        self.rect.x += 1
        self.x = self.rect.x
        time.sleep(0.005)

    def move_left(self):
        self.rect.x -= 1
        self.x = self.rect.x
        time.sleep(0.002)

    def move_center(self):
        delta = self.ufo_direction
        self.rect.x = self.settings.screen_width / 2 - 90
        self.x = self.rect.x
        time.sleep(0.002)

    def update(self):
        now = pg.time.get_ticks() % 44500
        if now < 9000:
            if now < 500:
                self.rect.right = 0

            self.move_right()
        elif now > 9000 and now < 16000:

            self.move_left()
        else:
            self.move_center()


    def draw(self):
        # image = Ufo.images[self.number]
        # self.screen.blit(image, self.rect)
        image = self.timer.imagerect()
        rect = image.get_rect()
        rect.x, rect.y = self.rect.x, self.rect.y
        self.screen.blit(image, rect)
        # self.screen.blit(self.image, self.rect)

    @staticmethod
    def run_tests():
        print(Ufo.images)
