

import pygame
import numpy as np
import random, sys
from time import sleep
from pygame.locals import *

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
WINDOWWIDTH = 800   # 게임화면의 가로크기
WINDOWHEIGHT = 800  # 게임화면의 세로크기
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



## Game Parameter
GRID_SIZE = 5

## Array origin call prob
LOW_PROB = 0.08
HIGH_PROB = 0.25
origin_prob = [LOW_PROB, LOW_PROB, LOW_PROB, LOW_PROB, LOW_PROB,
               LOW_PROB, HIGH_PROB, HIGH_PROB, HIGH_PROB, LOW_PROB,
               LOW_PROB, HIGH_PROB, HIGH_PROB, HIGH_PROB, LOW_PROB,
               LOW_PROB, HIGH_PROB, HIGH_PROB, HIGH_PROB, LOW_PROB,
               LOW_PROB, LOW_PROB, LOW_PROB, LOW_PROB, LOW_PROB]

D_LOW_PB = 0.02
D_HIGH_PB = 0.07

destin_prob = [D_LOW_PB, D_LOW_PB, D_LOW_PB, D_LOW_PB, D_LOW_PB,
               D_LOW_PB, D_LOW_PB, D_HIGH_PB, D_LOW_PB, D_LOW_PB,
               D_LOW_PB, D_HIGH_PB, D_HIGH_PB, D_HIGH_PB, D_LOW_PB,
               D_LOW_PB, D_HIGH_PB, D_HIGH_PB, D_HIGH_PB, D_LOW_PB,
               D_LOW_PB, D_HIGH_PB, D_HIGH_PB, D_HIGH_PB, D_LOW_PB]

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, RESET_SURF, RESET_RECT, NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT

    pygame.init()
    pygame.font.init()

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Mobil Gym')
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

 #   RESET_SURF, RESET_RECT = makeText('Reset', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 90)
 #   NEW_SURF, NEW_RECT = makeText('New Game', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 60)

    SOLVE_SURF, SOLVE_RECT = makeText('Solve', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 30)

    ## Image Load
    #CAR_IMG = pygame.image.load('./image/car-small.png')
    CAR_A_IMG = pygame.image.load('./image/car-small_a.png')
    CAR_B_IMG = pygame.image.load('./image/car-small_b.png')
    CAR_C_IMG = pygame.image.load('./image/car-small_c.png')
    MAP_IMG = pygame.image.load('./image/seoul_city_map.png').convert()
    MAP_IMG.set_alpha(50)


    ## Initiate Game Variable
    c_status = initStatus(3)

    #    pygame.draw.rect(DISPLAYSURF, RED, (200, 150, 100, 50))
#    pixObj = pygame.PixelArray(DISPLAYSURF)
#    pixObj[480][380] = BLACK
#    del pixObj


    ## Random Call Array

    init_x = WINDOWWIDTH/2
    init_y = WINDOWHEIGHT/2
#    car_x=init_x
#    car_y=init_y

    tmp = 0

    total_frame = 0
    frame = 0

    origin_call_list = makeOriginProb(500)

    while True:  # main game loop

        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(MAP_IMG, (0, 0))
        displayScore(DISPLAYSURF, c_status)
        displayGrid(DISPLAYSURF, grid=5)

        if total_frame > 499:
            total_frame = 0
        else:
            total_frame = total_frame + 1

        if total_frame % 20 == 0:
            if frame > 499 :
                frame = 0
            else:
                frame = frame + 1
                c_status = updateStatus(c_status, origin_call_list[frame])

        displayCallRect(DISPLAYSURF, origin_call_list[frame])



        #displayArrow(DISPLAYSURF, 200, 200)

        if tmp > 99:
            tmp =0
        else :
            tmp = tmp +1

        car_x = init_x-30# + tmp
        car_y = init_y-30# + tmp

        DISPLAYSURF.blit(CAR_A_IMG, (car_x, car_y))
        DISPLAYSURF.blit(CAR_B_IMG, (car_x-200, car_y-200))
        DISPLAYSURF.blit(CAR_C_IMG, (car_x+200, car_y+200))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def displayScore(surf, c_status):

    taxi_name = ['A', 'B', 'C', 'D', 'E','F']

    fontObj = pygame.font.Font('freesansbold.ttf', 16)
    font_stats = pygame.font.Font('freesansbold.ttf', 14)
    ## Fixed Text
    text_trip = fontObj.render('Trip', False, BLACK)
    text_dist = fontObj.render('Dist', False, BLACK)
    text_inco = fontObj.render('Income', False, BLACK)

    surf.blit(fontObj.render('Taxi', False, BLACK), (10, 10))
    surf.blit(text_trip, (80, 10))
    surf.blit(text_dist, (130, 10))
    surf.blit(text_inco, (180, 10))

    num_car = len(c_status)

    for i in range(num_car):
        tmp_name = c_status[i]['name']
        tmp_trip = str(c_status[i]['trip'])
        tmp_dist = str(c_status[i]['dist'])
        tmp_income = str(c_status[i]['income'])

        surf.blit(font_stats.render(tmp_name, False, BLACK), (10, 28+i*20))
        surf.blit(font_stats.render(tmp_trip, False, BLUE), (80, 28+i*20))
        surf.blit(font_stats.render(tmp_dist, False, BLUE), (130, 28+i*20))
        surf.blit(font_stats.render(tmp_income, False, BLUE), (180, 28+i*20))


def initStatus(num_car):

    taxi_name = ['A', 'B', 'C', 'D', 'E', 'F']

    rtn_status = []

    for i in range(num_car):
        tmp_dic = {}
        tmp_dic['name'] = taxi_name[i]
        tmp_dic['crt_pos'] = i*12
        tmp_dic['trip'] = 0
        tmp_dic['dist'] = 0.0
        tmp_dic['income'] = 0

        rtn_status.append(tmp_dic)

    rtn_status[0]['crt_pos'] = 12
    rtn_status[1]['crt_pos'] = 0
    rtn_status[2]['crt_pos'] = 24

    return rtn_status

def updateStatus(c_status, tmp_list):

    for i in range(len(c_status)):

        tmp_car_pos = c_status[i]['crt_pos']
        ori_pos = tmp_car_pos
        des_pos = tmp_list[ori_pos]
        call_dist = int(np.abs(des_pos-ori_pos) / GRID_SIZE + np.abs(des_pos-ori_pos) % GRID_SIZE)

        call_money = int(30+(call_dist-1)*14)

        if des_pos > 0:
            ## car-pos & call origin matched
            c_status[i]['trip'] = c_status[i]['trip']+1
            c_status[i]['dist'] = c_status[i]['dist'] + call_dist
            c_status[i]['income'] = c_status[i]['income'] + call_money

    return c_status


def displayGrid(surf, grid = 5):
#    surf.fill(WHITE)
    start_x = WINDOWWIDTH/2 - (grid/2)*RECTSIZE
    start_y = WINDOWHEIGHT/2 - (grid/2)*RECTSIZE

    for i in range(grid):
        for j in range(grid):
            rect_x = start_x+i*(RECTSIZE-RECT_LINE_WIDTH/2)
            rect_y = start_y+j*(RECTSIZE-RECT_LINE_WIDTH/2)
            pygame.draw.rect(surf, GREY, (rect_x , rect_y , RECTSIZE, RECTSIZE), RECT_LINE_WIDTH)
            displayText(surf, str(( i+1)+5*j ), rect_x+50, rect_y+50 )


def displayText(surf, text, center_x, center_y, t_color=GREY):
    fontObj = pygame.font.Font('freesansbold.ttf', 40)
    textSurfaceObj = fontObj.render(text, True, t_color, WHITE)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (center_x, center_y)
    surf.blit(textSurfaceObj, textRectObj)

def displayArrow(surf, end_x, end_y):

    pygame.draw.line(surf, RED, (end_x-12, end_y), (end_x, end_y), 3)
    pygame.draw.line(surf, RED, (end_x-4, end_y-4), (end_x, end_y), 3)
    pygame.draw.line(surf, RED, (end_x-4, end_y+4), (end_x, end_y), 3)


def displayCallRect(surf, tmp_list, grid=5):

    start_x = WINDOWWIDTH/2 - (grid/2)*RECTSIZE
    start_y = WINDOWHEIGHT/2 - (grid/2)*RECTSIZE

    for i in range(grid):
        for j in range(grid):
            rect_x = start_x+i*(RECTSIZE-RECT_LINE_WIDTH/2)
            rect_y = start_y+j*(RECTSIZE-RECT_LINE_WIDTH/2)
            ## If destination is defined
            if tmp_list[i+5*j] > 0:
                pygame.draw.rect(surf, RED, (rect_x , rect_y , RECTSIZE, RECTSIZE), RECT_LINE_WIDTH)
                displayText(surf, str(tmp_list[i+5*j]), rect_x + 50, rect_y + 50, t_color=RED)
                displayArrow(surf, rect_x + 28, rect_y + 50)


def makeOriginProb(max_seq, RANDOM_SEED=42):

    rtn_array = []

    for i in range(max_seq):
        tmp_call = []
        for tmp_prob in origin_prob:
            tmp = np.random.binomial(1, tmp_prob, size=1)
            ## if taxi is called
            if tmp > 0 :
                ## get destination from the prob
                tmp = np.random.choice(np.arange(0, len(destin_prob)), p=destin_prob)

            tmp_call.append(tmp)

        rtn_array.append(tmp_call)

    return rtn_array

def makeText(text, color, bgcolor, top, left):
    # create the Surface and Rect objects for some text.
    textSurf = BASICFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)




if __name__ == '__main__':
    main()



