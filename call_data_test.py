import pygame
import numpy as np
import pandas as pd
import random, sys
from time import sleep
from pygame.locals import *
from h3 import h3
import datetime as DT

from taxi import *

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


left_top = (top_border, left_border)
right_top = (top_border, right_border)
left_bottom = (bottom_border, left_border)
right_bottom = (bottom_border, right_border)

print ('Left-right (Top) : %0.2f'%distance(left_top, right_top))
print ('Left-right (Bot) : %0.2f'%distance(left_bottom, right_bottom))
print ('Top-Bottom (Lef) : %0.2f'%distance(left_top, left_bottom))
print ('Top-Bottom (Rig) : %0.2f'%distance(right_top, right_bottom))





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

    df_hour_prob = pd.read_csv('./nyc_data/hours_prob.csv')


    df_st_prob = pd.read_csv('./nyc_data/df_st_nyc_05_mean_ptm.csv')
    new_col = df_st_prob.columns.values
    new_col[0] = 's_loc'
    df_st_prob.columns = new_col


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

        ## check the call data ( Current Time Frame Call )
        df_call = df_0510[(df_0510['s_mins'] == total_frame)][
            ['h_dist', 's_cen_lat', 's_cen_lon', 'e_cen_lat', 'e_cen_lon', 's_mins', 'e_mins', 'eta_mins',
             'fare_amount', 's_loc', 'e_loc']].reset_index(drop=True)


        ## Check Current taxi status
        ## Ver 10-06
        #taxi_a.update_taxistatus(total_frame)

        #if taxi_a.call_status == False:
        #    taxi_a.check_taxigetcall(df_call)
        #    crt_taxi_pass = taxi_a.img_off
        #else:
        #    crt_taxi_pass = taxi_a.img_on

        ## Ver 10-07

        displayTime(DISPLAYSURF, total_frame)

        h3_list = get_nyc_h3coord()

        for item in h3_list :
            display_hexagon_h3(DISPLAYSURF, item, l_color=BLUE)


        # display_call(DISPLAYSURF, df_call)



        if total_frame > 1439:
            total_frame = 0
        else:
            total_frame = total_frame + 1

        if total_frame % 20 == 0:
            if frame > 499 :
                frame = 0
            else:
         #       c_status = updateCarStatus(c_status, origin_call_list[frame])
                frame = frame + 1

        ##################################################
        ## Test Display
        # display_test(DISPLAYSURF)

        ##################################################

        #if total_frame % 30 == 0 :
        #    c_status = updateCarPos(c_status)

        #displayCallRect(DISPLAYSURF, origin_call_list[frame])
        #displayCarImg(DISPLAYSURF, c_status)


        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

        sleep(1.5)
        FPSCLOCK.tick(FPS)

def call_generation(loc, s_prob, e_prob):



    return df_rtn_call



def displayTime(surf, fps):
    fontObj = pygame.font.Font(TEXT_FONT, 16)
    font_time = pygame.font.Font(TEXT_FONT, 14)
    ## Fixed Text

    tmp_time = str(int(fps))+'min'
    surf.blit(fontObj.render('Total mins : ', False, BLACK), (760, 10))
    surf.blit(font_time.render(tmp_time, False, BLUE), (890, 10))

    hours = fps // 60
    mins = fps % 60
    tmp_hours = str(hours)+":"+str(mins)
    surf.blit(fontObj.render('Time : ', False, BLACK), (760, 28))
    surf.blit(font_time.render(tmp_hours, False, BLUE), (890, 28))


def display_call(surf, df_call):

    num_call = len(df_call)

    call_loc_list = []

    for i in range(num_call):
        ## Append Start-Lat, Start-Lon
        call_loc_list.append([df_call.iloc[i, 1], df_call.iloc[i, 2]])

        display_hexagon(surf, df_call.iloc[i, 2], df_call.iloc[i, 1], l_color=RED)

    return 0

def display_hexagon_h3(surf, h3coord, l_color=RED):
    bound_list = h3.h3_to_geo_boundary(h3coord)

    adj_bound_list = return_adj_coord(bound_list)

    pygame.draw.polygon(surf, l_color, adj_bound_list, 2)


def display_hexagon(surf, x, y, l_color=RED):

    h3coord = h3.geo_to_h3(y, x, 8)
    bound_list = h3.h3_to_geo_boundary(h3coord)

    adj_bound_list = return_adj_coord(bound_list)

    pygame.draw.polygon(surf, l_color, adj_bound_list, 2)


def apply_etamins(col):
    t2 = DT.datetime(2016, 5, 10)
    return (col - t2).total_seconds() // 60


def get_nyc_h3coord():
    rtn_x_list, rtn_y_list = get_linspace(left_top, right_bottom, 100)

    h3_list = []

    for x_coord in rtn_x_list:
        for y_coord in rtn_y_list:
            h3_list.append(h3.geo_to_h3(y_coord, x_coord, 8))

    return set(h3_list)


if __name__ == '__main__':
    main()

