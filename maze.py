import pygame as pg
from timer import Timer
from vector import Vector
from settings import Settings


class Maze:
    def __init__(self, game):
        self.screen = game.screen
        self.image = pg.image.load('images/maze.png')
        self.image = pg.transform.rotozoom(self.image, 0, 0.6)
        self.rect = self.image.get_rect()

    def update(self): self.draw()
    def draw(self): self.screen.blit(self.image, self.rect)


class GridPoint:
    image0 = pg.image.load('images/star.png')
    image0 = pg.transform.rotozoom(image0, 0, 0.7)
    image1 = pg.transform.rotozoom(image0, 0, 1.1)
    image2 = pg.transform.rotozoom(image0, 0, 1.2)
    image3 = pg.transform.rotozoom(image0, 0, 1.3)
    images = [image0, image1, image2, image3, image2, image1]

    imagen0 = pg.image.load('images/star_next.png')
    imagen0 = pg.transform.rotozoom(imagen0, 0, 0.7)
    imagen1 = pg.transform.rotozoom(imagen0, 0, 1.1)
    imagen2 = pg.transform.rotozoom(imagen0, 0, 1.2)
    imagen3 = pg.transform.rotozoom(imagen0, 0, 1.3)
    imagesn = [imagen0, imagen1, imagen2, imagen3, imagen2, imagen1]

    def __init__(self, game, pt=Vector(70,931), index=0, adj_list=[]):
        self.game = game
        self.screen = game.screen
        self.pt = pt
        self.index = index
        self.adj_list = adj_list
        self.timer_normal = Timer(GridPoint.images, wait=100)
        self.timer_next = Timer(GridPoint.imagesn, wait=100)
        self.timer = self.timer_normal

    def update(self): self.draw()

    def make_next(self): self.timer = self.timer_next

    def make_normal(self): self.timer = self.timer_normal

    def draw(self):
        image = self.timer.imagerect()
        rect = image.get_rect()
        rect.centerx, rect.centery = self.pt.x, self.pt.y
        self.screen.blit(image, rect)
