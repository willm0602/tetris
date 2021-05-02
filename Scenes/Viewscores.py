
from .pygametools import drawButton, getCenterBtnCoords, write
from constants import COLORS
import pygame
import Scores

goHomeButtonSize = (300, 50)
GO_HOME_BUTTON_COORDS = getCenterBtnCoords(goHomeButtonSize, 50)

class ViewScore:
    def __init__(self, scene):
        self.scene = scene
        self.win = scene.win
        
    def tick(self):
        pass
        
    def pygameEvent(self, event):
        if event.type == pygame.QUIT:
            self.scene.mode = "EXIT"
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            x, y = mouse[0], mouse[1]
            upper = GO_HOME_BUTTON_COORDS[1]
            left = GO_HOME_BUTTON_COORDS[0]
            lower = GO_HOME_BUTTON_COORDS[1] + goHomeButtonSize[1]
            right = GO_HOME_BUTTON_COORDS[0] + goHomeButtonSize[0]
            if left < x < right and upper < y < lower:
                self.scene.mode = "LOBBY"
            
    def draw(self):
        self.win.fill(COLORS["BACKGROUND_COLOR"])
        drawButton(GO_HOME_BUTTON_COORDS, goHomeButtonSize, "Go home", self.win)
        
        scores = Scores.getScores()[:10]
        for index, score in enumerate(scores):
            write(300 + 50 * index, 50, f"{index + 1}){score[0]}, {score[1]}", "WHITE", self.win, x = 0)
        
        pygame.display.update()