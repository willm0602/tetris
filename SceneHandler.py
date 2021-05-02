'''
Controls which scene the user sees
'''
import pygame
import sys

from constants import WIN_SIZE
from Scenes.Game import Game
from Scenes.GameOver import GameOver
from Scenes.savescore import SaveScore
from Scenes.Viewscores import ViewScore as ViewScore
from Scenes.Lobby import Lobby

class SceneHandler:
    def __init__(self, mode = "LOBBY", windowSize = WIN_SIZE):
        self.mode = mode
        pygame.init()
        self.win = pygame.display.set_mode(windowSize)
        pygame.display.set_caption("Tetris")

        self.scenes = {
            "LOSE": GameOver,
            "GAME": Game,
            "LOBBY": Lobby,
            "EXIT": sys.exit,
            "SAVE_SCORE": SaveScore,
            "VIEW_SCORES": ViewScore
        }
    
    def run(self):
        lastMode = None
        self.currentScene = None
        while self.mode != "EXIT":
            if self.mode != lastMode:
                self.currentScene = self.scenes[self.mode](self)
                lastMode = self.mode
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.mode = "EXIT"
                self.currentScene.pygameEvent(event)
            if self.currentScene.tick:
                self.currentScene.tick()
            self.currentScene.draw()
            pygame.time.delay(1)
