import pygame as pg
from pygame.examples.sprite_texture import sprite

import constants as c


class Turret(pg.sprite.Sprite):
    def __init__(self, sprite_sheet, tile_x, tile_y):
        pg.sprite.Sprite.__init__(self)

        #position variables
        self.tile_x = tile_x
        self.tile_y = tile_y
        #calculate center coordinates
        self.x = (self.tile_x + 0.5) * c.TILE_SIZE
        self.y = (self.tile_y + 0.5) * c.TILE_SIZE

        #animation variables
        self.sprite_sheet = sprite_sheet
        self.animations_list = self.load_images()
        self.frame_index = 0
        self.update_time = pg.time.get_ticks()


        #update image
        self.image = self.animations_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def load_images(self):
        #extract images from spritesheet
        size = self.sprite_sheet.get_height()
        animation_list = []
        for x in range(c.ANIMATION_STEPS):
            temp_img = self.sprite_sheet.subsurface(x * size, 0, size, size)
            animation_list.append(temp_img)
        return animation_list

    def update(self):
        self.play_animation()


    def play_animation(self):
        # update image
        self.image = self.animations_list[self.frame_index]
        # check if enough time has passed since the last update
        if pg.time.get_ticks() - self.update_time > c.ANIMATION_DELAY:
            self.update_time = pg.time.get_ticks()
            self.frame_index += 1
            if self.frame_index >= len(self.animations_list):
                self.frame_index = 0
