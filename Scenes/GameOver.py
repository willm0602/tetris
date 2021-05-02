import pygame
from constants import COLORS, WIN_SIZE
from .pygametools import write, drawButton

BTN_SIZE = (300, 50)
BTN_COLOR = (205, 215, 214)
BTN_X = (WIN_SIZE[0] - BTN_SIZE[0]) / 2

BTN_BORDER = 5
btnFontSize = 20

GAME_OVER_SIZE = 100
GAME_OVER_Y = 15
GAME_OVER_COLOR = COLORS["TITLE_COLOR"]

scoreHeight = GAME_OVER_Y + GAME_OVER_SIZE + int(.5 * GAME_OVER_SIZE)

RESTART_BTN_COORDS = (BTN_X, GAME_OVER_Y + 2 * GAME_OVER_SIZE + scoreHeight)

LOBBY_BTN_COORDS = (BTN_X, RESTART_BTN_COORDS[1] + GAME_OVER_SIZE)

SAVE_SCORE_COORDS = (BTN_X, LOBBY_BTN_COORDS[1] + GAME_OVER_SIZE)
    
class GameOver:
    def __init__(self, scene):
        self.scene = scene
        self.win = self.scene.win
        self.score = self.scene.score
        
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
            
            left = RESTART_BTN_COORDS[0]
            restartUpper = RESTART_BTN_COORDS[1] 
            right = left + BTN_SIZE[0]
            restartLower = restartUpper + BTN_SIZE[1]

            if (left < x < right) and (restartUpper < y < restartLower):
                self.scene.mode = "GAME"
                
            lobbyUpper = LOBBY_BTN_COORDS[1]
            lobbyLower = lobbyUpper + BTN_SIZE[1]
            
            if (left < x < right) and (lobbyUpper < y < lobbyLower):
                self.scene.mode = "LOBBY"

            saveScoreUpper = SAVE_SCORE_COORDS[1]
            saveScoreLower = saveScoreUpper + BTN_SIZE[1]
            
            if left < x < right and saveScoreUpper < y < saveScoreLower:
                self.scene.mode = "SAVE_SCORE"
            
            
    def draw(self):
        self.win.fill(COLORS["BACKGROUND_COLOR"])

        #handles title text
        write(GAME_OVER_Y, GAME_OVER_SIZE, "GAME OVER", COLORS["TITLE_COLOR"], self.win)
        
        #handles showing score
        
        write(scoreHeight, int(GAME_OVER_SIZE*2/3), str(self.score), 
                COLORS["TITLE_COLOR"], self.win
            )
        
        
        #draws the button to play again
        
        drawButton(RESTART_BTN_COORDS,BTN_SIZE, "PLAY AGAIN", self.win)

        drawButton(LOBBY_BTN_COORDS, BTN_SIZE, "LOBBY", self.win)

        drawButton(SAVE_SCORE_COORDS, BTN_SIZE, "SAVE SCORE", self.win)
        #draws the button to go to the lobby

        pygame.display.update()