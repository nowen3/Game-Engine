import os.path
import pygame
from xml.etree import ElementTree
from Platform import MovingBaddy


class TMXparse(object):
    def __init__(self, filename):
        self.tmxfilename = filename
        self.columns = 0
        self.rows = 0
        self.tile_width = 0
        self.tile_height = 0
        self.tileimagepath = None
        self.layerlist = []
        self.background_image = None
        self.Baddy_list = pygame.sprite.Group()

    def parse(self):
        # image = None
        if os.path.isfile(self.tmxfilename):
            with open(self.tmxfilename, 'rt') as f:
                tree = ElementTree.parse(f)
                root = tree.getroot()
                # read basic map info
                self.columns = int(root.attrib['width'])  # no of columns
                self.rows = int(root.attrib['height'])  # no of rows
                self.tile_width = int(root.attrib['tilewidth'])
                self.tile_height = int(root.attrib['tileheight'])
                self.image = pygame.Surface(
                    [self.columns * self.tile_width, self.rows * self.tile_height]).convert()
                tileset = tree.find('tileset/image')
                self.tileimagepath = os.path.join('images',tileset.attrib['source'])
                backgroundimage = tree.find('properties/property')
                self.background_image = backgroundimage.attrib['value']

                # Read Objects
                for subobject in tree.findall('objectgroup'):
                    if subobject.attrib['name'] == 'Object_Baddy':
                        for layer_object in subobject.findall('object'):
                            bad = MovingBaddy(layer_object.attrib['type'] + '.png'
                                              , int(layer_object.attrib['x']), int(layer_object.attrib['y'])
                                              , int(layer_object.attrib['width']), int(layer_object.attrib['height'])
                                              )
                            self.Baddy_list.add(bad)
                # read the layers and store in mylayer class
                for subnode in tree.findall('layer'):
                    i = 0
                    newlayer = Mylayer(
                        subnode.attrib['name'], subnode.attrib['width'], subnode.attrib['height'])
                    # Read the properties for the layer, ie amount of up and down, side to side
                    for layer_props in subnode.findall('properties/property'):
                        newlayer.addprops(layer_props.attrib['name'], layer_props.attrib['value'])
                    # read all the tile data and add to an array
                    for child in subnode.findall('data/tile'):
                        gid = int(child.attrib['gid']) - 1
                        if gid < 0:
                            gid = 0
                        newlayer.adddata(i, gid)
                        i += 1
                    self.layerlist.append(newlayer)

    def getlayers(self):
        return self.layerlist

    def getbackground_image(self):
        return self.background_image

    def getbaddy(self):
        return self.Baddy_list


class Mylayer(object):
    def __init__(self, name, width, height):
        self.layername = name
        self.width = width
        self.height = height
        self.layerdata = {}
        self.layerprops = {}

    def adddata(self, key, gud):
        self.layerdata[key] = gud

    def addprops(self, key, gud):
        self.layerprops[key] = gud
