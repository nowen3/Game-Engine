import sys
import pygame
import Constants

if sys.version[0] == '3':
    xrange = range


class Tileset(object):
    def __init__(self, myfile):
        self.image = pygame.image.load(myfile).convert_alpha()
        self.tiles = []
        if not self.image:
            print("Error creating new Tileset: file {} not found".format(myfile))

    def loadsheet(self, tile_width, tile_height):
        self.tile_width = tile_width
        self.tile_height = tile_height

        for line in xrange(int(self.image.get_height() / self.tile_height)):
            for column in xrange(int(self.image.get_width() / self.tile_width)):
                pos = pygame.Rect(
                    column * self.tile_width,
                    line * self.tile_height,
                    self.tile_width,
                    self.tile_height)

                self.tiles.append(self.image.subsurface(pos))

    def get_image(self, x, y, width, height):
        """ Grab a single image out of a larger spritesheet
            Pass in the x, y location of the sprite
            and the width and height of the sprite. """

        # Create a new blank image
        tempimage = pygame.Surface([width, height]).convert()

        # Copy the sprite from the large sheet onto the smaller image
        tempimage.blit(self.image, (0, 0), (x, y, width, height))

        # Assuming black works as the transparent color
        tempimage.set_colorkey(Constants.BLACK)

        # Return the image
        return tempimage

    def get_tile(self, gid):
        return self.tiles[gid]

    def get_tile_count(self):
        return self.tiles.count

    def get_tiles(self):
        return self.tiles