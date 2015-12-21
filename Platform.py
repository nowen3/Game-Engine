import pygame
import os.path
from MyTileset import Tileset
import Constants

class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """

    def __init__(self, tile_image):
        pygame.sprite.Sprite.__init__(self)
        self.image = tile_image
        self.rect = self.image.get_rect()


class MovingPlatform(Platform):
    """ This is a fancier platform that can actually move. """
    change_x = 0
    change_y = 0
    start_x = 0
    start_y = 0
    move_distance_x = 0
    move_distance_y = 0

    def update(self):
        # Move left/right
        self.rect.x += self.change_x
        # Move up/down
        self.rect.y += self.change_y
        if self.change_y != 0:
            if self.start_y - self.rect.y >= self.move_distance_y:
                self.change_y *= -1
            if self.rect.y >= self.start_y:
                self.change_y *= -1
        if self.change_x != 0:
            if self.rect.x - self.start_x >= self.move_distance_x:
                self.change_x *= -1
            if self.rect.x <= self.start_x:
                self.change_x *= -1


class BaseBad(pygame.sprite.Sprite):
    """ Baddy base class """

    def __init__(self, tile_image, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        sprite_sheet = Tileset(os.path.join('images', tile_image))
        sprite_sheet.loadsheet(width, height)
        self.images = sprite_sheet.get_tiles()
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class MovingBaddy(BaseBad):
    change_x = 1
    change_y = 0
    xpos = 0
    ypos = 0
    change = 0

    def update(self, hit):
        if hit > 0:
            if self.change_x == 1:
                self.change_x = -1
                self.image = pygame.transform.flip(self.image, True, False)
            else:
                self.change_x = 1
                self.image = pygame.transform.flip(self.image, True, False)
         # Move left/right
        self.rect.x += self.change_x
        # Move up/down
        self.rect.y += self.change_y
        if self.rect.x < 0:
            self.rect.x = 0
        self.xpos = self.rect.x
        self.ypos = self.rect.y

    def change_direction(self):
        if self.change_x == 1:
            self.change_x = -1
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.change_x = 1
            self.image = pygame.transform.flip(self.image, True, False)

    @property
    def get_x(self):
        return self.xpos

    @property
    def get_y(self):
        return self.ypos