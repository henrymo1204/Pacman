import pygame as pg
from copy import copy
import game_functions as gf
from settings import Settings
from vector import Vector
from maze import Maze, GridPoint
from character import Pacman, Ghost
from math import atan2
from timer import Timer
import time


class Game:
    def __init__(self):
        pg.init()
        self.settings = Settings()
        self.screen = pg.display.set_mode(size=(self.settings.screen_width, self.settings.screen_height))
        pg.display.set_caption("PacMan Portal")
        self.font = pg.font.SysFont(None, 48)

        self.maze = Maze(game=self)

        # li = [70, 400, 500, 830]
        # self.stars = []
        # for x in li:
        #     self.stars.append(GridPoint(game=self, pt=Vector(x, 925)))

        self.stars = [GridPoint(game=self, pt=Vector(x,925),
                                index=index, adj_list=adj_list) for (index,x,adj_list) in [(0, 70, [1, 10]),
                                                                                           (1, 120, [0, 2]),
                                                                                           (2, 210, [1, 3]),
                                                                                           (3, 310, [2, 4]),
                                                                                           (4, 400, [3, 5, 14]),
                                                                                           (5, 450, [4, 6]),
                                                                                           (6, 500, [5, 7, 16]),
                                                                                           (7, 590, [6, 8]),
                                                                                           (8, 690, [7, 9]),
                                                                                           (9, 780, [8, 10]),
                                                                                           (10, 830, [9, 20])]]

        self.stars1 = [GridPoint(game=self, pt=Vector(x,831),
                                 index=index, adj_list=adj_list) for (index,x,adj_list) in [(11, 70, [0, 12]),
                                                                                            (12, 120, [11, 13, 23]),
                                                                                            (13, 210, [12, 24]),
                                                                                            (14, 310, [15, 25]),
                                                                                            (15, 400, [4, 14]),
                                                                                            (17, 500, [6, 18]),
                                                                                            (18, 590, [17, 29]),
                                                                                            (19, 690, [20, 30]),
                                                                                            (20, 780, [19, 21, 31]),
                                                                                            (21, 830, [10, 20])]]
        self.stars2 = [GridPoint(game=self, pt=Vector(x,735)) for x in [70, 120, 210, 310, 400, 500, 590, 690, 780, 830]]
        self.stars3 = [GridPoint(game=self, pt=Vector(x,641)) for x in [70, 210, 310, 400, 500, 590, 690, 830]]
        self.stars4 = [GridPoint(game=self, pt=Vector(x,541)) for x in [210, 310, 400, 450, 500, 590, 690]]
        self.stars5 = [GridPoint(game=self, pt=Vector(x,445)) for x in [70, 210, 310, 400, 450, 500, 590, 690, 830]]
        self.stars6 = [GridPoint(game=self, pt=Vector(x,350)) for x in [210, 310, 400, 450, 500, 590, 690]]
        self.stars7 = [GridPoint(game=self, pt=Vector(x,255)) for x in [70, 210, 310, 400, 500, 590, 690, 830]]
        self.stars8 = [GridPoint(game=self, pt=Vector(x,160)) for x in [70, 210, 310, 400, 500, 590, 690, 830]]
        self.stars9 = [GridPoint(game=self, pt=Vector(x,70)) for x in [70, 210, 400, 500, 690, 830]]
        self.stars_stars = self.stars + self.stars1 + self.stars2 + self.stars3 + self.stars4 + self.stars5 + self.stars6 + self.stars7 + self.stars8 + self.stars9

        nxt = self.stars[4]
        prev = self.stars[5]

        self.pacman = Pacman(game=self, v=Vector(-1, 0), pt=prev.pt, grid_pt_next=nxt, grid_pt_prev=prev)
        # self.ghost = Ghost(game=self)

        self.grid = self.create_grid()
        self.finished = False

    def to_pixel(self, grid):
        pixels = []

    def create_grid(self):
        row0 = [0, 1, 2, 3, 4, 6, 10]
        row1 = [x for x in range(11) if x != 5]
        row2 = copy(row1)
        row3 = [x for x in range(11) if x not in [1, 5, 9]]
        row4 = [2, 3, 5, 7, 8]
        row5 = [x for x in range(11) if x not in [4, 5, 6]]
        row6 = [x for x in range(3, 8, 1)]
        row7 = copy(row3)
        row8 = [x for x in range(11) if x not in [1, 5, 9]]
        row9 = copy(row3)
        rows = [row0, row1, row2, row3, row4, row5, row6, row7, row8, row8]

        i = 0
        for row in rows:
            print(f'row {i} = {row}');
            i += 1
        return rows

    def play(self):
        while not self.finished:
            gf.check_events(game=self)
            # self.screen.fill(self.settings.bg_color)
            self.maze.update()
            self.pacman.update()
            for star in self.stars_stars:
                star.update()
            # self.ghost.update()
            pg.display.flip()

def main():
    game = Game()
    game.play()


if __name__ == '__main__':
    main()

