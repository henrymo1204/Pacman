import pygame as pg
import random


class Score:
    def __init__(self, game, stars):
        self.screen = game.screen
        self.stars = stars
        self.point_image = pg.image.load('images/point.png') # dot point image
        self.point_rect = self.point_image.get_rect()
        self.power_pill_image = pg.image.load('images/power_pill.png') # power image
        self.power_pill_rect = self.power_pill_image.get_rect()
        self.cherry_image = pg.image.load('images/cherry.png')  # x2
        self.cherry_rect = self.cherry_image.get_rect()
        self.apple_image = pg.image.load('images/apple.png')  # x3
        self.apple_rect = self.apple_image.get_rect()
        self.strawberry_image = pg.image.load('images/strawberry.png')  # x4
        self.strawberry_rect = self.strawberry_image.get_rect()
        self.orange_image = pg.image.load('images/orange.png')  # x5
        self.orange_rect = self.orange_image.get_rect()
        self.water_mellon_image = pg.image.load('images/water_mellon.png')  # x6
        self.water_mellon_rect = self.water_mellon_image.get_rect()
        self.points = []
        self.power_pills = []
        self.fruits = []
        self.fruit_time = pg.time.get_ticks()
        self.empty = []
        self.create_food()

    def create_food(self):
        for star in self.stars:
            if star.index != 177 and star.index != 178 and star.index != 179 and star.index != 68 and star.index != 84 and star.index != 289 and star.index != 305:
                self.points.append(star.pt)
            elif star.index == 68 or star.index == 84 or star.index == 289 or star.index == 305:
                self.power_pills.append(star.pt)

    def create_fruit(self):
        now = pg.time.get_ticks()
        if now > self.fruit_time + 50000:
            num = random.randint(0, 100)
            if num == 0 and len(self.empty) > 0:
                index = random.randint(0, len(self.empty) - 1)
                self.fruits = [self.empty[index], random.randint(0, 4)]
                self.fruit_time = pg.time.get_ticks()

    def update(self):
        if len(self.fruits) == 0:
            self.create_fruit()
        self.draw()

    def draw(self):
        for i in self.points:
            self.point_rect.centerx, self.point_rect.centery = i.x, i.y
            self.screen.blit(self.point_image, self.point_rect)
        for i in self.power_pills:
            self.power_pill_rect.centerx, self.power_pill_rect.centery = i.x, i.y
            self.screen.blit(self.power_pill_image, self.power_pill_rect)
        if len(self.fruits) > 0:
            if self.fruits[1] == 0:
                self.cherry_rect.centerx, self.cherry_rect.centery = self.fruits[0].x, self.fruits[0].y
                self.screen.blit(self.cherry_image, self.cherry_rect)
            elif self.fruits[1] == 1:
                self.apple_rect.centerx, self.apple_rect.centery = self.fruits[0].x, self.fruits[0].y
                self.screen.blit(self.apple_image, self.apple_rect)
            elif self.fruits[1] == 2:
                self.strawberry_rect.centerx, self.strawberry_rect.centery = self.fruits[0].x, self.fruits[0].y
                self.screen.blit(self.strawberry_image, self.strawberry_rect)
            elif self.fruits[1] == 3:
                self.orange_rect.centerx, self.orange_rect.centery = self.fruits[0].x, self.fruits[0].y
                self.screen.blit(self.orange_image, self.orange_rect)
            elif self.fruits[1] == 4:
                self.water_mellon_rect.centerx, self.water_mellon_rect.centery = self.fruits[0].x, self.fruits[0].y
                self.screen.blit(self.water_mellon_image, self.water_mellon_rect)
