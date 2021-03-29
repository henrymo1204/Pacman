import pygame as pg
from math import atan2, sqrt
from vector import Vector
from timer import Timer
from settings import Settings
import time
import random
from block import Block


class Character:
    def __init__(self, game, v, pt, grid_pt_next, grid_pt_prev, name, filename, scale, angle, speed):
        self.screen, self.screen_rect = game.screen, game.screen.get_rect()
        self.name = name
        self.pt, self.grid_pt_next, self.grid_pt_prev = pt, grid_pt_next, grid_pt_prev
        self.grid_pt_next.make_next()
        self.speed = speed
        if name == 'Pacman':
            self.images_up = [pg.image.load('images/pacman_up' + str(i) + '.png') for i in range(18)] + [
                pg.image.load('images/pacman_up' + str(i) + '.png') for i in reversed(range(18))]
            self.images_left = [pg.image.load('images/pacman_left' + str(i) + '.png') for i in range(18)] + [
                pg.image.load('images/pacman_left' + str(i) + '.png') for i in reversed(range(18))]
            self.images_down = [pg.image.load('images/pacman_down' + str(i) + '.png') for i in range(18)] + [
                pg.image.load('images/pacman_down' + str(i) + '.png') for i in reversed(range(18))]
            self.images_right = [pg.image.load('images/pacman_right' + str(i) + '.png') for i in range(18)] + [
                pg.image.load('images/pacman_right' + str(i) + '.png') for i in reversed(range(18))]

            self.scale = scale
            self.scale_factor = 1.0
            self.v = v
            self.prev_angle = angle
            curr_angle = self.angle()
            delta_angle = curr_angle - self.prev_angle
            self.prev_angle = curr_angle

            self.origimage_up = self.images_up
            self.origimage_left = self.images_up
            self.origimage_down = self.images_down
            self.origimage_right = self.images_right

            # for image in self.images_up:
            #     pg.transform.rotozoom(image, delta_angle, scale)
            # print(f'>>>>>>>>>>>>>>>>>>>>>>>> PREV ANGLE is {self.prev_angle}')

            timer = Timer(frames=self.images_up, wait=10)
            self.image = timer

            self.last = self.pt
            if self.grid_pt_prev is None: print("PT_PREV IS NONE NONE NONE NONE NONE")
            self.rect = self.image.imagerect().get_rect()
            self.rect.centerx, self.rect.centery = pt.x, pt.y
        else:
            self.image = pg.image.load('images/' + filename)
            self.scale = scale
            self.origimage = self.image
            self.scale_factor = 1.0
            self.v = v
            self.prev_angle = angle
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
        # self.update_angle()

    def angle(self):
        return round((atan2(self.v.x, self.v.y) * 180.0 / 3.1415 - 90) % 360, 0)
        # return atan2(self.v.x, self.v.y) * 180.0 / 3.1415 + 180.0

    def update_angle(self):
        # if self.name == 'Pacman':
        #     curr_angle = self.angle()
        #     delta_angle = curr_angle - self.prev_angle
        #     # self.image = pg.transform.rotozoom(self.image, delta_angle, 1.0)
        #     for i in range(35):
        #         self.images[i] = pg.transform.rotozoom(self.origimage[i], curr_angle - 90.0, self.scale)
        #     timer = Timer(frames=self.images, wait=1)
        #     self.image = timer
        #     self.prev_angle = curr_angle
        # else:
        #     curr_angle = self.angle()
        #     delta_angle = curr_angle - self.prev_angle
        #     # self.image = pg.transform.rotozoom(self.image, delta_angle, 1.0)
        #     self.image = pg.transform.rotozoom(self.origimage, curr_angle - 90.0, self.scale)
        #     self.prev_angle = curr_angle
        if self.v == Vector(-1, 0):
            timer = Timer(frames=self.images_left, wait=10)
            self.image = timer
        elif self.v == Vector(1, 0):
            timer = Timer(frames=self.images_right, wait=10)
            self.image = timer
        elif self.v == Vector(0, -1):
            timer = Timer(frames=self.images_up, wait=10)
            self.image = timer
        elif self.v == Vector(0, 1):
            timer = Timer(frames=self.images_down, wait=10)
            self.image = timer

    def update(self):
        # print(f'{self.pt} with dims={self.pt.dims} and {self.pt_next} with dims={self.pt.dims}')
        delta = self.pt - self.grid_pt_next.pt
        # print(f'         delta is: {delta} and mag is {delta.magnitude()}')
        if delta.magnitude() > 3:
            # print(f'changing location... --- with velocity {self.v}')
            self.prev = self.pt
            self.pt += self.scale_factor * self.v * self.speed
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
        if self.name == 'Pacman':
            image = self.image.imagerect()
            self.screen.blit(image, self.rect)
        else:
            self.screen.blit(self.image, self.rect)


class Pacman(Character):
    def __init__(self, game, v, pt, grid_pt_next, grid_pt_prev, name="Pacman", filename="pacman17.png", scale=1):
        super().__init__(game=game, name=name, filename=filename, scale=scale,
                         v=v, pt=pt, grid_pt_next=grid_pt_next, grid_pt_prev=grid_pt_prev, angle=90.0, speed=3)

    def killGhost(self): pass

    def eatPoint(self): pass

    def eatFruit(self): pass

    def eatPowerPill(self): pass

    def firePortalGun(self, color): pass
    # def update(self):  self.draw()

    # def draw(): pass


class Ghost(Character):
    def __init__(self, game, v, pt, grid_pt_next, grid_pt_prev, pacman, stars, name="Pinky", filename="alien00.png",
                 scale=0.8):
        super().__init__(game, v=v, pt=pt, grid_pt_next=grid_pt_next, grid_pt_prev=grid_pt_prev, name=name,
                         filename=filename, scale=scale, angle=270.0, speed=5)
        # self.screen, self.screen_rect = game.screen, game.screen.get_rect()
        self.pacman = pacman
        self.stars = stars
        self.last = pt
        self.current = grid_pt_next.index

        self.idle = False
        self.flicker = False
        self.run = False
        self.chase = False

        self.route = None

    def a_star(self):
        for star in self.stars:
            if star.index == self.current:
                open_list = [Block(star.pt.x, star.pt.y, 0, 0, 0, star, None)]
        closed_list = []

        while len(open_list) > 0:
            best = None
            route = None
            lowest = None
            for i in open_list:
                if lowest is None or lowest.f > i.f:
                    lowest = i
            current = lowest
            adj_list = lowest.star.adj_list
            if current.star.index == self.pacman.grid_pt_next.index:
                open_list = []
                break
            for adj in adj_list:
                for star in self.stars:
                    if star.index == adj:
                        temp = current.g + 1
                        exist = False
                        for i in closed_list:
                            if star == i.star:
                                exist = True
                        if not exist:
                            g = current.g + 1
                            delta = star.pt - self.pacman.pt
                            h = sqrt(delta.x * delta.x + delta.y * delta.y)
                            f = g + h
                            for i in open_list:
                                if i.star == star:
                                    exist = True
                            if exist:
                                if temp < g:
                                    for i in open_list:
                                        if i.star == star:
                                            i.g = g
                                            break
                            else:
                                g = current.g + 1
                                delta = star.pt - self.pacman.pt
                                h = sqrt(delta.x * delta.x + delta.y * delta.y)
                                f = g + h
                                open_list.append(Block(star.pt.x, star.pt.y, f, g, h, star, current.star.index))
            open_list.remove(current)
            closed_list.append(current)

        current = closed_list[-1]
        temp = [current.star.index]
        while current.star.index != self.current:
            for i in closed_list:
                if i.star.index == current.previous:
                    temp.insert(0, i.star.index)
                    current = i
        print('temp:', temp)
        print('route:', self.route)
        if self.route is None or len(self.route) == 0 or len(self.route) > len(temp):
            self.route = temp[1:]
        print(self.route)

    def performAction(self):
        if self.chase:
            print('chase')

            self.a_star()

            if self.name == 'blinky':
                print('blinky')
            print('before route:', self.route)
            route = self.route[0]
            del self.route[0]
            print('after route:', self.route)

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

            # if len(self.route) == 0:
            #     self.a_star()

            # for star in self.stars:
            #     if star.index == self.current:
            #         open_list = [Block(star.pt.x, star.pt.y, 0, 0, 0, star, None)]
            # closed_list = []
            #
            # while len(open_list) > 0:
            #     best = None
            #     route = None
            #     lowest = None
            #     for i in open_list:
            #         if lowest is None or lowest.f > i.f:
            #             lowest = i
            #     current = lowest
            #     adj_list = lowest.star.adj_list
            #     if current.star.index == self.pacman.grid_pt_next.index:
            #         open_list = []
            #         break
            #     for adj in adj_list:
            #         for star in self.stars:
            #             if star.index == adj:
            #                 temp = current.g + 1
            #                 exist = False
            #                 for i in closed_list:
            #                     if star == i.star:
            #                         exist = True
            #                 if not exist:
            #                     g = current.g + 1
            #                     delta = star.pt - self.pacman.pt
            #                     h = sqrt(delta.x * delta.x + delta.y * delta.y)
            #                     f = g + h
            #                     for i in open_list:
            #                         if i.star == star:
            #                             exist = True
            #                     if exist:
            #                         if temp < g:
            #                             for i in open_list:
            #                                 if i.star == star:
            #                                     i.g = g
            #                                     break
            #                     else:
            #                         g = current.g + 1
            #                         delta = star.pt - self.pacman.pt
            #                         h = sqrt(delta.x * delta.x + delta.y * delta.y)
            #                         f = g + h
            #                         open_list.append(Block(star.pt.x, star.pt.y, f, g, h, star, current.star.index))
            #     open_list.remove(current)
            #     closed_list.append(current)
            #
            #
            # self.route = []
            # for i in closed_list:
            #     if i.star.index != self.current:
            #         self.route.append(i.star.index)
            #
            # # next_grid = self.grid_pt_next
            # # visited = [self.current]
            # # diverge = []
            # # while next_grid.index != self.pacman.grid_pt_next.index:
            # #     print(self.pacman.grid_pt_next.index)
            # #     print(self.name)
            # #     print(next_grid.index)
            # #     for adjacency in next_grid.adj_list:
            # #         print('adj_list', adjacency)
            # #         for star in self.stars:
            # #             if star.index == adjacency:
            # #                 delta = star.pt - self.pacman.pt
            # #                 h = sqrt(delta.x * delta.x + delta.y * delta.y)
            # #                 f = 2 + h
            # #                 diverge.append(adjacency)
            # #         if best is None and route is None or best > f:
            # #             if adjacency not in visited:
            # #                 best = f
            # #                 route = adjacency
            # #                 print(route)
            # #     if route is None:
            # #         route = diverge[0]
            # #         del diverge[0]
            # #     for star in self.stars:
            # #         if star.index == route:
            # #             next_grid = star
            # #             if star.index not in visited:
            # #                 visited.append(star.index)
            # #             diverge.remove(adjacency)
            # #             print(visited)
            # #             break
            # #     best = None
            # #     route = None
            # # route = visited[1]
            # # print('route:', route)
            #
            # self.grid_pt_next.make_normal()
            # self.grid_pt_prev = self.grid_pt_next
            # for star in self.stars:
            #     if star.index == route:
            #         index = route - self.current
            #         if index == -1:
            #             self.v = Vector(-1, 0)
            #         elif index == 1:
            #             self.v = Vector(1, 0)
            #         elif index == -17:
            #             self.v = Vector(0, 1)
            #         elif index == 17:
            #             self.v = Vector(0, -1)
            #         self.grid_pt_next = star
            #         self.current = route
            #         break
            #
            # self.grid_pt_next.make_next()


        elif self.idle:
            print('idle')
            adj_list = []
            for adjacency in self.grid_pt_next.adj_list:
                if adjacency != self.current:
                    adj_list.append(adjacency)
            next_grid = random.choice(adj_list)

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

    def switchToChase(self):
        # best = None
        # route = None
        # for adjacency in self.grid_pt_next.adj_list:
        #     for star in self.stars:
        #         if star.index == adjacency:
        #             delta = star.pt - self.pacman.pt
        #             h = sqrt(delta.x * delta.x + delta.y * delta.y)
        #     if best is None and route is None or best > h:
        #         best = h
        #         route = adjacency
        # self.grid_pt_next.make_normal()
        # self.grid_pt_prev = self.grid_pt_next
        # for star in self.stars:
        #     if star.index == route:
        #         index = route - self.current
        #         if index == -1:
        #             self.v = Vector(-1, 0)
        #         elif index == 1:
        #             self.v = Vector(1, 0)
        #         elif index == -17:
        #             self.v = Vector(0, 1)
        #         elif index == 17:
        #             self.v = Vector(0, -1)
        #         self.grid_pt_next = star
        #         self.current = route
        #         break
        #
        # self.grid_pt_next.make_next()
        pass

    def switchToRun(self):
        best = None
        route = None
        for adjacency in self.grid_pt_next.adj_list:
            for star in self.stars:
                if star.index == adjacency:
                    delta = star.pt - self.pacman.pt
                    h = sqrt(delta.x * delta.x + delta.y * delta.y)
            if best is None and route is None or best < h:
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

    def switchToFlicker(self):
        pass

    def switchToIdle(self):
        # adj_list = []
        # for adjacency in self.grid_pt_next.adj_list:
        #     if adjacency != self.current:
        #         adj_list.append(adjacency)
        # next_grid = random.choice(adj_list)
        #
        # for star in self.stars:
        #     if star.index == next_grid:
        #         index = next_grid - self.current
        #         if index == -1:
        #             self.v = Vector(-1, 0)
        #         elif index == 1:
        #             self.v = Vector(1, 0)
        #         elif index == -17:
        #             self.v = Vector(0, 1)
        #         elif index == 17:
        #             self.v = Vector(0, -1)
        #         self.grid_pt_next.make_normal()
        #         self.grid_pt_prev = self.grid_pt_next
        #         self.grid_pt_next = star
        #         self.grid_pt_next.make_next()
        #         self.current = next_grid
        pass

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
