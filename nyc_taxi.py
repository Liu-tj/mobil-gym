

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

## Driver Property
## 0 - get long dist call
## 1 - get long eta - call
## 2 - get short dist - call
## 3 - get short eta - call

DRIVER_PROP = 0


class Taxi:
    def __init__(self, img_on, img_off ):
        self.img_on = img_on
        self.img_off = img_off
        self.call_status = False  ## True - Pass - on, False
        self.crt_pos = None  ## h3 index
        self.call_ori = None ## h3 index
        self.call_des = None ## h3 index
        self.call_stm = 0      ## Start Total mins
        self.call_etm = 0      ## Estimated Arrival Total mins
        self.call_remain_tm = 0 ##
        self.crt_call_dist = 0
        self.crt_call_eta = 0
        self.taxi_attribute = None ## Taxi property
        self.total_trip = 0
        self.total_dist = 0
        self.total_money = 0


    def check_taxiloc(self):
        if self.crt_pos == self.call_des :
            ## If arrived destination
            ## Update
            return True
        else:
            return False

    def update_taxistatus(self):
        ## if check_taxiloc() == True
        ## Update status

        return 0


    def check_taxigetcall(self, df_call, driver_prone):

        df_crt_pos = df_call[(df_call['s_loc']==self.crt_pos)]

        if len(df_crt_pos) > 0:
            ## There is a call in crt_pos
            if driver_prone == 0: ## get long dist call
                idx = df_crt_pos.index[df_crt_pos['h_dist'] == df_crt_pos['h_dist'].max()].tolist()
                df_tmp2 = df_crt_pos.iloc[idx, :][:1]

            if driver_prone == 1: ## get long eta - call
                idx = df_crt_pos.index[df_crt_pos['eta_mins'] == df_crt_pos['eta_mins'].max()].tolist()
                df_tmp2 = df_crt_pos.iloc[idx, :][:1]

            if driver_prone == 2: ## get short dist - call
                idx = df_crt_pos.index[df_crt_pos['h_dist'] == df_crt_pos['h_dist'].min()].tolist()
                df_tmp2 = df_crt_pos.iloc[idx, :][:1]

            if driver_prone == 3: ## get short eta - call
                idx = df_crt_pos.index[df_crt_pos['eta_mins'] == df_crt_pos['eta_mins'].min()].tolist()
                df_tmp2 = df_crt_pos.iloc[idx, :][:1]




        return 0


    def add(self, num):
        self.result += num
        return self.result


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

    IMG_CAR_OFF = pygame.image.load('./image/car-small-nyc.png')
    IMG_CAR_ON = pygame.image.load('./image/car-small-nyc.png')
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

        #display_dot(DISPLAYSURF, 0, 0 )
        #display_hexagon(DISPLAYSURF, center_lon, center_lat)
        #display_dot(DISPLAYSURF, 1000, 1000)
        #displayScore(DISPLAYSURF, c_status)
        displayTime(DISPLAYSURF, total_frame)
        #displayGrid(DISPLAYSURF, grid=5)


        ## check the call data ( Current Time Frame Call )
        df_call = df_0510[(df_0510['s_mins'] ==total_frame)][
            ['h_dist', 's_cen_lat', 's_cen_lon', 'e_cen_lat', 'e_cen_lon', 's_mins', 'e_mins','eta_mins', 'fare_amount','s_loc','e_loc']].reset_index(drop=True)

        display_call(DISPLAYSURF, df_call)
        display_taxi_img(DISPLAYSURF, IMG_CAR_OFF, 500, 500, car_on=False)


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


import datetime as DT

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

def display_taxi_img(surf, img, x, y, car_on = False):
    DISPLAYSURF.blit(img, (x, y))


def display_call(surf, df_call):

    num_call = len(df_call)

    call_loc_list = []

    for i in range(num_call):
        ## Append Start-Lat, Start-Lon
        call_loc_list.append([df_call.iloc[i, 1], df_call.iloc[i, 2]])

        display_hexagon(surf, df_call.iloc[i, 2], df_call.iloc[i, 1], l_color=RED)

    return 0

def display_test_call(surf, df_call):

    num_call = len(df_call)

    call_loc_list = []

    for i in range(num_call):
        ## Append Start-Lat, Start-Lon
        ## Lat - y, Lon - x
        call_loc_list.append([df_call.iloc[i, 1], df_call.iloc[i, 2]])

        display_dot(surf, df_call.iloc[i, 2], df_call.iloc[i, 1], l_color=RED)

    return 0



def return_adj_coord(tmp):
    rtn_list = []

    for item in tmp:
        lat, lon = item
        lat_adj = 1000 - (lat - bottom_border) * lat_div
        lon_adj = (lon - left_border) * lon_div
        rtn_list.append([lon_adj, lat_adj])

    return rtn_list


def display_dot(surf, x, y, l_color=RED):

    #adj_x = x
    #adj_y = y

    adj_coord = return_adj_coord([[y,x]])
    pygame.draw.circle(surf, l_color, adj_coord, 3)


def display_hexagon(surf, x, y, l_color=RED):

    h3coord = h3.geo_to_h3(y, x, 8)
    bound_list = h3.h3_to_geo_boundary(h3coord)

    adj_bound_list = return_adj_coord(bound_list)

    pygame.draw.polygon(surf, l_color, adj_bound_list, 2)


def apply_etamins(col):
    t2 = DT.datetime(2016, 5, 10)
    return (col - t2).total_seconds() // 60



if __name__ == '__main__':
    main()
