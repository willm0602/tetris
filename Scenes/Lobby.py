import pygame
from pygame import draw
from constants import WIN_SIZE, COLORS
from .pygametools import drawButton, write

START_BTN_COORDS = (150, 400)
BTN_SIZE = (300, 50)
START_BTN_BORDER = 5

TITLE_SIZE = 120
TITLE_HEIGHT = TITLE_SIZE / 3

SCORE_SIZE = 30

btnFontSize = int(BTN_SIZE[1] * 2 / 3)

viewScoreBTNCOORDS = (START_BTN_COORDS[0], START_BTN_COORDS[1] + BTN_SIZE[1] * 2)

class Lobby():
    def __init__(self, scene):
        self.scene = scene
        self.win = scene.win
    
    def tick(self):
        pass
    
    def pygameEvent(self, event):
        if event.type == pygame.QUIT:
            self.scene.mode = "EXIT"

        #handles mouse clicks in lobby
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            #checks if clicked in button to start game
            x = mouse_pos[0]
            y = mouse_pos[1]
            left = START_BTN_COORDS[0]
            upper = START_BTN_COORDS[1] 
            right = left + BTN_SIZE[0]
            lower = upper + BTN_SIZE[1]

            if (left < x < right) and (upper < y < lower):
                self.scene.mode = "GAME"
            
            upper = viewScoreBTNCOORDS[1]
            lower = upper + BTN_SIZE[1]
            
            if left < x < right and upper < y < lower:
                self.scene.mode = "VIEW_SCORES"
            
    def draw(self):
        self.win.fill(COLORS["BACKGROUND_COLOR"])

        #handles title text
        write(TITLE_HEIGHT, fontsize= TITLE_SIZE, text = "TETRIS", color= COLORS["TITLE_COLOR"], win = self.win)
        
        drawButton(START_BTN_COORDS, BTN_SIZE, "START", self.win)

        drawButton(viewScoreBTNCOORDS, BTN_SIZE, "VIEW TOP SCORES", self.win)
        
        pygame.display.update()