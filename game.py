import pygame as pg
from copy import copy
import game_functions as gf
from settings import Settings
from vector import Vector
from maze import Maze, GridPoint
from character import Pacman, Ghost
from math import atan2
from timer import Timer
from score import Score
import time
from button import Button
from game_stats import GameStats
from sound import Sound
from scoreboard import Scoreboard
from settings import Settings


class Game:
    def __init__(self):
        pg.init()
        self.settings = Settings()
        self.screen = pg.display.set_mode(size=(self.settings.screen_width, self.settings.screen_height))
        pg.display.set_caption("PacMan Portal")
        self.font = pg.font.SysFont(None, 48)

        self.play_button = self.stats = self.sb = None
        self.sound = Sound(bg_music="sounds/ghost_moving.wav")
        self.sound.play()
        self.sound.pause_bg()

        self.restart()


    def restart(self):
        self.maze = Maze(game=self)
        self.last_update = None
        self.last_exit = None
        self.last_idle = None
        self.isIdle = False

        self.play_button = Button(settings=self.settings, screen=self.screen, msg="Play")
        self.stats = GameStats(settings=self.settings)
        self.sb = Scoreboard(settings=self.settings, screen=self.screen, stats=self.stats)



        self.stars = [GridPoint(game=self, pt=Vector(x, 925),
                                index=index, adj_list=adj_list) for (index, x, adj_list) in [(0, 70, [1, 17]),
                                                                                             (1, 120, [0, 2]),
                                                                                             (2, 165, [1, 3]),
                                                                                             (3, 210, [2, 4]),
                                                                                             (4, 260, [3, 5]),
                                                                                             (5, 310, [4, 6]),
                                                                                             (6, 355, [5, 7]),
                                                                                             (7, 400, [6, 8, 24]),
                                                                                             (8, 450, [7, 9]),
                                                                                             (9, 500, [8, 10, 26]),
                                                                                             (10, 545, [9, 11]),
                                                                                             (11, 590, [10, 12]),
                                                                                             (12, 640, [11, 13]),
                                                                                             (13, 690, [12, 14]),
                                                                                             (14, 735, [13, 15]),
                                                                                             (15, 780, [14, 16]),
                                                                                             (16, 830, [15, 33])]]

        self.stars1 = [GridPoint(game=self, pt=Vector(x, 878),
                                 index=index, adj_list=adj_list) for (index, x, adj_list) in [(17, 70, [0, 34]),
                                                                                              (24, 400, [7, 41]),
                                                                                              (26, 500, [9, 43]),
                                                                                              (33, 830, [16, 50])]]

        self.stars2 = [GridPoint(game=self, pt=Vector(x, 831),
                                 index=index, adj_list=adj_list) for (index, x, adj_list) in [(34, 70, [17, 35]),
                                                                                              (35, 120, [34, 36, 52]),
                                                                                              (36, 165, [35, 37]),
                                                                                              (37, 210, [36, 54]),
                                                                                              (39, 310, [40, 56]),
                                                                                              (40, 355, [39, 41]),
                                                                                              (41, 400, [24, 40]),
                                                                                              (43, 500, [26, 44]),
                                                                                              (44, 545, [43, 45]),
                                                                                              (45, 590, [44, 62]),
                                                                                              (47, 690, [48, 64]),
                                                                                              (48, 735, [47, 49]),
                                                                                              (49, 780, [48, 50, 66]),
                                                                                              (50, 830, [33, 49])]]

        self.stars3 = [GridPoint(game=self, pt=Vector(x, 783),
                                 index=index, adj_list=adj_list) for (index, x, adj_list) in [(52, 120, [35, 69]),
                                                                                              (54, 210, [37, 71]),
                                                                                              (56, 310, [39, 73]),
                                                                                              (62, 590, [45, 79]),
                                                                                              (64, 690, [47, 81]),
                                                                                              (66, 780, [49, 83])]]

        self.stars4 = [GridPoint(game=self, pt=Vector(x, 735),
                                 index=index, adj_list=adj_list) for (index, x, adj_list) in [(68, 70, [69, 85]),
                                                                                              (69, 120, [52, 68]),
                                                                                              (71, 210, [54, 72, 88]),
                                                                                              (72, 260, [71, 73]),
                                                                                              (73, 310, [56, 72, 74]),
                                                                                              (74, 355, [73, 75]),
                                                                                              (75, 400, [74, 76, 92]),
                                                                                              (76, 450, [75, 77]),
                                                                                              (77, 500, [76, 78, 94]),
                                                                                              (78, 545, [77, 79]),
                                                                                              (79, 590, [62, 78, 80]),
                                                                                              (80, 640, [79, 81]),
                                                                                              (81, 690, [64, 80, 98]),
                                                                                              (83, 780, [66, 84]),
                                                                                              (84, 830, [83, 101])]]

        self.stars5 = [GridPoint(game=self, pt=Vector(x, 688),
                                 index=index, adj_list=adj_list) for (index, x, adj_list) in [(85, 70, [68, 102]),
                                                                                              (88, 210, [71, 105]),
                                                                                              (92, 400, [75, 109]),
                                                                                              (94, 500, [77, 111]),
                                                                                              (98, 690, [81, 115]),
                                                                                              (101, 830, [84, 118])]]

        self.stars6 = [GridPoint(game=self, pt=Vector(x, 641),
                                 index=index, adj_list=adj_list) for (index, x, adj_list) in [(102, 70, [85, 103]),
                                                                                              (103, 120, [102, 104]),
                                                                                              (104, 165, [103, 105]),
                                                                                              (105, 210, [88, 104, 106, 122]),
                                                                                              (106, 260, [105, 107]),
                                                                                              (107, 310, [106, 108, 124]),
                                                                                              (108, 355, [107, 109]),
                                                                                              (109, 400, [92, 108]),
                                                                                              (111, 500, [94, 112]),
                                                                                              (112, 545, [111, 113]),
                                                                                              (113, 590, [112, 114, 130]),
                                                                                              (114, 640, [113, 115]),
                                                                                              (115, 690, [98, 114, 116, 132]),
                                                                                              (116, 735, [115, 117]),
                                                                                              (117, 780, [116, 118]),
                                                                                              (118, 830, [101, 117])]]
        self.stars7 = [GridPoint(game=self, pt=Vector(x, 591),
                                 index=index, adj_list=adj_list) for (index, x, adj_list) in [(122, 210, [105, 139]),
                                                                                              (124, 310, [107, 141]),
                                                                                              (130, 590, [113, 147]),
                                                                                              (132, 690, [115, 149])]]

        self.stars8 = [GridPoint(game=self, pt=Vector(x, 541),
                                 index=index, adj_list=adj_list) for (index, x, adj_list) in [(139, 210, [122, 156]),
                                                                                              (141, 310, [124, 142, 158]),
                                                                                              (142, 355, [141, 143]),
                                                                                              (143, 400, [142, 144]),
                                                                                              (144, 450, [143, 145]),
                                                                                              (145, 500, [144, 146]),
                                                                                              (146, 545, [145, 147]),
                                                                                              (147, 590, [130, 146, 164]),
                                                                                              (149, 690, [132, 166])]]

        self.stars9 = [GridPoint(game=self, pt=Vector(x, 493),
                                 index=index, adj_list=adj_list) for (index, x, adj_list) in [(156, 210, [139, 173]),
                                                                                              (158, 310, [141, 175]),
                                                                                              (164, 590, [147, 181]),
                                                                                              (166, 690, [149, 183])]]

        self.stars10 = [GridPoint(game=self, pt=Vector(x, 445),
                                  index=index, adj_list=adj_list) for (index, x, adj_list) in [(170, 70, [171, 186]),
                                                                                               (171, 120, [170, 172]),
                                                                                               (172, 165, [171, 173]),
                                                                                               (173, 210, [156, 172, 174, 190]),
                                                                                               (174, 260, [173, 175]),
                                                                                               (175, 310, [158, 174, 192]),
                                                                                               (177, 400, [178]),
                                                                                               (178, 450, [177, 179, 212]),
                                                                                               (179, 500, [178]),
                                                                                               (181, 590, [164, 182, 198]),
                                                                                               (182, 640, [181, 183]),
                                                                                               (183, 690, [166, 182, 184, 200]),
                                                                                               (184, 735, [183, 185]),
                                                                                               (185, 780, [184, 186]),
                                                                                               (186, 830, [170, 185])]]

        self.stars11 = [GridPoint(game=self, pt=Vector(x, 397),
                                  index=index, adj_list=adj_list) for (index, x, adj_list) in [(190, 210, [173, 207]),
                                                                                               (192, 310, [175, 209]),
                                                                                               (198, 590, [181, 215]),
                                                                                               (200, 690, [183, 217])]]

        self.stars12 = [GridPoint(game=self, pt=Vector(x, 350),
                                  index=index, adj_list=adj_list) for (index, x, adj_list) in [(207, 210, [190, 224]),
                                                                                               (209, 310, [192, 210]),
                                                                                               (210, 355, [209, 211]),
                                                                                               (211, 400, [210, 212, 228]),
                                                                                               (212, 450, [211, 213]),
                                                                                               (213, 500, [212, 214, 230]),
                                                                                               (214, 545, [213, 215]),
                                                                                               (215, 590, [198, 214]),
                                                                                               (217, 690, [200, 234])]]

        self.stars13 = [GridPoint(game=self, pt=Vector(x, 303),
                                  index=index, adj_list=adj_list) for (index, x, adj_list) in [(224, 210, [207, 241]),
                                                                                               (228, 400, [211, 245]),
                                                                                               (230, 500, [213, 247]),
                                                                                               (234, 690, [217, 251])]]

        self.stars14 = [GridPoint(game=self, pt=Vector(x, 255),
                                  index=index, adj_list=adj_list) for (index, x, adj_list) in [(238, 70, [239, 255]),
                                                                                               (239, 120, [238, 240]),
                                                                                               (240, 165, [239, 241]),
                                                                                               (241, 210, [224, 240, 258]),
                                                                                               (243, 310, [244, 260]),
                                                                                               (244, 355, [243, 245]),
                                                                                               (245, 400, [228, 244]),
                                                                                               (247, 500, [230, 248]),
                                                                                               (248, 545, [247, 249]),
                                                                                               (249, 590, [248, 266]),
                                                                                               (251, 690, [234, 252, 268]),
                                                                                               (252, 735, [251, 253]),
                                                                                               (253, 780, [252, 254]),
                                                                                               (254, 830, [253, 271])]]

        self.stars15 = [GridPoint(game=self, pt=Vector(x, 208),
                                  index=index, adj_list=adj_list) for (index, x, adj_list) in [(255, 70, [238, 272]),
                                                                                               (258, 210, [241, 275]),
                                                                                               (260, 310, [243, 277]),
                                                                                               (266, 590, [249, 283]),
                                                                                               (268, 690, [251, 285]),
                                                                                               (271, 830, [254, 288])]]

        self.stars16 = [GridPoint(game=self, pt=Vector(x, 160),
                                  index=index, adj_list=adj_list) for (index, x, adj_list) in [(272, 70, [255, 273, 289]),
                                                                                               (273, 120, [272, 274]),
                                                                                               (274, 165, [273, 275]),
                                                                                               (275, 210, [258, 274, 276, 292]),
                                                                                               (276, 260, [275, 277]),
                                                                                               (277, 310, [260, 276, 278]),
                                                                                               (278, 355, [277, 279]),
                                                                                               (279, 400, [278, 280, 296]),
                                                                                               (280, 450, [279, 281]),
                                                                                               (281, 500, [280, 282, 298]),
                                                                                               (282, 545, [281, 283]),
                                                                                               (283, 590, [266, 282, 284]),
                                                                                               (284, 640, [283, 285]),
                                                                                               (285, 690, [268, 284, 286, 302]),
                                                                                               (286, 735, [285, 287]),
                                                                                               (287, 780, [286, 288]),
                                                                                               (288, 830, [271, 287, 305])]]

        self.stars17 = [GridPoint(game=self, pt=Vector(x, 115),
                                  index=index, adj_list=adj_list) for (index, x, adj_list) in [(289, 70, [272, 306]),
                                                                                               (292, 210, [275, 309]),
                                                                                               (296, 400, [279, 313]),
                                                                                               (298, 500, [281, 315]),
                                                                                               (302, 690, [285, 319]),
                                                                                               (305, 830, [288, 322])]]

        self.stars18 = [GridPoint(game=self, pt=Vector(x, 70),
                                  index=index, adj_list=adj_list) for (index, x, adj_list) in [(306, 70, [289, 307]),
                                                                                               (307, 120, [306, 308]),
                                                                                               (308, 165, [307, 309]),
                                                                                               (309, 210, [292, 308, 310]),
                                                                                               (310, 260, [309, 311]),
                                                                                               (311, 310, [310, 312]),
                                                                                               (312, 355, [311, 313]),
                                                                                               (313, 400, [296, 312]),
                                                                                               (315, 500, [298, 316]),
                                                                                               (316, 545, [315, 317]),
                                                                                               (317, 590, [316, 318]),
                                                                                               (318, 640, [317, 319]),
                                                                                               (319, 690, [302, 318, 320]),
                                                                                               (320, 735, [319, 321]),
                                                                                               (321, 780, [320, 322]),
                                                                                               (322, 830, [305, 321])]]

        self.stars_stars = self.stars + self.stars1 + self.stars2 + self.stars3 + self.stars4 + self.stars5 + self.stars6 + self.stars7 + self.stars8 + self.stars9 + self.stars10 + self.stars11 + self.stars12 + self.stars13 + self.stars14 + self.stars15 + self.stars16 + self.stars17 + self.stars18

        self.score = Score(game=self, stars=self.stars_stars)

        nxt = self.stars4[7]
        prev = self.stars4[7]

        self.pacman = self.blinky = self.pinky = self.inkey = self.clyde = self.ghosts = None

        self.blinky = Ghost(game=self, v=Vector(0, 0), pt=self.stars12[4].pt, grid_pt_next=self.stars12[4],
                            grid_pt_prev=self.stars12[4], stars=self.stars_stars, sound=self.sound, name='blinky')
        self.pinky = Ghost(game=self, v=Vector(0, 0), pt=self.stars10[6].pt, grid_pt_next=self.stars10[6],
                           grid_pt_prev=self.stars10[6], stars=self.stars_stars, sound=self.sound, name='pinky')
        self.inkey = Ghost(game=self, v=Vector(0, 0), pt=self.stars10[7].pt, grid_pt_next=self.stars10[7],
                           grid_pt_prev=self.stars10[7], stars=self.stars_stars, sound=self.sound, name='inkey')
        self.clyde = Ghost(game=self, v=Vector(0, 0), pt=self.stars10[8].pt, grid_pt_next=self.stars10[8],
                           grid_pt_prev=self.stars10[8], stars=self.stars_stars, sound=self.sound, name='clyde')

        self.ghosts = [self.blinky, self.inkey, self.pinky, self.clyde]

        self.pacman = Pacman(game=self, v=Vector(0, 0), pt=prev.pt, grid_pt_next=nxt, grid_pt_prev=prev, stats=self.stats, sb=self.sb, settings=self.settings, sound=self.sound)

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

            if not self.stats.game_active:
                self.play_button.draw()
                self.sound.pause_bg()
                quit_game = not gf.startup_screen(settings=self.settings, stats=self.stats, screen=self.screen)
                if quit_game:
                    pg.quit()
                    break

            if self.stats.game_active:
                self.screen.fill(self.settings.bg_color)
                self.sb.show_score()
                self.maze.update()
                self.score.update()
                self.pacman.performAction(self.score)
                self.pacman.update()

                if not self.pacman.dead:
                    now = pg.time.get_ticks()
                    if self.last_update is None and self.last_exit is None and self.last_idle is None:
                        self.last_update = pg.time.get_ticks()
                        self.last_exit = pg.time.get_ticks()
                        self.last_idle = pg.time.get_ticks()
                        for ghost in self.ghosts:
                            if not ghost.at_base():
                                ghost.chase = True
                                # ghost.a_star(self.pacman)
                    elif now > self.last_update + 700:
                        for ghost in self.ghosts:
                            if ghost.at_base():
                                if now > self.last_exit + 3000:
                                    ghost.exit()
                                    if not ghost.at_base():
                                        ghost.chase = True
                                    self.last_exit = pg.time.get_ticks()
                            elif now > self.last_idle + 100000 and not ghost.idle:
                                ghost.chase = False
                                ghost.idle = True
                                ghost.performAction(self.pacman)
                            elif now > self.last_idle + 20000 and ghost.idle:
                                ghost.idle = False
                                ghost.chase = True
                                self.last_idle = pg.time.get_ticks()
                                ghost.performAction(self.pacman)
                            else:
                                ghost.performAction(self.pacman)

                        self.last_update = pg.time.get_ticks()

                    for ghost in self.ghosts:
                        ghost.update()

                if self.pacman.dead:
                    if self.pacman.image.frame_index() == len(self.pacman.images):
                        self.reset()
                if not self.sound.playing_bg:
                    self.sound.unpause_bg()



            pg.display.flip()

        print('finish')

    def reset(self):
        if self.stats.lives_left != 0:
            self.stats.lives_left -= 1
            self.sb.prep_lives()
            time.sleep(1)
        else:
            self.stats.game_active = False
            self.stats.save_high_score()
            self.sound.pause_bg()
            self.restart()

def main():
    game = Game()
    game.play()


if __name__ == '__main__':
    main()
