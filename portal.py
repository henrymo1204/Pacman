import pygame as pg
from vector import Vector


class Portal:
    def __init__(self, game):
        self.screen = game.screen
        self.v = game.pacman.v
        self.walls = game.walls_walls
        self.wall = None

        self.horizontal_up = pg.image.load('images/horizontal_up_portal.png')
        self.horizontal_up_rect = self.horizontal_up.get_rect()
        self.horizontal_down = pg.image.load('images/horizontal_down_portal.png')
        self.horizontal_down_rect = self.horizontal_down.get_rect()
        self.vertical_right = pg.image.load('images/vertical_right_portal.png')
        self.vertical_right_rect = self.vertical_right.get_rect()
        self.vertical_left = pg.image.load('images/vertical_left_portal.png')
        self.vertical_left_rect = self.vertical_left.get_rect()
        self.portal = pg.image.load('images/portal.png')
        self.portal_rect = self.portal.get_rect()

        self.image = self.portal
        self.rect = self.portal_rect
        self.rect.centerx = game.pacman.pt.x
        self.rect.centery = game.pacman.pt.y

        self.hit = False

    def update(self):
        self.draw()
        if not self.hit:
            if self.v == Vector(-1, 0):
                self.rect.centerx -= 5
                for wall in self.walls:
                    for i in range(5):
                        if self.rect.centerx - i == wall.pt.x and self.rect.centery == wall.pt.y:
                            self.hit = True
                            self.wall = wall
                            break
            elif self.v == Vector(1, 0):
                self.rect.centerx += 5
                for wall in self.walls:
                    for i in range(5):
                        if self.rect.centerx + i == wall.pt.x and self.rect.centery == wall.pt.y:
                            self.hit = True
                            self.wall = wall
                            break
            elif self.v == Vector(0, -1):
                self.rect.centery -= 5
                for wall in self.walls:
                    for i in range(5):
                        if self.rect.centerx == wall.pt.x and self.rect.centery - i == wall.pt.y:
                            self.hit = True
                            self.wall = wall
                            break
            elif self.v == Vector(0, 1):
                self.rect.centery += 5
                for wall in self.walls:
                    for i in range(5):
                        if self.rect.centerx == wall.pt.x and self.rect.centery + i == wall.pt.y:
                            self.hit = True
                            self.wall = wall
                            break
        else:
            if self.v == Vector(-1, 0):
                self.image = self.vertical_right
                self.rect = self.vertical_right_rect
            elif self.v == Vector(1, 0):
                self.image = self.vertical_left
                self.rect = self.vertical_left_rect
            elif self.v == Vector(0, -1):
                self.image = self.horizontal_down
                self.rect = self.horizontal_down_rect
            elif self.v == Vector(0, 1):
                self.image = self.horizontal_up
                self.rect = self.horizontal_up_rect



    def draw(self):
        self.screen.blit(self.image, self.portal_rect)
