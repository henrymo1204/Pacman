import pygame as pg
from math import atan2, sqrt
from vector import Vector
from timer import Timer
from settings import Settings
import time
import random
from block import Block
from sound import Sound


class Character:
    def __init__(self, game, v, pt, grid_pt_next, grid_pt_prev, name, filename, scale, angle, speed, stars):
        self.screen, self.screen_rect = game.screen, game.screen.get_rect()
        self.name = name
        self.pt, self.grid_pt_next, self.grid_pt_prev = pt, grid_pt_next, grid_pt_prev
        self.grid_pt_next.make_next()
        self.speed = speed
        self.dead = False
        self.stars = stars


        if name == 'Pacman':
            self.images_up = [pg.image.load('images/pacman_up' + str(i) + '.png') for i in range(18)] + [
                pg.image.load('images/pacman_up' + str(i) + '.png') for i in reversed(range(18))]
            self.images_left = [pg.image.load('images/pacman_left' + str(i) + '.png') for i in range(18)] + [
                pg.image.load('images/pacman_left' + str(i) + '.png') for i in reversed(range(18))]
            self.images_down = [pg.image.load('images/pacman_down' + str(i) + '.png') for i in range(18)] + [
                pg.image.load('images/pacman_down' + str(i) + '.png') for i in reversed(range(18))]
            self.images_right = [pg.image.load('images/pacman_right' + str(i) + '.png') for i in range(18)] + [
                pg.image.load('images/pacman_right' + str(i) + '.png') for i in reversed(range(18))]
            self.images = [pg.image.load('images/dying_pacman' + str(i) + '.png') for i in range(13)]

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
            #if self.grid_pt_prev is None: print("PT_PREV IS NONE NONE NONE NONE NONE")
            self.rect = self.image.imagerect().get_rect()
            self.rect.centerx, self.rect.centery = pt.x, pt.y
        else:
            self.images_up = [pg.image.load('images/' + name + '_up' + str(i) + '.png') for i in range(2)]
            self.images_left = [pg.image.load('images/' + name + '_left' + str(i) + '.png') for i in range(2)]
            self.images_down = [pg.image.load('images/' + name + '_down' + str(i) + '.png') for i in range(2)]
            self.images_right = [pg.image.load('images/' + name + '_right' + str(i) + '.png') for i in range(2)]
            self.images_run = [pg.image.load('images/blue_ghost' + str(i) + '.png') for i in range(2)]
            self.images_flicker = [pg.image.load('images/blue_ghost' + str(i) + '.png') for i in range(2)] + [
                pg.image.load('images/white_ghost' + str(i) + '.png') for i in range(2)]
            self.images_eyes_up = pg.image.load('images/eyes_up.png')
            self.images_eyes_left = pg.image.load('images/eyes_left.png')
            self.images_eyes_down = pg.image.load('images/eyes_down.png')
            self.images_eyes_right = pg.image.load('images/eyes_right.png')

            self.scale = scale
            self.scale_factor = 1.0
            self.v = v
            self.prev_angle = angle
            curr_angle = self.angle()
            delta_angle = curr_angle - self.prev_angle
            self.prev_angle = curr_angle
            #print(f'>>>>>>>>>>>>>>>>>>>>>>>> PREV ANGLE is {self.prev_angle}')

            timer = Timer(frames=self.images_up, wait=200)
            self.image = timer

            self.last = self.pt
            self.rect = self.image.imagerect().get_rect()
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
        if self.name == 'Pacman':
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
        else:
            if self.dead:
                if self.v == Vector(-1, 0):
                    self.image = self.images_eyes_left
                elif self.v == Vector(1, 0):
                    self.image = self.images_eyes_right
                elif self.v == Vector(0, -1):
                    self.image = self.images_eyes_up
                elif self.v == Vector(0, 1):
                    self.image = self.images_eyes_down
            else:
                if self.v == Vector(-1, 0):
                    timer = Timer(frames=self.images_left, wait=200)
                    self.image = timer
                elif self.v == Vector(1, 0):
                    timer = Timer(frames=self.images_right, wait=200)
                    self.image = timer
                elif self.v == Vector(0, -1):
                    timer = Timer(frames=self.images_up, wait=200)
                    self.image = timer
                elif self.v == Vector(0, 1):
                    timer = Timer(frames=self.images_down, wait=200)
                    self.image = timer

    def update(self, portals=None):
        # print(f'{self.pt} with dims={self.pt.dims} and {self.pt_next} with dims={self.pt.dims}')
        delta = self.pt - self.grid_pt_next.pt
        # print(f'         delta is: {delta} and mag is {delta.magnitude()}')
        if delta.magnitude() > 3:
            # print(f'changing location... --- with velocity {self.v}')
            self.prev = self.pt
            self.pt += self.scale_factor * self.v * self.speed
        self.clamp()
        if portals:
            hit = True
            for portal in portals:
                if not portal.hit:
                    hit = False
            if hit and len(portals) == 2:
                temp = None
                for portal in portals:
                    if self.pt.x == portal.wall.pt.x and self.pt.y == portal.wall.pt.y:
                        temp = portal
                if temp:
                    for portal in portals:
                        if portal != temp:
                            self.pt = portal.wall.pt
                            for adj in portal.wall.adj_list:
                                for star in self.stars:
                                    if star.index == adj:
                                        if portal.image == portal.vertical_left:
                                            if portal.wall.pt.x > star.pt.x and portal.wall.pt.y == star.pt.y:
                                                self.v = Vector(-1, 0)
                                                self.grid_pt_next = star
                                                self.update_angle()
                                                break
                                        elif portal.image == portal.vertical_right:
                                            if portal.wall.pt.x < star.pt.x and portal.wall.pt.y == star.pt.y:
                                                self.v = Vector(1, 0)
                                                self.grid_pt_next = star
                                                self.update_angle()
                                                break
                                        elif portal.image == portal.horizontal_up:
                                            if portal.wall.pt.x == star.pt.x and portal.wall.pt.y > star.pt.y:
                                                self.v = Vector(0, -1)
                                                self.grid_pt_next = star
                                                self.update_angle()
                                                break
                                        elif portal.image == portal.horizontal_down:
                                            if portal.wall.pt.x == star.pt.x and portal.wall.pt.y < star.pt.y:
                                                self.v = Vector(0, 1)
                                                self.grid_pt_next = star
                                                self.update_angle()
                                                break
        if self.pt.x <= 0:
            self.pt = Vector(900, 445)
        elif self.pt.x >= 900:
            self.pt = Vector(0, 445)
        if self.pt != self.last:
            #print(f'{self.name}@{self.pt} -- next is: {self.grid_pt_next.pt}')
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
            if self.dead:
                self.screen.blit(self.image, self.rect)
            else:
                image = self.image.imagerect()
                self.screen.blit(image, self.rect)


class Pacman(Character):
    def __init__(self, game, v, pt, grid_pt_next, grid_pt_prev, stats, sb, settings, sound, stars, name="Pacman", filename="pacman17.png", scale=1):
        super().__init__(game=game, name=name, filename=filename, scale=scale,
                         v=v, pt=pt, grid_pt_next=grid_pt_next, grid_pt_prev=grid_pt_prev, angle=90.0, speed=3, stars=stars)
        self.ghosts = game.ghosts
        self.points = game.score.points
        self.stats = stats
        self.sb = sb
        self.sound = sound
        self.settings = settings
        self.power_pills = game.score.power_pills
        self.empty = game.score.empty
        self.game = game

    def performAction(self, fruit):
        self.eatPoint()
        self.eatPowerPill()
        self.eatFruit(fruit)
        self.killGhost()

    def killGhost(self):
        for ghost in self.ghosts:
            if ghost.run or ghost.flicker:
                if self.pt == ghost.pt:
                    ghost.die()
                    self.sound.eat_ghost()
                    self.stats.score += self.settings.ghost_points
                    self.sb.check_high_score(self.stats.score)

    def eatPoint(self):
        temp = self.points.copy()
        self.sb.prep_score()
        for point in temp:
            if self.pt == point:
                self.points.remove(point)
                self.empty.append(point)
                self.stats.score += self.settings.points
                self.sb.check_high_score(self.stats.score)
                self.sound.eat_points()
                if len(temp) == 1: # next level
                    self.game.restart()
                    self.stats.level += 1
                    self.sb.prep_level()
                    self.settings.speed += 0.5

    def eatFruit(self, fruit):
        if len(fruit.fruits) > 0:
            if self.pt == fruit.fruits[0]:
                fruit.fruits = []
                self.stats.score += self.settings.fruit_points
                self.sb.check_high_score(self.stats.score)
                self.sound.eat_fruit()

    def eatPowerPill(self):
        temp = self.power_pills.copy()
        for power_pill in temp:
            if self.pt == power_pill:
                self.power_pills.remove(power_pill)
                self.empty.append(power_pill)
                self.sound.pause_bg()
                for ghost in self.ghosts:
                    if not ghost.dead:
                        ghost.switchToRun()
                break

    def enterPortal(self, portals):
        if len(portals) == 2:
            created = True
            for portal in portals:
                if not portal.hit:
                    created = False
            if created:
                for i, portal in enumerate(portals):
                    if portal.image == portal.vertical_right:
                        for adj in portal.wall.adj_list:
                            if adj == self.grid_pt_next.index and portal.wall.pt.x < self.pt.x and portal.wall.pt.y == self.pt.y:
                                self.grid_pt_prev = self.grid_pt_next
                                self.grid_pt_next = portal.wall
                    elif portal.image == portal.vertical_left:
                        for adj in portal.wall.adj_list:
                            if adj == self.grid_pt_next.index and portal.wall.pt.x > self.pt.x and portal.wall.pt.y == self.pt.y:
                                self.grid_pt_prev = self.grid_pt_next
                                self.grid_pt_next = portal.wall
                    elif portal.image == portal.horizontal_up:
                        for adj in portal.wall.adj_list:
                            if adj == self.grid_pt_next.index and portal.wall.pt.x == self.pt.x and portal.wall.pt.y > self.pt.y:
                                self.grid_pt_prev = self.grid_pt_next
                                self.grid_pt_next = portal.wall
                    elif portal.image == portal.horizontal_down:
                        for adj in portal.wall.adj_list:
                            if adj == self.grid_pt_next.index and portal.wall.pt.x == self.pt.x and portal.wall.pt.y < self.pt.y:
                                self.grid_pt_prev = self.grid_pt_next
                                self.grid_pt_next = portal.wall


    # def update(self):  self.draw()

    # def draw(): pass


class Ghost(Character):
    def __init__(self, game, v, pt, grid_pt_next, grid_pt_prev, stars, sound, speed, name="Pinky", filename="alien00.png",
                 scale=0.8):
        super().__init__(game, v=v, pt=pt, grid_pt_next=grid_pt_next, grid_pt_prev=grid_pt_prev, name=name,
                         filename=filename, scale=scale, angle=270.0, speed=speed, stars=stars)
        # self.screen, self.screen_rect = game.screen, game.screen.get_rect()
        self.stars = stars
        self.last = pt
        self.current = grid_pt_next.index
        self.sound=sound
        self.game = game

        self.idle = False
        self.flicker = False
        self.run = False
        if name=='blinky':
            self.chase = True
        else:
            self.chase = False

        self.route = None

        self.run_time = None
        self.flicker_time = None

        self.previous_pacman = None

    def a_star(self, pacman):
        index = pacman.grid_pt_next.index
        pt = pacman.pt
        for star in self.stars:
            if star.index == self.current:
                open_list = [Block(star.pt.x, star.pt.y, 0, 0, 0, star, None)]
        closed_list = []

        while len(open_list) > 0:
            lowest = None
            for i in open_list:
                if lowest is None or lowest.f > i.f:
                    lowest = i
            current = lowest
            adj_list = lowest.star.adj_list
            if current.star.index == index:
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
                            delta = star.pt - pt
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
                                open_list.append(Block(star.pt.x, star.pt.y, f, g, h, star, current.star.index))
            open_list.remove(current)
            closed_list.append(current)

        current = closed_list[-1]
        temp = [current.star.index, index]
        while current.star.index != self.current:
            for i in closed_list:
                if i.star.index == current.previous:
                    temp.insert(0, i.star.index)
                    current = i
        #print('temp:', temp)
        #print('route:', self.route)
        # if self.route is None or len(self.route) == 0 or len(self.route) > len(temp)

        if self.route is None or len(self.route) == 0:
            if len(temp) == 1:
                self.route = temp
            else:
                self.route = temp[1:]
        elif 170 in temp or 186 in temp:
            self.route.append(temp[-1])
        elif self.previous_pacman is None or self.previous_pacman != index:
            # if len(temp) == 1:
            #     self.route = temp
            # else:
            self.route = temp[1:]
        #print(self.route)
        self.previous_pacman = index


    def performAction(self, pacman):
        if not self.flicker and not self.run and not self.dead:
            self.killPacman(pacman)
        if not pacman.dead:
            if self.chase:
            #    print('chase')

                self.a_star(pacman)

            #    if self.name == 'blinky':
            #        print('blinky')
            #    print('before route:', self.route)
                route = self.route[0]
                del self.route[0]
            #    print('after route:', self.route)

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

            elif self.run or self.flicker:
                best = None
                route = None
                for adjacency in self.grid_pt_next.adj_list:
                    for star in self.stars:
                        if star.index == adjacency and adjacency != self.current:
                            delta = star.pt - pacman.pt
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

            elif self.dead:
                if self.current == 212:
                    self.enter()
                else:
                    destination = None
                    for star in self.stars:
                        if star.index == 212:
                            destination = star
                    self.a_star(destination.index, destination.pt)

                    route = self.route[0]
                    del self.route[0]

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

            if self.run:
                now = pg.time.get_ticks()
                if now > self.run_time + 10000 and self.on_star():
                    self.switchToFlicker()
            elif self.flicker:
                now = pg.time.get_ticks()
                if now > self.flicker_time + 3000 and self.on_star():
                    self.switchToChase()
                    print("switched to chase")
                    self.sound.unpause_bg()
            else:
                self.update_angle()

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
        for star in self.stars:
            if star.index == 178:
                self.grid_pt_next.make_normal()
                self.grid_pt_prev = self.grid_pt_next
                self.grid_pt_next = star
                self.grid_pt_next.make_next()
                self.v = Vector(0, 1)
                self.current = 178
                self.dead = False
                self.switchToChase()

    def switchToChase(self):
        self.chase = True
        self.run = False
        self.flicker = False
        self.idle = False

        self.route = []

    def switchToRun(self):
        self.run = True

        self.chase = False
        self.flicker = False
        self.idle = False

        timer = Timer(frames=self.images_run, wait=200)
        self.image = timer

        self.run_time = pg.time.get_ticks()

    def switchToFlicker(self):
        self.flicker = True

        self.chase = False
        self.run = False
        self.idle = False

        timer = Timer(frames=self.images_flicker, wait=200)
        self.image = timer

        self.flicker_time = pg.time.get_ticks()

    def switchToIdle(self):
        self.idle = True

        self.chase = False
        self.run = False
        self.flicker = False

    def die(self):
        self.dead = True

        self.chase = False
        self.run = False
        self.flicker = False
        self.idle = False

        self.image = self.images_eyes_up

        self.route = []

    def killPacman(self, pacman):
        if self.current == pacman.grid_pt_next.index:
            pacman.dead = True
            self.playing_bg = False
            pg.mixer.music.pause()
            self.sound.death_sound()
            timer = Timer(frames=pacman.images, wait=50, looponce=True)
            pacman.image = timer
            print(pacman.dead)
