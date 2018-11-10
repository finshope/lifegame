#!/usr/bin/env python3



import random
import time
import sys

import pygame
from pygame.locals import *

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
    maps = generate_random_map(HEIGHT, WIDTH);
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
                    maps = generate_random_map(HEIGHT, WIDTH)

            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        SURF.fill(BG_COLOR)

        count += 1

        #draw grid
        for i in range(1,WIDTH):
            pygame.draw.line(SURF, GRID_COLOR,(i*CELL_SIZE[0],0),(i*CELL_SIZE[0],SCREEN_SIZE[1]))
        for i in range(1,HEIGHT):
            pygame.draw.line(SURF, GRID_COLOR,(0,i*CELL_SIZE[1]),(SCREEN_SIZE[0],i*CELL_SIZE[1]))
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
    """generate a (HEIGHT + 2, WIDTH + 2) size map randomly,
fill each side with False"""

    maps=[[False] * (WIDTH+2)]
    for row in range(HEIGHT):
        row_map = []
        n_cell = random.randint(0, WIDTH)
        row_map.extend([True] * n_cell)
        row_map.extend([False] * (WIDTH-n_cell))
        random.shuffle(row_map)
        row_map.insert(0,False)
        row_map.append(False)
        assert len(row_map) == (WIDTH + 2)
        maps.append(row_map)
    maps.append([False] * (WIDTH+2))
    return maps

def show_map(maps):
    cell_surf = pygame.Surface(CELL_SIZE)
    for w in range(WIDTH):
        for h in range(HEIGHT):
            try:
                if maps[h+1][w+1]:
                    cell_surf.fill(colors.random_color())
                    SURF.blit(cell_surf, ((w+1) * CELL_SIZE[0], (h+1) * CELL_SIZE[1]))
            except:
                print(w, h)

def update(maps):
    """calculate status of ever cell in next generation"""

    newmaps = [[False] * (WIDTH + 2)]
    print('lens of maps = ',len(maps))
    for y in range(1, HEIGHT+1):
        row_map = [False]
        for x in range(1, WIDTH+1):
            count = 0
            try:
                count = sum(maps[i][j] for i in (y-1, y, y+1) for j in (x-1, x, x+1) if(i!=y or j!=x))
            except:
                pass
            if count==3:
                row_map.append(True)
            elif count==2:
                row_map.append(maps[y][x])
            else:
                row_map.append(False)
        row_map.append(False)
        assert len(row_map) == (WIDTH+2)
        newmaps.append(row_map)
    newmaps.append([False] * (WIDTH + 2))
    return newmaps


if __name__ == '__main__':
    main()
