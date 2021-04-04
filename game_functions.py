import sys
import pygame as pg
from vector import Vector
from button import Button
from menu import Button, Intro, Ufo
from highscore import HighScoreScreen
from portal import Portal

swapped = False
li = [pg.K_RIGHT, pg.K_LEFT, pg.K_UP, pg.K_DOWN]
di = {pg.K_RIGHT: Vector(1, 0), pg.K_LEFT: Vector(-1, 0),
      pg.K_UP: Vector(0, -1), pg.K_DOWN: Vector(0, 1)}


def check_keydown_events(event, game):
    global swapped
    if event.key in li and not swapped:
        pacman = game.pacman
        stars = game.stars_stars
        v, new_dir = pacman.v, di[event.key]
        if not pacman.on_star():
            if v.dot(new_dir) == -1:
                pacman.reverse()
                pacman.update_angle()
            return
        # choose next star for destination

        v = di[event.key]
        delta = (v.x if v.y == 0 else -17 * v.y)

        pacman.grid_pt_prev = pacman.grid_pt_next
        index = int(pacman.grid_pt_next.index + delta)
        pacman.grid_pt_next.make_normal()
        temp = None
        if index == 169:
            index = 186
        elif index == 187:
            index = 170
        for star in stars:
            if star.index == index:
                if index in pacman.grid_pt_next.adj_list:
                    temp = star
                    break
        if not temp:
            pacman.enterPortal(game.portals)
        else:
            pacman.grid_pt_next = temp
            pacman.grid_pt_next.make_next()

        if not pacman.v == di[event.key]:
            pacman.v = di[event.key]
            pacman.scale_factor = 1.0
            pacman.update_angle()
    elif event.key == pg.K_SPACE and not swapped:
        if game.pacman.v != Vector(0, 0):
            if len(game.portals) < 2:
                if len(game.portals) == 1:
                    if not game.portals[0].wall is None:
                        game.portals.append(Portal(game=game))
                        if len(game.portals) == 2:
                            game.portal_time = pg.time.get_ticks()
                else:
                    game.portals.append(Portal(game=game))
                    if len(game.portals) == 2:
                        game.portal_time = pg.time.get_ticks()

def check_keyup_events(event, pacman):
    global swapped
    if event.key in li and swapped:
        pacman.scale_factor = 0
        swapped = False
    # if event.key == pg.K_q: ship.shooting_bullets = False


# def check_play_button(stats, play_button, mouse_x, mouse_y):
#     if play_button.rect.collidepoint(mouse_x, mouse_y):
#         stats.game_active = True
#
# def check_space_bar_events(event, game):
#     global swapped
#     if swapped:
#         pacman = game.pacman
#         walls = game.walls_walls
#         game.portal = Portal(v=pacman.v, walls=walls, pt=pacman.pt)


def check_events(game):
    # Watch for keyboard and mouse events.
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game.finished = True
        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pg.mouse.get_pos()
            # check_play_button(stats=game.stats, play_button=game.play_button, mouse_x=mouse_x, mouse_y=mouse_y)
        elif event.type == pg.KEYDOWN:
            check_keydown_events(event=event, game=game)
        elif event.type == pg.KEYUP:
            check_keyup_events(event=event, pacman=game.pacman)


def check_play_button(stats, play_button, mouse_x, mouse_y):
    if play_button.rect.collidepoint(mouse_x, mouse_y):
        stats.game_active = True


def startup_screen(settings, stats, screen):
    """Display the startup menu on the screen, return False if the user wishes to quit,
    True if they are ready to play"""
    menu = Intro(settings, stats, screen)
    play_button = Button(settings, screen, 'Play Game', y_factor=0.80)
    hs_button = Button(settings, screen, 'High Scores', y_factor=0.90)
    animation = Ufo(settings, screen)
    intro = True

    while intro:
        play_button.alter_text_color(*pg.mouse.get_pos())
        hs_button.alter_text_color(*pg.mouse.get_pos())
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
            elif event.type == pg.MOUSEBUTTONDOWN:
                click_x, click_y = pg.mouse.get_pos()
                stats.game_active = play_button.check_button(click_x, click_y)
                intro = not stats.game_active
                animation.set_timer_zero()
                if hs_button.check_button(click_x, click_y):
                    ret_hs = high_score_screen(settings, stats, screen)
                    if not ret_hs:
                        return False
        screen.fill(settings.bg_color)
        menu.draw()
        hs_button.draw_button()
        play_button.draw_button()

        animation.draw()
        animation.update()

        pg.display.flip()

    return True


def high_score_screen(settings, stats, screen):
    """Display all high scores in a separate screen with a back button"""
    hs_screen = HighScoreScreen(settings, screen, stats)
    back_button = Button(settings, screen, 'Back To Menu', y_factor=0.85)

    while True:
        back_button.alter_text_color(*pg.mouse.get_pos())
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if back_button.check_button(*pg.mouse.get_pos()):
                    return True
        screen.fill(settings.bg_color)
        hs_screen.show_scores()
        back_button.draw_button()
        pg.display.flip()
