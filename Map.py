import os.path
import math
import pygame
from MyTileset import Tileset
import Constants
from Platform import Platform, MovingPlatform, MovingBaddy
from TMXparse import TMXparse

class Maps(object):
    platform_list = None
    moving_platform_list = None
    Baddy_list = None
    background = None

    def __init__(self, filename):
        self.Surface = Constants.SCREEN
        self.image = None
        self.tile = None
        # create lists groups for the platforms
        self.platform_list = pygame.sprite.Group()
        self.moving_platform_list = pygame.sprite.Group()
        self.Baddy_list = pygame.sprite.Group()
        # create a TMXparse object and loadm the map
        self.mapparse = TMXparse(filename)
        self.mapparse.parse()
        # load background image
        self.background = pygame.image.load(os.path.join('images', self.mapparse.getbackground_image())).convert()
        # load the tilesets
        self.mytileset = Tileset(self.mapparse.tileimagepath)
        self.mytileset.loadsheet(self.mapparse.tile_width, self.mapparse.tile_height)
        self.add_layer_to_group("Background")
        # add baddys  #
        self.Baddy_list = self.mapparse.getbaddy()
        for myvalue in self.mapparse.layerlist:
            if myvalue.layerprops != "":
                x = 0
                y = 0
                platform = 1
                for key, value in myvalue.layerdata.iteritems():
                    if value > 0:
                        self.tile = self.mytileset.get_tile(value)
                        block = MovingPlatform(self.tile)
                        block.rect.x = x * self.mapparse.tile_width
                        block.rect.y = y * self.mapparse.tile_height
                        if myvalue.layername == "UP":
                            block.change_y = -1
                            block.change_x = 0
                            block.start_x = block.rect.x
                            block.start_y = block.rect.y
                            block.move_distance_y = int(myvalue.layerprops[str(platform)])
                            block.type = "UP"
                            if myvalue.layerdata[key + 1] == 0:
                                platform += 1
                        if myvalue.layername == "SIDE":
                            block.change_y = 0
                            block.change_x = 1
                            block.start_x = block.rect.x
                            block.start_y = block.rect.y
                            block.move_distance_x = int(myvalue.layerprops[str(platform)])
                            block.type = "SIDE"
                            if myvalue.layerdata[key + 1] == 0:
                                platform += 1

                        self.moving_platform_list.add(block)
                    x += 1
                    if x >= self.mapparse.columns:
                        y += 1
                        x = 0

    def add_layer_to_group(self, name):
        # load platforms from layers and store in a group
        for myvalue in self.mapparse.layerlist:
            if myvalue.layername == name:
                x = 0
                y = 0
                for key, value in myvalue.layerdata.iteritems():
                    if value > 0:
                        self.tile = self.mytileset.get_tile(value)
                        block = Platform(self.tile)
                        block.rect.x = x * self.mapparse.tile_width
                        block.rect.y = y * self.mapparse.tile_height
                        self.platform_list.add(block)

                    x += 1
                    if x >= self.mapparse.columns:
                        y += 1
                        x = 0

    def render(self, name):
        Constants.SCREEN.blit(self.background, [0, 0])
        self.moving_platform_list.update()
        self.moving_platform_list.draw(Constants.SCREEN)
        # self.Baddy_list.update(self.platform_list)
        self.update_baddys()
        self.Baddy_list.draw(Constants.SCREEN)

        for myvalue in self.mapparse.layerlist:
            if myvalue.layername == name:
                x = 0
                y = 0
                for key, value in myvalue.layerdata.iteritems():
                    if value > 0:
                        self.tile = self.mytileset.get_tile(value)
                        pos = (x * self.mapparse.tile_width, y * self.mapparse.tile_height)
                        self.Surface.blit(self.tile, pos)
                    x += 1
                    if x >= self.mapparse.columns:
                        y += 1
                        x = 0

    def get_tile_from_cords(self, x, y):
        try:
            tiledown = (math.ceil(float(y) / self.mapparse.tile_height))+1
            tileacross = math.ceil(x / self.mapparse.tile_width)
            tileno = ((int(self.mapparse.layerlist[0].width) * (tiledown - 1)) + tileacross) + 1
            if tileno < 0:
                tileno = 0
            return self.mapparse.layerlist[0].layerdata[tileno]

        except IndexError:
            print(
                "Index error {0}--{1}".format(str(int(math.ceil(y / 25))), str(int(math.ceil(x / 25)))))

    def update_baddys(self):
        for bad in self.Baddy_list.sprites():
            bad_x = bad.get_x
            bad_y = bad.get_y
            tile = self.get_tile_from_cords(bad_x, bad_y)
            bad.update(tile)
            for badcol in self.Baddy_list.sprites():
                if bad_x - badcol.get_x > 5:
                    bad.update(1)
                    badcol.update(1)


