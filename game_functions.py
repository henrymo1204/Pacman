import sys
import pygame as pg
from vector import Vector

swapped = False
li = [pg.K_RIGHT, pg.K_LEFT, pg.K_UP, pg.K_DOWN]
di = {pg.K_RIGHT : Vector(1, 0), pg.K_LEFT : Vector(-1, 0),
      pg.K_UP : Vector(0, -1), pg.K_DOWN : Vector(0, 1)}

def check_keydown_events(event, pacman, stars):
    global swapped
    if event.key in li and not swapped:
        v, new_dir = pacman.v, di[event.key]
        if not pacman.on_star():
            if v.dot(new_dir) == -1:
                pacman.reverse()
            return
        # choose next star for destination
        v = di[event.key]
        delta = (v.x if v.y == 0 else -11 * v.y)
        print(delta)
        proposed_next_grid_pt = pacman.grid_pt_next.index + delta

        pacman.grid_pt_prev = pacman.grid_pt_next
        index = int(pacman.grid_pt_next.index + delta)
        pacman.grid_pt_next.make_normal()
        for star in stars:
            if star.index == index:
                pacman.grid_pt_next = star
                break
        pacman.grid_pt_next.make_next()
        print(pacman.grid_pt_next.pt)

        pacman.v = di[event.key]
        pacman.scale_factor = 1.0
        pacman.update_angle()

def check_keyup_events(event, pacman):
    global swapped
    if event.key in li and swapped:
        pacman.scale_factor = 0
        swapped = False
    # if event.key == pg.K_q: ship.shooting_bullets = False

# def check_play_button(stats, play_button, mouse_x, mouse_y):
#     if play_button.rect.collidepoint(mouse_x, mouse_y):
#         stats.game_active = True

def check_events(game):
    # Watch for keyboard and mouse events.
    for event in pg.event.get():
        if event.type == pg.QUIT: game.finished = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pg.mouse.get_pos()
            # check_play_button(stats=game.stats, play_button=game.play_button, mouse_x=mouse_x, mouse_y=mouse_y)
        elif event.type == pg.KEYDOWN: check_keydown_events(event=event, pacman=game.pacman, stars=game.stars_stars)
        elif event.type == pg.KEYUP: check_keyup_events(event=event, pacman=game.pacman)

