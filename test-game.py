

import pygame
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

## Image Load
CAR_IMG = pygame.image.load('./image/car-small.png')



## Game Parameter
GRID_SIZE = 5

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, RESET_SURF, RESET_RECT, NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Mobil Gym')
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

 #   RESET_SURF, RESET_RECT = makeText('Reset', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 90)
 #   NEW_SURF, NEW_RECT = makeText('New Game', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 60)

    SOLVE_SURF, SOLVE_RECT = makeText('Solve', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 30)


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

    while True:  # main game loop

        DISPLAYSURF.fill(WHITE)

        displayGrid(DISPLAYSURF, grid=5)

        if tmp > 99:
            tmp =0
        else :
            tmp = tmp +1

        car_x = init_x + tmp
        car_y = init_y + tmp

        DISPLAYSURF.blit(CAR_IMG, (car_x, car_y))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        FPSCLOCK.tick(FPS)

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


def displayText(surf, text, center_x, center_y):
    fontObj = pygame.font.Font('freesansbold.ttf', 40)
    textSurfaceObj = fontObj.render(text, True, GREY, WHITE)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (center_x, center_y)
    surf.blit(textSurfaceObj, textRectObj)

def makeText(text, color, bgcolor, top, left):
    # create the Surface and Rect objects for some text.
    textSurf = BASICFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)




if __name__ == '__main__':
    main()



