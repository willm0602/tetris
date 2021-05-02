from .GameOver import SAVE_SCORE_COORDS
import pygame
from .pygametools import TextInput, drawButton
from constants import WIN_SIZE, COLORS
import Scores

INPUT_SIZE = (WIN_SIZE[0] * 2/3, WIN_SIZE[1] / 15)
INPUT_COORDS = ((WIN_SIZE[0] - INPUT_SIZE[0]) / 2, WIN_SIZE[1] / 15)
SUB_BUTTON_SIZE  = (WIN_SIZE[0] * 2/3, WIN_SIZE[1] / 15)
SUB_BUTTON_COORDS = (INPUT_COORDS[0], WIN_SIZE[1] / 5)
class SaveScore:
    def __init__(self, scene):
        self.textinput = TextInput(3)
        self.scene = scene
        
    def pygameEvent(self, event: pygame.event):
        if event.type == pygame.QUIT:
                self.scene.mode = "EXIT"
        if event.type == pygame.KEYDOWN:
            key = pygame.key.name(event.key)
            self.textinput.addChar(key)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            x, y = mouse_pos[0], mouse_pos[1]
            upper, lower, left, right = SUB_BUTTON_COORDS[1], SUB_BUTTON_COORDS[1] + SUB_BUTTON_SIZE[1], SUB_BUTTON_COORDS[0], SUB_BUTTON_COORDS[0] + SUB_BUTTON_SIZE[0]
            
            if left < x < right and upper < y < lower:
                self.record()
                
    def tick(self):
        pass
    
    def record(self):
        name = self.textinput.result
        score = self.scene.score
        Scores.addScore(name, score)
        self.scene.mode = "LOBBY"
    
    def draw(self):
        self.scene.win.fill(COLORS["BACKGROUND_COLOR"])
        self.textinput.draw(self.scene.win, INPUT_COORDS, INPUT_SIZE)
        drawButton(SUB_BUTTON_COORDS, SUB_BUTTON_SIZE, "SUBMIT", self.scene.win)
        pygame.display.update()