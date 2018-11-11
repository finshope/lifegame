#!/usr/bin/env python3

import random
import time
import sys

import pygame
from pygame.locals import *
import pygame.surfarray as surfarray        # for performance
import numpy as np

import colors       # color definition


SCREEN_SIZE = (1600, 900)                   # change it to your screen size
#color definitions
#           (r,     g,      b)
RED   =     (255,   0,      0)
BLACK =     (0,     0,      0)
WHITE =     (255,   255,    255)
GREEN =     (0,     255,    0)
BLUE  =     (0,     0,      128)

BG_COLOR = BLACK
CELL_COLOR = GREEN


def main():
    """\
Press 'a' to decrease max possible fps.
Press 'd' to increase max possible fps.
Press 's' for no max fps limit.
Press 'z' to decrease length of cell side.
Press 'x' to increase length of cell side.
Press 'p' to pause the game.
"""
    side = 50                                   # length of cell side
    width = int(SCREEN_SIZE[0] / side)  # number of cells per row 
    height = int(SCREEN_SIZE[1] / side) # number of cellls per column
    pygame.init()
    pygame.mouse.set_visible(False)
    SURF = pygame.display.set_mode(SCREEN_SIZE,FULLSCREEN,32);
    fontObj = pygame.font.Font('freesansbold.ttf',32);

    FPSCLOCK = pygame.time.Clock()
    fps = 5                                     # max fps 
    maps, slices = generate_random_map(width, height, side);
    pre_frame_time = time.time()                # time of previous frame
    paused = False
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == K_a and FPS > 1:
                    FPS -= 1
                if event.key == K_d and FPS < 60:
                    FPS += 1
                if event.key == K_p:
                    paused = not paused
                if event.key == K_f:
                    maps[random.randint(1, width), random.randint(1, height)] = True
                if event.key == K_k:
                    maps[random.randint(1, width), :] = True
                if event.key == K_l:
                    maps[:, random.randint(1, height)] = True
                if event.key == K_z and side > 5:
                    side -= 5
                    if side == 15:
                        side = 10
                    width = int(SCREEN_SIZE[0] / side);
                    height = int(SCREEN_SIZE[1] / side);
                    maps, slices = generate_random_map(width, height, side)
                if event.key == K_x and side < 100:
                    side += 5
                    if side == 15:
                        side = 20
                    width = int(SCREEN_SIZE[0] / side);
                    height = int(SCREEN_SIZE[1] / side);
                    maps, slices = generate_random_map(width, height, side)
                if event.key == K_s:
                    fps = 0
                if event.key == K_r:
                    maps, slices = generate_random_map(width, height, side)

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        SURF.fill(BG_COLOR)

        show_map(SURF, maps, side, slices)
        if not paused:
            maps = update(maps)

        current_frame_time = time.time()
        textSURF = fontObj.render('real fps: ' + str(1//(current_frame_time-pre_frame_time)), True, colors.random_color());
        pre_frame_time = current_frame_time
        textRect = textSURF.get_rect();
        textRect.topright = (SCREEN_SIZE[0],200);
        SURF.blit(textSURF,textRect);

        textSURF = fontObj.render('length of side: ' +  str(side), True, colors.random_color());
        textRect = textSURF.get_rect();
        textRect.topright = (SCREEN_SIZE[0],100);
        SURF.blit(textSURF,textRect);

        pygame.display.update();
        FPSCLOCK.tick(fps)


def generate_random_map(width, height, side):
    """\
Generate a larger sized map than given width, height.
Define slices for quickly drawing with small length of side.
Return generated map and slices.
"""
    slices = None
    if side < 10:
        K = side
        Y, X = SCREEN_SIZE
        slices = []
        for y in range(0, K):
            for x in range(0, K):
                s = slice(y, Y, K), slice(x, X, K)
                slices.append(s)

    maps = np.zeros((width+2, height+2), dtype=np.bool)
    for col in range(width):
        n_cell = random.randint(0, height)
        col_map = n_cell * [np.bool(1)]
        col_map.extend([np.bool(0)] * (height-n_cell))
        assert len(col_map) == height 
        random.shuffle(col_map)
        maps[col+1,1:-1] = col_map
    return (maps, slices)

def show_map(SURF, _map, side, slices=None):
    """\
Draw the map to surface SURF. If side is to small, pass in slices returned
by generate_random_map.
"""
    _map = _map[1:-1, 1:-1]

    if slices is not None:
        bit_map = np.zeros(SCREEN_SIZE, dtype=np.bool)
        for s in slices:
            bit_map[s] = _map

        bit_map = bit_map * SURF.map_rgb(colors.random_color())
        surfarray.blit_array(SURF, bit_map)
    else:
        cell_surf = pygame.Surface((side,side))
        for w in range(_map.shape[0]):
            for h in range(_map.shape[1]):
                if _map[w][h]:
                    cell_surf.fill(colors.random_color())
                    SURF.blit(cell_surf, (w * side, h * side))

def update(oldmap):
    """\
Update the status fo every cell according to arround live cells.
"""
    nbrs_count = sum(np.roll(np.roll(oldmap, i, 0), j, 1)
                for i in (-1, 0, 1) for j in (-1, 0, 1)
                if (i != 0 or j != 0))
    _newmap = (nbrs_count == 3) | (oldmap & (nbrs_count == 2))
    newmap = np.zeros(oldmap.shape, dtype=np.bool)
    newmap[1:-1, 1:-1] = _newmap[1:-1, 1:-1]
    return newmap

if __name__ == '__main__':
    main()
