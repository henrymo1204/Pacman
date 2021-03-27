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
        self.last_updated = None

        # li = [70, 400, 500, 830]
        # self.stars = []
        # for x in li:
        #     self.stars.append(GridPoint(game=self, pt=Vector(x, 925)))

        self.stars = [GridPoint(game=self, pt=Vector(x,925),
                                index=index, adj_list=adj_list) for (index,x,adj_list) in [(0, 70, [1, 11]),
                                                                                           (1, 120, [0, 2]),
                                                                                           (2, 210, [1, 3]),
                                                                                           (3, 310, [2, 4]),
                                                                                           (4, 400, [3, 5, 15]),
                                                                                           (5, 450, [4, 6]),
                                                                                           (6, 500, [5, 7, 17]),
                                                                                           (7, 590, [6, 8]),
                                                                                           (8, 690, [7, 9]),
                                                                                           (9, 780, [8, 10]),
                                                                                           (10, 830, [9, 21])]]

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
        self.stars2 = [GridPoint(game=self, pt=Vector(x, 735),
                                 index=index, adj_list=adj_list) for (index, x, adj_list) in [(22, 70,  [33, 23]),
                                                                                              (23, 120, [22, 12]),
                                                                                              (24, 210, [35, 25, 13]),
                                                                                              (25, 310, [24, 26, 14]),
                                                                                              (26, 400, [25, 27, 37]),
                                                                                              (27, 450, [26, 28]),
                                                                                              (28, 500, [27, 29, 39]),
                                                                                              (29, 590, [28, 30, 18]),
                                                                                              (30, 690, [29, 41, 19]),
                                                                                              (31, 780, [32, 20]),
                                                                                              (32, 830, [31, 43])]]
        self.stars3 = [GridPoint(game=self, pt=Vector(x, 641),
                                 index=index, adj_list=adj_list) for (index, x, adj_list) in [(33, 70,  [22, 34]),
                                                                                              (34, 120, [33, 35]),
                                                                                              (35, 210, [46, 34, 36, 24]),
                                                                                              (36, 310, [35, 37, 47]),
                                                                                              (37, 400, [36, 26]),
                                                                                              (39, 500, [28, 40]),
                                                                                              (40, 590, [39, 41, 51]),
                                                                                              (41, 690, [52, 40, 42, 30]),
                                                                                              (42, 780, [41, 43]),
                                                                                              (43, 830, [42, 32])]]
        self.stars4 = [GridPoint(game=self, pt=Vector(x, 541),
                                 index=index, adj_list=adj_list) for (index, x, adj_list) in [(46, 210, [35, 57]),
                                                                                              (47, 310, [58, 48, 36]),
                                                                                              (48, 400, [47, 49]),
                                                                                              (49, 450, [48, 50]),
                                                                                              (50, 500, [49, 51]),
                                                                                              (51, 590, [62, 50, 40]),
                                                                                              (52, 690, [41, 53])]]
        self.stars5 = [GridPoint(game=self, pt=Vector(x, 445),
                                 index=index, adj_list=adj_list) for (index, x, adj_list) in [(55, 70,  [65, 56]),
                                                                                              (56, 120, [55, 57]),
                                                                                              (57, 210, [46, 56, 58, 68]),
                                                                                              (58, 310, [47, 57, 69]),
                                                                                              (59, 400, [60]),
                                                                                              (60, 450, [59, 61, 71]),
                                                                                              (61, 500, [60]),
                                                                                              (62, 590, [51, 63, 73]),
                                                                                              (63, 690, [52, 62, 64, 74]),
                                                                                              (64, 780, [63, 65]),
                                                                                              (65, 830, [64, 55])]]
        self.stars6 = [GridPoint(game=self, pt=Vector(x, 350),
                                 index=index, adj_list=adj_list) for (index, x, adj_list) in [(68, 210, [57, 79]),
                                                                                              (69, 310, [58, 70]),
                                                                                              (70, 400, [69, 71, 81]),
                                                                                              (71, 450, [70, 72]),
                                                                                              (72, 500, [71, 73, 83]),
                                                                                              (73, 590, [72, 62]),
                                                                                              (74, 690, [63, 85])]]
        self.stars7 = [GridPoint(game=self, pt=Vector(x, 255),
                                 index=index, adj_list=adj_list) for (index, x, adj_list) in [(77, 70, [88, 78]),
                                                                                              (78, 120, [77, 79]),
                                                                                              (79, 210, [90, 78, 68]),
                                                                                              (80, 310, [91, 81]),
                                                                                              (81, 400, [80, 70]),
                                                                                              (83, 500, [84, 72]),
                                                                                              (84, 590, [83, 95]),
                                                                                              (85, 690, [96, 86, 74]),
                                                                                              (86, 780, [85, 87]),
                                                                                              (87, 830, [86, 98])]]
        self.stars8 = [GridPoint(game=self, pt=Vector(x, 160),
                                 index=index, adj_list=adj_list) for (index, x, adj_list) in [(88, 70, [77, 89, 99]),
                                                                                              (89, 120, [88, 90]),
                                                                                              (90, 210, [101, 89, 91, 79]),
                                                                                              (91, 310, [90, 92, 80]),
                                                                                              (92, 400, [103, 91, 93]),
                                                                                              (93, 450, [92, 94]),
                                                                                              (94, 500, [105, 93, 95]),
                                                                                              (95, 590, [94, 96, 84]),
                                                                                              (96, 690, [107, 95, 97, 85]),
                                                                                              (97, 780, [96, 98]),
                                                                                              (98, 830, [97, 109, 87])]]
        self.stars9 = [GridPoint(game=self, pt=Vector(x, 70),
                                 index=index, adj_list=adj_list) for (index, x, adj_list) in [(99, 70, [88, 100]),
                                                                                              (100, 120, [99, 101]),
                                                                                              (101, 210, [100, 102, 90]),
                                                                                              (102, 310, [101, 103]),
                                                                                              (103, 400, [102, 92]),
                                                                                              (105, 500, [94, 106]),
                                                                                              (106, 590, [105, 107]),
                                                                                              (107, 690, [106, 108, 96]),
                                                                                              (108, 780, [107, 109]),
                                                                                              (109, 830, [108, 98])]]
        self.stars_stars = self.stars + self.stars1 + self.stars2 + self.stars3 + self.stars4 + self.stars5 + self.stars6 + self.stars7 + self.stars8 + self.stars9

        # nxt = self.stars2[5]
        # prev = self.stars2[5]
        nxt = self.stars[0]
        prev = self.stars[0]

        self.pacman = Pacman(game=self, v=Vector(0, 0), pt=prev.pt, grid_pt_next=nxt, grid_pt_prev=prev)
        self.ghost = Ghost(game=self, v=Vector(0, 0), pt=self.stars6[3].pt, grid_pt_next=self.stars6[3], grid_pt_prev=self.stars6[3], pacman=self.pacman, stars=self.stars_stars)

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
        rows = [row0, row1, row2, row3, row4, row5, row6, row7, row8, row8, row9]

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

            now = pg.time.get_ticks()
            if self.last_updated is None:
                self.last_updated = pg.time.get_ticks()
                self.ghost.chase()
            elif now > self.last_updated + 3000:
                self.ghost.chase()
                self.last_updated = pg.time.get_ticks()
            self.ghost.update()
            pg.display.flip()

def main():
    game = Game()
    game.play()


if __name__ == '__main__':
    main()

