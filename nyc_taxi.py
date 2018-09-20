

import pygame
import numpy as np
import pandas as pd
import random, sys
from time import sleep
from pygame.locals import *
from h3 import h3

## Hyper Parameter

FPS = 30
BLANK = None

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (200,200,200)

BRIGHTBLUE =    (  0,  50, 255)
DARKTURQUOISE = (  3,  54,  73)
WINDOWWIDTH = 1000   # 게임화면의 가로크기
WINDOWHEIGHT = 1000  # 게임화면의 세로크기
RECTSIZE = 100
RECT_LINE_WIDTH = 2

BASICFONTSIZE = 20
BGCOLOR = DARKTURQUOISE
TILECOLOR = GREEN
TEXTCOLOR = WHITE
BORDERCOLOR = BRIGHTBLUE
BUTTONCOLOR = WHITE
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = WHITE

TEXT_FONT = 'freesansbold.ttf'

left_border = -74.2589
bottom_border = 40.4774
right_border = -73.7004
top_border = 40.9176

# h3_address = h3.geo_to_h3(37.3615593, -122.0553238, 5) # lat, lng, hex resolution
# hex_center_coordinates = h3.h3_to_geo(h3_address) # array of [lat, lng]

center_lat = (top_border + bottom_border) / 2  ## Vertical
center_lon = (right_border + left_border) / 2  ## Horizon

lat_div =  WINDOWHEIGHT / (top_border - bottom_border)
lon_div =  WINDOWWIDTH / (right_border - left_border)


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, RESET_SURF, RESET_RECT, NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT

    pygame.init()
    pygame.font.init()

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Mobil NYC Gym')
    BASICFONT = pygame.font.Font(TEXT_FONT, BASICFONTSIZE)

 #   RESET_SURF, RESET_RECT = makeText('Reset', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 90)
 #   NEW_SURF, NEW_RECT = makeText('New Game', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 60)

    #SOLVE_SURF, SOLVE_RECT = makeText('Solve', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 30)

    ## Data Load

    df_0510 = pd.read_csv('./nyc_data/df_nyc_2016_05_10.csv').drop('Unnamed: 0', axis=1)
    df_0510['s_time'] = pd.to_datetime(df_0510['s_time'])
    df_0510['e_time'] = pd.to_datetime(df_0510['e_time'])
    df_0510 = df_0510.sort_values('s_time', axis=0)
    df_0510['s_mins'] = df_0510['s_time'].apply(apply_etamins)
    df_0510['e_mins'] = df_0510['e_time'].apply(apply_etamins)





    ## Image Load

    MAP_IMG = pygame.image.load('./image/nyc_map_1000.png').convert()
    MAP_IMG.set_alpha(50)

    ## Initiate Game Variable
 #   c_status = initStatus(3)


    total_frame = 0
    frame = 0

    ## Random Call Array
#    origin_call_list = makeOriginProb(500)

    while True:  # main game loop

        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(MAP_IMG, (0, 0))

        #display_dot(DISPLAYSURF, center_lon, center_lat)

        display_dot(DISPLAYSURF, 0, 0 )
        display_hexagon(DISPLAYSURF, center_lon, center_lat)
        #display_dot(DISPLAYSURF, 1000, 1000)
        #displayScore(DISPLAYSURF, c_status)
        displayTime(DISPLAYSURF, total_frame)
        #displayGrid(DISPLAYSURF, grid=5)

        if total_frame > 99999:
            total_frame = 0
        else:
            total_frame = total_frame + 1

        if total_frame % 20 == 0:
            if frame > 499 :
                frame = 0
            else:
         #       c_status = updateCarStatus(c_status, origin_call_list[frame])
                frame = frame + 1

        #if total_frame % 30 == 0 :
        #    c_status = updateCarPos(c_status)

        #displayCallRect(DISPLAYSURF, origin_call_list[frame])
        #displayCarImg(DISPLAYSURF, c_status)


        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

        sleep(2)
        FPSCLOCK.tick(FPS)


import datetime as DT

def displayTime(surf, fps):
    fontObj = pygame.font.Font(TEXT_FONT, 16)
    font_time = pygame.font.Font(TEXT_FONT, 14)
    ## Fixed Text

    tmp_time = str(int(fps))+'min'
    surf.blit(fontObj.render('Time : ', False, BLACK), (850, 10))
    surf.blit(font_time.render(tmp_time, False, BLUE), (890, 10))


def display_call(surf, x, y):
    return 0


def return_adj_coord(tmp):
    rtn_list = []

    for item in tmp:
        lat, lon = item
        lat_adj = 1000 - (lat - bottom_border) * lat_div
        lon_adj = (lon - left_border) * lon_div
        rtn_list.append([lat_adj, lon_adj])

    return rtn_list


def display_dot(surf, x, y):

    adj_x = x
    adj_y = y
    pygame.draw.circle(surf, RED, [adj_x, adj_y], 3)


def display_hexagon(surf, x, y):

    h3coord = h3.geo_to_h3(y, x, 8)
    bound_list = h3.h3_to_geo_boundary(h3coord)

    adj_bound_list = return_adj_coord(bound_list)

    pygame.draw.polygon(surf, RED, adj_bound_list, 2)


def apply_etamins(col):
    t2 = DT.datetime(2016, 5, 10)
    return (col - t2).total_seconds() // 60



if __name__ == '__main__':
    main()
