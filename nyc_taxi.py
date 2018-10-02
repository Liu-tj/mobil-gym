

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

TAXI_MOVE_PROB = [0.7, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05]

RANDOM_START_LOCATION = ["882a1072cbfffff",
                        "882a100d65fffff",
                        "882a100d61fffff",
                        "882a10721bfffff",
                        "882a100d67fffff",
                        "882a1072c9fffff",
                        "882a100d21fffff",
                        "882a1008b3fffff",
                        "882a10725bfffff",
                        "882a1072cdfffff",
                        "882a107251fffff",
                        "882a100d63fffff"]


class Taxi:
    def __init__(self, img_on, img_off, crt_pos):
        self.img_on = img_on
        self.img_off = img_off
        self.call_status = False  ## True - Pass - on, False
        self.out_cell_move = False
        self.crt_pos = crt_pos  ## h3 index
        self.crt_ori = None ## h3 index
        self.crt_des = None ## h3 index
        self.crt_move_stm = 0      ## Start Total mins
        self.crt_move_etm = 0      ## Estimated Arrival Total mins
        self.crt_move_remain_tm = 0 ##
        self.crt_move_dist = 0
        self.crt_move_eta = 0
        self.crt_call_money = 0
        self.taxi_attribute = None ## Taxi property
        self.total_wait_tm = 0       ## Call waiting Time
        self.crt_drive_tm_no_pass = 0  ## Taxi drive to other cell without Pass
        self.total_trip = 0
        self.total_dist = 0
        self.total_money = 0


    def check_taxiloc(self):
        if self.crt_pos == self.crt_des :
            ## If arrived destination
            ## Update
            return True
        else:
            return False

    def update_taxistatus(self, frame):
        ## Taxi Movement Status Update
        ## if check_taxiloc() == True
        ## Update status

        if self.crt_move_remain_tm > 0 :
            self.crt_move_remain_tm = self.crt_move_remain_tm-1
        else:
            self.out_cell_move = False
            self.crt_pos = self.crt_des

            if self.call_status == True :
                self.total_trip = self.total_trip + 1
                self.total_money = self.total_money + self.crt_call_money

            self.total_dist = self.total_dist + self.crt_move_dist
            self.call_status = False

            self.crt_ori = None  ## h3 index
            self.crt_des = None  ## h3 index
            self.crt_move_stm = 0  ## Start Total mins   ( Frame )
            self.crt_move_etm = 0  ## Estimated Arrival Total mins  ( Frame )
            self.crt_move_remain_tm = 0  ##
            self.crt_move_dist = 0
            self.crt_move_eta = 0
            self.crt_call_money = 0


        return 0


    def check_taxigetcall(self, df_call):

        ## Within 1 min - All call list
        df_crt_pos = df_call[(df_call['s_loc']==self.crt_pos)]

        ## Driver's call selection attribute
        ## For testing - it set to be randomly selected
        ##
        driver_prone = self.taxi_attribute

        if len(df_crt_pos) > 0:
            ## There is a call in crt_pos
            if driver_prone == 0: ## get long dist call
                #idx = df_crt_pos.index[df_crt_pos['h_dist'] == df_crt_pos['h_dist'].max()].tolist()
                df_tmp2 = df_crt_pos[(df_crt_pos['h_dist'] == df_crt_pos['h_dist'].max())]
                #df_tmp2 = df_crt_pos[idx[0]]#[:1]

            if driver_prone == 1: ## get long eta - call
                #idx = df_crt_pos.index[df_crt_pos['eta_mins'] == df_crt_pos['eta_mins'].max()].tolist()
                df_tmp2 = df_crt_pos[(df_crt_pos['eta_mins'] == df_crt_pos['eta_mins'].max())]
                #df_tmp2 = df_crt_pos.iloc[idx, :]#[:1]

            if driver_prone == 2: ## get short dist - call
                #idx = df_crt_pos.index[df_crt_pos['h_dist'] == df_crt_pos['h_dist'].min()].tolist()
                #df_tmp2 = df_crt_pos.iloc[idx, :]#[:1]
                df_tmp2 = df_crt_pos[(df_crt_pos['h_dist'] == df_crt_pos['h_dist'].min())]

            if driver_prone == 3: ## get short eta - call
                #idx = df_crt_pos.index[df_crt_pos['eta_mins'] == df_crt_pos['eta_mins'].min()].tolist()
                #df_tmp2 = df_crt_pos.iloc[idx, :]#[:1]
                df_tmp2 = df_crt_pos[(df_crt_pos['eta_mins'] == df_crt_pos['eta_mins'].min())]

            if driver_prone == 4: ## Waiting
                ## Decide not to take current Call
                ## After This call -> Choosing the Moving Action
                return False

            ## df_tmp2 - Col list
            ## 0- h_dist,
            ## 1- s_cen_lat
            ## 2- s_cen_lon
            ## 3- e_cen_lat
            ## 4- e_cen_lon
            ## 5- s_mins
            ## 6- e_mins
            ## 7- eta_mins
            ## 8- fare_amount
            ## 9- s_loc
            ##10- e_loc

            self.call_status = True
            self.crt_ori = df_tmp2.iloc[0, 9 ]
            self.crt_des = df_tmp2.iloc[0, 10]

            if self.crt_ori != self.crt_des :
                self.out_cell_move = True
            else:
                self.out_cell_move = False

            self.crt_move_stm = df_tmp2.iloc[0, 5]
            self.crt_move_etm = df_tmp2.iloc[0, 6]
            self.crt_move_remain_tm = df_tmp2.iloc[0, 7]
            self.crt_move_dist = df_tmp2.iloc[0, 0]
            self.crt_move_eta = df_tmp2.iloc[0, 7]
            self.crt_call_money = df_tmp2.iloc[0, 8]

            ## Get Call
            return True
        else :
            ## Not Get Call
            ## Waitting until some call is activated in cell
            return False


    def check_taximove(self, prob =TAXI_MOVE_PROB ):

        ## When check_taxigetcall return False ->
        ## Decide to wait ( in - cell ) or go out - cell

        ## Decision to wait : selected location = self.crt_pos
        ## Decision to go out - cell : selected location != self.crt_pos

        ## Pre-defined Prob TAXI_MOVE_PROB = [0.7, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05]

        nearby_coord_list = return_nearby_coord(self.crt_pos)

        select_loc = nearby_coord_list[np.random.choice(np.arange(0, len(nearby_coord_list)), p=prob)]


        if select_loc != self.crt_pos:

            tmp_eta = random.randint(4,6)
            self.out_cell_move = True
            self.crt_ori = self.crt_pos
            self.crt_des = select_loc
            self.crt_move_remain_tm = tmp_eta
            self.crt_move_dist = 1
            self.crt_move_eta = tmp_eta
        else:
            self.out_cell_move = False

        return 0



    def display_taxiimg(self):
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

    df_hour_prob = pd.read_csv('./nyc_data/hours_prob.csv')

    ## Image Load

    IMG_CAR_OFF = pygame.image.load('./image/car-small-nyc-off.png')
    IMG_CAR_ON = pygame.image.load('./image/car-small-nyc-on.png')

    ## Car Img Rescaled
    IMG_CAR_OFF = pygame.transform.scale(IMG_CAR_OFF, (8, 16))
    IMG_CAR_ON = pygame.transform.scale(IMG_CAR_ON, (8, 16))

    MAP_IMG = pygame.image.load('./image/nyc_map_1000.png').convert()
    MAP_IMG.set_alpha(50)

    ## Initiate Game Variable
 #   c_status = initStatus(3)

    ## Taxi class
    ## Initialized with On Img, Off Img, Initial Location (H3-coord)



    taxi_a = Taxi(IMG_CAR_ON, IMG_CAR_OFF,
                  RANDOM_START_LOCATION[random.randint(0, len(RANDOM_START_LOCATION))])
    taxi_a.taxi_attribute = DRIVER_PROP

    total_frame = 0
    frame = 0

    ## Random Call Array
#    origin_call_list = makeOriginProb(500)

    while True:  # main game loop

        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(MAP_IMG, (0, 0))

        displayTime(DISPLAYSURF, total_frame)
        #displayGrid(DISPLAYSURF, grid=5)

        ## check the call data ( Current Time Frame Call )
        df_call = df_0510[(df_0510['s_mins'] ==total_frame)][
            ['h_dist', 's_cen_lat', 's_cen_lon', 'e_cen_lat', 'e_cen_lon', 's_mins', 'e_mins','eta_mins', 'fare_amount','s_loc','e_loc']].reset_index(drop=True)

        display_call(DISPLAYSURF, df_call)
        display_score(DISPLAYSURF, taxi_a)
        display_crt_taxi_status(DISPLAYSURF, taxi_a)


        ## Check Current taxi status
        if taxi_a.call_status == True & taxi_a.out_cell_move == True :
            ## Getted Call and Moving Out - cell des
            crt_taxi_pass = taxi_a.img_on

        elif taxi_a.call_status == False & taxi_a.out_cell_move == False :
            ## Watting in - Cell loc
            crt_taxi_pass = taxi_a.img_off

        elif taxi_a.call_status == True & taxi_a.out_cell_move == False:
            ## Getted Call and Moving in - cell des
            crt_taxi_pass = taxi_a.img_on

        elif taxi_a.call_status == False & taxi_a.out_cell_move == True:
            ## Moving without pass out - cell loc
            crt_taxi_pass = taxi_a.img_off

        if taxi_a.call_status == True :
            taxi_a.update_taxistatus(total_frame)
        else:
            taxi_a.check_taxigetcall(df_call)

        display_taxi_img(DISPLAYSURF, crt_taxi_pass, taxi_a.crt_pos)

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


def display_score(surf, taxi_cls):
    fontObj = pygame.font.Font(TEXT_FONT, 16)
    font_score = pygame.font.Font(TEXT_FONT, 14)

    surf.blit(fontObj.render('Total calls : ', False, BLACK), (20, 10))
    surf.blit(fontObj.render('Total dists : ', False, BLACK), (20, 28))
    surf.blit(fontObj.render('Total incomes : ', False, BLACK), (20, 46))

    str_calls = str(taxi_cls.total_trip)
    str_dists = str('%.2f'%taxi_cls.total_dist)
    str_incomes = str(taxi_cls.total_money)

    surf.blit(font_score.render(str_calls, False, BLUE), (150, 10))
    surf.blit(font_score.render(str_dists, False, BLUE), (150, 28))
    surf.blit(font_score.render(str_incomes, False, BLUE), (150, 46))

    return 0

def display_crt_taxi_status(surf, taxi_cls):
    fontObj = pygame.font.Font(TEXT_FONT, 16)
    font_score = pygame.font.Font(TEXT_FONT, 14)


    surf.blit(fontObj.render('Call on : ', False, BLACK), (20, 70))
    surf.blit(fontObj.render('Des Pos(H3) : ', False, BLACK), (20, 88))
    surf.blit(fontObj.render('Remain Time : ', False, BLACK), (20, 106))
    surf.blit(fontObj.render('Taxi Status : ', False, BLACK), (20, 124))

    if taxi_cls.call_status == True:
        str_calls = 'True'

        bound_list = h3.h3_to_geo_boundary(taxi_cls.crt_des)
        adj_bound_list = return_adj_coord(bound_list)
        pygame.draw.polygon(surf, BRIGHTBLUE, adj_bound_list, 2)

        if taxi_cls.out_cell_move == True:
            str_taxi_status = 'Out-Call On'
        else :
            str_taxi_status = 'In-Call On'
    else :
        str_calls = 'False'

        if taxi_cls.out_cell_move == True:
            str_taxi_status = 'Out-Call off'
        else :
            str_taxi_status = 'In-Call off'

    str_des = str(taxi_cls.crt_des)
    str_time = str(taxi_cls.crt_move_remain_tm)

    surf.blit(font_score.render(str_calls, False, BLUE), (150, 70))
    surf.blit(font_score.render(str_des, False, BLUE), (150, 88))
    surf.blit(font_score.render(str_time, False, BLUE), (150, 106))
    surf.blit(font_score.render(str_taxi_status, False, BLUE), (150, 124))

    return 0


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

def display_taxi_img(surf, img, h3_coord, car_on = False):

    lat, lon = h3.h3_to_geo(h3_coord)  # array of [lat, lng]

    #rect = img.get_rect()

    rtn_adj_coord = return_adj_coord([[lat,lon]])

    rtn_adj_coord[0][0] = rtn_adj_coord[0][0] - 4
    rtn_adj_coord[0][1] = rtn_adj_coord[0][1] - 8

    surf.blit(img, rtn_adj_coord[0])


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

def return_nearby_coord(h3_address, dist=1):

    ## Get H3-coord then return nearby 6 coord + center - location

    tmp = h3.k_ring_distances(h3_address, dist)
    rtn_list = []

    for item in tmp:
        tmp2 = list(item)
        for item2 in tmp2:
            rtn_list.append(item2)

    return rtn_list


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
