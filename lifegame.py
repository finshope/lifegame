#!/usr/bin/env python3

import random
import time
import sys

import pygame
from pygame.locals import *
import pygame.surfarray as surfarray
import numpy as np

import colors


SCREEN_SIZE=(1600,900)
SIDE=50
CELL_SIZE=(SIDE,SIDE)
WIDTH=int(SCREEN_SIZE[0]/CELL_SIZE[0]);
HEIGHT=int(SCREEN_SIZE[1]/CELL_SIZE[1]);
#color definitions
#           (r,     g,      b)
RED   =     (255,   0,      0);
BLACK =     (0,     0,      0);
WHITE =     (255,   255,    255);
GREEN =     (0,     255,    0);
BLUE  =     (0,     0,      128);
BG_COLOR=BLACK
GRID_COLOR=BLUE
CELL_COLOR=GREEN


def main():
    global SURF, WIDTH, HEIGHT, CELL_SIZE
    global SIDE
    count = 0
    pygame.init()
    pygame.mouse.set_visible(False)
    SURF = pygame.display.set_mode(SCREEN_SIZE,FULLSCREEN,32);
    fontObj = pygame.font.Font('freesansbold.ttf',32);
    FPSCLOCK = pygame.time.Clock()
    FPS = 5
    maps = generate_random_map(WIDTH,HEIGHT);
    pre_frame_time = time.time()
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
                    maps[random.randint(0,WIDTH-1),random.randint(0,HEIGHT-1)]=True
                if event.key == K_z and SIDE > 5:
                    SIDE -= 5
                    if SIDE == 15:
                        SIDE = 10
                    CELL_SIZE=(SIDE, SIDE)
                    WIDTH=int(SCREEN_SIZE[0]/CELL_SIZE[0]);
                    HEIGHT=int(SCREEN_SIZE[1]/CELL_SIZE[1]);
                    maps = generate_random_map(WIDTH, HEIGHT)
                if event.key == K_x and CELL_SIZE[0] < 100:
                    SIDE += 5
                    if SIDE == 15:
                        SIDE = 20
                    CELL_SIZE = (SIDE, SIDE)
                    WIDTH=int(SCREEN_SIZE[0]/CELL_SIZE[0]);
                    HEIGHT=int(SCREEN_SIZE[1]/CELL_SIZE[1]);
                    maps = generate_random_map(WIDTH, HEIGHT)
                if event.key == K_s:
                    FPS = 0
                if event.key == K_r:
                    maps = generate_random_map(WIDTH,HEIGHT)

            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        SURF.fill(BG_COLOR)

        count += 1

        #draw grid
        #for i in range(1,WIDTH):
        #    pygame.draw.line(SURF, GRID_COLOR,(i*CELL_SIZE[0],0),(i*CELL_SIZE[0],SCREEN_SIZE[1]))
        #for i in range(1,HEIGHT):
        #    pygame.draw.line(SURF, GRID_COLOR,(0,i*CELL_SIZE[1]),(SCREEN_SIZE[0],i*CELL_SIZE[1]))
        show_map(maps)
        if not paused:
            maps = update(maps)


        current_frame_time = time.time()
        textSURF = fontObj.render('real fps: ' + str(1//(current_frame_time-pre_frame_time)), True, colors.random_color());
        pre_frame_time = current_frame_time
        textRect = textSURF.get_rect();
        textRect.topright = (SCREEN_SIZE[0],200);
        SURF.blit(textSURF,textRect);

        textSURF = fontObj.render('length of side: ' +  str(SIDE), True, colors.random_color());
        textRect = textSURF.get_rect();
        textRect.topright = (SCREEN_SIZE[0],100);
        SURF.blit(textSURF,textRect);

        pygame.display.update();
        FPSCLOCK.tick(FPS)


def generate_random_map(HEIGHT,WIDTH):
    global myslices, a_x
    K = CELL_SIZE[0]
    a_x = np.zeros(SCREEN_SIZE, dtype=np.bool)
    Y = a_x.shape[0]
    X = a_x.shape[1]
    myslices = []
    for y in range(0, K):
        for x in range(0, K):
            s = slice(y, Y, K), slice(x, X, K)
            myslices.append(s)
    print('HEIGHT=',HEIGHT,  ' WIDTH=',WIDTH, 'block_side=', CELL_SIZE[0])
    maps = np.zeros((HEIGHT+2,WIDTH+2), dtype=np.bool)
    for row in range(HEIGHT):
        n_cell = random.randint(0, WIDTH)
        row_map = n_cell * [np.bool(1)]
        row_map.extend([np.bool(0)]*(WIDTH-n_cell))
        assert len(row_map) == WIDTH
        random.shuffle(row_map)
        maps[row+1,1:-1] = row_map
    return maps

def show_map(maps):
    global myslices, a_x
    maps = maps[1:WIDTH+1,1:HEIGHT+1]

    #map_array = np.kron(maps,block)

    #map_array = maps.repeat(CELL_SIZE[0],axis=0).repeat(CELL_SIZE[1],axis=1)
    
    if CELL_SIZE[0] < 10:
        for s in myslices:
            a_x[s] = maps
        map_array = a_x

        map_array = map_array * SURF.map_rgb(colors.random_color())
        surfarray.blit_array(SURF, map_array)
    else:
        cell_surf = pygame.Surface(CELL_SIZE)
        for w in range(WIDTH):
            for h in range(HEIGHT):
                if maps[w][h]:
                    cell_surf.fill(colors.random_color())
                    SURF.blit(cell_surf, (w * CELL_SIZE[0], h * CELL_SIZE[1]))



                #SURF.blit(cell_surf,(x*CELL_SIZE[0], y * CELL_SIZE[1]))



                #tmp_surf.fill(colors.random_color(), rect=(x*CELL_SIZE[0],y*CELL_SIZE[1],CELL_SIZE[0],CELL_SIZE[1]))

                #tmp_surf.blit(cell_surf, (x*CELL_SIZE[0], y * CELL_SIZE[1]))

#                pygame.draw.rect(SURF, colors.random_color(), (x*CELL_SIZE[0],y*CELL_SIZE[1],CELL_SIZE[0],CELL_SIZE[1]))
    #surfarray.blit_array(SURF, dest)
    #SURF.blit(tmp_surf,(0,0))

def update(maps):
    nbrs_count = sum(np.roll(np.roll(maps, i, 0), j, 1)
                for i in (-1, 0, 1) for j in (-1, 0, 1)
                if (i != 0 or j != 0))
    _newmaps = (nbrs_count == 3) | (maps & (nbrs_count == 2))
    newmaps = np.zeros((WIDTH+2,HEIGHT+2), dtype=np.bool)
    newmaps[1:WIDTH+1, 1:HEIGHT+1] = _newmaps[1:WIDTH+1, 1:HEIGHT+1]
#    newmaps = np.zeros((HEIGHT+2,WIDTH+2), dtype=np.bool)
#    for y in range(HEIGHT):
#        row_cell = []
#        y += 1
#        for x in range(WIDTH):
#            count = 0
#            x += 1
#            count = np.sum(maps[y-1:y+2,x-1:x+2]) - maps[y, x]
#            if count==3:
#                newmaps[y][x] = np.bool(1)
#row_cell.append(True)
#            elif count==2:
#                newmaps[y][x] = maps[y][x]
#row_cell.append(maps[y][x])
#            else:
#                newmaps[y][x] = np.bool(0)
#row_cell.append(False)
#if random.randint(0,HEIGHT*WIDTH-1) % 65536 == 0:
#               newmaps[y][x] = True
#row_cell[-1] = True
#assert len(row_cell) == (WIDTH-1)
#    random_y = random.choice(range(0,HEIGHT))
#    random_x = random.choice(range(0,WIDTH))
#    newmaps[random_x+1][random_y+1] = np.bool(1)
    return newmaps


if __name__ == '__main__':
    main()
