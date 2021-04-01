import pygame as pg

class Sound:
    def __init__(self, bg_music):
        pg.mixer.init()
        pg.mixer.music.load(bg_music)
        pg.mixer.music.set_volume(0.5)
        eat_sound = pg.mixer.Sound('sounds/pacman_eat.wav')
        pg.mixer.Sound.set_volume(eat_sound, 0.22)
        eat_fruit_sound = pg.mixer.Sound('sounds/pacman_eat_fruit.wav')
        pg.mixer.Sound.set_volume(eat_fruit_sound, 0.22)
        eat_ghost_sound = pg.mixer.Sound('sounds/pacman_eat_ghost.wav')
        pg.mixer.Sound.set_volume(eat_ghost_sound, 0.22)
        death_sound = pg.mixer.Sound('sounds/pacman_death.wav')
        pg.mixer.Sound.set_volume(death_sound, 0.22)

        self.sounds = {'eat': eat_sound, 'eat_fruit': eat_fruit_sound, 'eat_ghost': eat_ghost_sound, 'death_sound': death_sound}
        self.playing_bg = None
        self.play()
        self.pause_bg()

    def pause_bg(self):
        self.playing_bg = False
        pg.mixer.music.pause()

    def unpause_bg(self):
        self.playing_bg = True
        pg.mixer.music.unpause()

    def play(self):
        self.playing_bg = True
        pg.mixer.music.play(-1, 0.0)

    def stop_bg(self):
        self.playing_bg = False
        pg.mixer.music.stop()

    def eat_points(self):
        pg.mixer.Sound.play(self.sounds['eat'])

    def eat_fruit(self):
        pg.mixer.Sound.play(self.sounds['eat_fruit'])

    def eat_ghost(self):
        pg.mixer.Sound.play(self.sounds['eat_ghost'])

    def death_sound(self):
        pg.mixer.Sound.play(self.sounds['death_sound'])