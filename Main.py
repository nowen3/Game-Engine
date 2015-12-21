#!/usr/bin/python
# -*- coding: utf-8 -*-

import os.path
import pygame
from Map import Maps
import Constants


def init_game():
    pygame.init()
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    Constants.SCREEN = pygame.display.set_mode((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT), pygame.DOUBLEBUF)


def main():
    init_game()
    # list of all level maps
    level_list = [os.path.join('images', 'level1.tmx'), os.path.join('images', 'level2.tmx')]
    # Set the current level
    current_level_no = 0
    # load map level 1
    mymap = Maps(level_list[current_level_no])
    done = False
    clock = pygame.time.Clock()
    while not done:
        # Do state event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True  # exit game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    done = True  # exit game
                # if event.key == pygame.K_LEFT:
                #   player.go_left()
                # if event.key == pygame.K_RIGHT:
                 #  player.go_right()
                # if event.key == pygame.K_UP:
                #   player.jump()
            # elif event.type == pygame.KEYUP:
                # if event.key == pygame.K_LEFT and player.change_x < 0:
                #   player.stop()
                # if event.key == pygame.K_RIGHT and player.change_x > 0:
                 #  player.stop()

        mymap.render('Background')
        pygame.display.flip()
        clock.tick(Constants.FPS)

    return 0


if __name__ == '__main__':
    main()
