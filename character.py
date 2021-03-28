import pygame as pg
from math import atan2, sqrt
from vector import Vector
from timer import Timer
from settings import Settings
import time
import random

class Character:
    def __init__(self, game, v, pt, grid_pt_next, grid_pt_prev, name, filename, scale):
        self.screen, self.screen_rect = game.screen, game.screen.get_rect()
        self.name = name
        self.pt, self.grid_pt_next, self.grid_pt_prev = pt, grid_pt_next, grid_pt_prev
        self.grid_pt_next.make_next()
        self.image = pg.image.load('images/' + filename)
        self.scale = scale
        self.origimage = self.image
        self.scale_factor = 1.0
        self.v = v
        self.prev_angle = 90.0
        curr_angle = self.angle()
        delta_angle = curr_angle - self.prev_angle
        self.prev_angle = curr_angle
        print(f'>>>>>>>>>>>>>>>>>>>>>>>> PREV ANGLE is {self.prev_angle}')
        self.last = self.pt
        if self.grid_pt_prev is None: print("PT_PREV IS NONE NONE NONE NONE NONE")
        self.image = pg.transform.rotozoom(self.image, delta_angle, scale)
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = pt.x, pt.y

    def clamp(self):
        screen = self.screen_rect
        self.pt.x = max(0, min(self.pt.x, screen.width))
        self.pt.y = max(0, min(self.pt.y, screen.height))

    def enterPortal(self):
        pass

    def at_dest(self):
        return self.pt == self.grid_pt_next.pt

    def at_source(self):
        return self.pt == self.grid_pt_prev.pt

    def on_star(self):
        return self.at_dest() or self.at_source()

    def reverse(self):
        temp = self.grid_pt_prev
        self.grid_pt_prev = self.grid_pt_next
        self.grid_pt_next = temp
        self.grid_pt_prev.make_normal()
        self.grid_pt_next.make_next()
        self.v *= -1
        self.scale_factor = 1
        self.update_angle()

    def angle(self):
        return round((atan2(self.v.x, self.v.y) * 180.0 / 3.1415 - 90) % 360, 0)
        # return atan2(self.v.x, self.v.y) * 180.0 / 3.1415 + 180.0

    def update_angle(self):
        curr_angle = self.angle()
        delta_angle = curr_angle - self.prev_angle
        # self.image = pg.transform.rotozoom(self.image, delta_angle, 1.0)
        self.image = pg.transform.rotozoom(self.origimage, curr_angle - 90.0, self.scale)
        self.prev_angle = curr_angle

    def update(self):
        # print(f'{self.pt} with dims={self.pt.dims} and {self.pt_next} with dims={self.pt.dims}')
        delta = self.pt - self.grid_pt_next.pt
        # print(f'         delta is: {delta} and mag is {delta.magnitude()}')
        if delta.magnitude() > 1:
            # print(f'changing location... --- with velocity {self.v}')
            self.prev = self.pt
            self.pt += self.scale_factor * self.v * 3
        self.clamp()
        if self.pt.x <= 0:
            self.pt = Vector(900, 445)
        elif self.pt.x >= 900:
            self.pt = Vector(0, 445)
        if self.pt != self.last:
            print(f'{self.name}@{self.pt} -- next is: {self.grid_pt_next.pt}')
            self.last = self.pt
        else:
            self.pt = self.grid_pt_next.pt
            self.last = self.pt
        self.rect.centerx, self.rect.centery = self.pt.x, self.pt.y
        self.draw()

    def draw(self):
        self.screen.blit(self.image, self.rect)


class Pacman(Character):
    def __init__(self, game, v, pt, grid_pt_next, grid_pt_prev, name="Pacman", filename="ship.bmp", scale=0.55):
        super().__init__(game=game, name=name, filename=filename, scale=scale,
                         v=v, pt=pt, grid_pt_next=grid_pt_next, grid_pt_prev=grid_pt_prev)

    def killGhost(self): pass

    def eatPoint(self): pass

    def eatFruit(self): pass

    def eatPowerPill(self): pass

    def firePortalGun(self, color): pass
    # def update(self):  self.draw()

    # def draw(): pass


class Ghost(Character):
    def __init__(self, game, v, pt, grid_pt_next, grid_pt_prev, pacman, stars, name="Pinky", filename="alien10.png",
                 scale=0.8):
        super().__init__(game, v=v, pt=pt, grid_pt_next=grid_pt_next, grid_pt_prev=grid_pt_prev, name=name,
                         filename=filename, scale=scale)
        # self.screen, self.screen_rect = game.screen, game.screen.get_rect()
        self.pacman = pacman
        self.stars = stars
        self.last = pt
        self.current = grid_pt_next.index
        self.inside = True

    def at_base(self):
        return self.current == 177 or self.current == 178 or self.current == 179

    def exit(self):
        if self.current == 178:
            for star in self.stars:
                if star.index == 212:
                    self.grid_pt_next.make_normal()
                    self.grid_pt_prev = self.grid_pt_next
                    self.grid_pt_next = star
                    self.grid_pt_next.make_next()
                    self.v = Vector(0, -1)
                    self.current = 212
        elif self.current == 177:
            for star in self.stars:
                if star.index == 178:
                    self.grid_pt_next.make_normal()
                    self.grid_pt_prev = self.grid_pt_next
                    self.grid_pt_next = star
                    self.grid_pt_next.make_next()
                    self.v = Vector(1, 0)
                    self.current = 178
        elif self.current == 179:
            for star in self.stars:
                if star.index == 178:
                    self.grid_pt_next.make_normal()
                    self.grid_pt_prev = self.grid_pt_next
                    self.grid_pt_next = star
                    self.grid_pt_next.make_next()
                    self.v = Vector(-1, 0)
                    self.current = 178


    def enter(self):
        pass

    def chase(self):
        best = None
        route = None
        for adjacency in self.grid_pt_next.adj_list:
            for star in self.stars:
                if star.index == adjacency:
                    delta = star.pt - self.pacman.pt
                    h = sqrt(delta.x * delta.x + delta.y * delta.y)
            if best is None and route is None or best > h:
                best = h
                route = adjacency
        self.grid_pt_next.make_normal()
        self.grid_pt_prev = self.grid_pt_next
        for star in self.stars:
            if star.index == route:
                index = route - self.current
                if index == -1:
                    self.v = Vector(-1, 0)
                elif index == 1:
                    self.v = Vector(1, 0)
                elif index == -17:
                    self.v = Vector(0, 1)
                elif index == 17:
                    self.v = Vector(0, -1)
                self.grid_pt_next = star
                self.current = route
                break

        self.grid_pt_next.make_next()

    def switchToRun(self):
        pass

    def switchToFlicker(self):
        pass

    def switchToIdle(self):
        next_grid = None
        for adjacency in self.grid_pt_next.adj_list:
            number = random.randint(0, 3)
            if number == 0:
                next_grid = adjacency
            if next_grid is None:
                next_grid = adjacency

        for star in self.stars:
            if star.index == next_grid:
                index = next_grid - self.current
                if index == -1:
                    self.v = Vector(-1, 0)
                elif index == 1:
                    self.v = Vector(1, 0)
                elif index == -17:
                    self.v = Vector(0, 1)
                elif index == 17:
                    self.v = Vector(0, -1)
                self.grid_pt_next.make_normal()
                self.grid_pt_prev = self.grid_pt_next
                self.grid_pt_next = star
                self.grid_pt_next.make_next()
                self.current = next_grid





    def die(self):
        pass

    def killPacman(self):
        pass

    # def update(self):
    #     destination = self.chase()
    #     self.grid_pt_next.make_normal()
    #     self.grid_pt_prev = self.grid_pt_next
    #     for star in self.stars:
    #         if star.index == destination:
    #             index = destination - self.current
    #             if index == -1:
    #                 self.v = Vector(-1, 0)
    #             elif index == 1:
    #                 self.v = Vector(1, 0)
    #             elif index == -11:
    #                 self.v = Vector(0, -1)
    #             elif index == 11:
    #                 self.v = Vector(0, 1)
    #             self.grid_pt_next = star
    #             self.current = destination
    #             break
    #
    #     self.grid_pt_next.make_next()
    #
    #     delta = self.pt - self.grid_pt_next.pt
    #     # print(f'         delta is: {delta} and mag is {delta.magnitude()}')
    #     if delta.magnitude() > 0:
    #         # print(f'changing location... --- with velocity {self.v}')
    #         self.prev = self.pt
    #         self.pt += self.scale_factor * self.v
    #     self.clamp()
    #     if self.pt != self.last:
    #         print(f'{self.name}@{self.pt} -- next is: {self.grid_pt_next.pt}')
    #         self.last = self.pt
    #     self.rect.centerx, self.rect.centery = self.pt.x, self.pt.y
    #     self.draw()

    # def draw(self):
    #     self.screen.blit(self.image, self.rect)
