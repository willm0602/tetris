import pygame
from constants import COLORS, WIN_SIZE
from .Block import Block

SCORE_SIZE = 30


GAME_BOX_Y = int(WIN_SIZE[1] * 0.1)
GAME_BOX_HEIGHT = int(WIN_SIZE[1] * 0.85)

class Graphics():
    def __init__(self, scene, size):
        global GAME_BOX_SIZE, GAME_BOX_POS
        self.scene = scene
        self.win = scene.win
        width = size[0]
        height = size[1]
        
        boxSize = GAME_BOX_HEIGHT / height
        
        gameBoxWidth = width * boxSize
        GAME_BOX_SIZE = (gameBoxWidth, GAME_BOX_HEIGHT)
        self.gameBoxSize = GAME_BOX_SIZE
        
        gameBoxXPos = (WIN_SIZE[0] - gameBoxWidth) / 2
        GAME_BOX_POS = (gameBoxXPos, GAME_BOX_Y)
        self.gameBoxPos = GAME_BOX_POS
        
        self.boxSize = boxSize
        self.size = size
    
    def drawGame(self, currentBlock, occupiedTiles, score, held, queue):
        self.win.fill(COLORS["BACKGROUND_COLOR"])

        self.drawWindow()

        self.drawPiece(currentBlock)
        
        for tile in occupiedTiles:
            self.drawTile(tile)

        self.drawScore(score)
        
        if held:
            self.drawHeldTile(held)           
            
        self.drawQueue(queue)
        
        pygame.display.update()

    def drawWindow(self):
        x = GAME_BOX_POS[0]
        y = GAME_BOX_POS[1]
        width = GAME_BOX_SIZE[0]
        height = GAME_BOX_SIZE[1]
        pygame.draw.rect(self.win,COLORS["GAME_BACKGROUND"],(x, y, width, height))
    
    def drawScore(self, score):
        font = pygame.font.SysFont("Arial", SCORE_SIZE)    
        text = font.render(str(score), True, COLORS["TITLE_COLOR"])
        x = (WIN_SIZE[0] - text.get_width()) / 2
        y = SCORE_SIZE / 2
        self.win.blit(text, (x, y))

    def drawTile(self, tile):
        width = self.size[0]
        height = self.size[1]
        if any([tile.x < 0, tile.x > width, tile.y < -2, tile.y > height]):
            raise Exception(f"Error: Illegal box placement at {tile.x} {tile.y}")
        elif tile.y >= 0:
            
            OFFSET = 0.43
            
            xSize = ySize = self.boxSize + OFFSET

            x = GAME_BOX_POS[0] + tile.x * self.boxSize - (OFFSET / 2)

            y = GAME_BOX_POS[1] + tile.y * self.boxSize - (OFFSET / 2)
        
            pygame.draw.rect(self.win, tile.color, (x, y, xSize, ySize))
            
            highlighted_color = (int(tile.color[0] * 0.92), int(tile.color[1] * 0.7), int(tile.color[2] * 0.7))
            pygame.draw.rect(self.win, highlighted_color, (x + xSize / 4, y + ySize / 4, xSize/2, ySize/2))

    def drawPiece(self, piece:Block):
        for tile in piece.tiles:
            self.drawTile(tile)
            
    def drawMiniBlock(self, piece, x, y, size):
        miniBlock = Block(piece.code, (0,0))
        OVERLAP = 0
        size = size + OVERLAP
        for tile in miniBlock.tiles:
            tileX = x + size * tile.x 
            tileY = y + size * tile.y
            pygame.draw.rect(self.win, miniBlock.color, (tileX, tileY, size, size))
            
    def drawHeldTile(self, held):
        left_margin = self.gameBoxPos[0]
        newBlockSize = left_margin / (held.width + 2)
        HELD_Y = WIN_SIZE[1] / 5
        self.drawMiniBlock(held, newBlockSize, HELD_Y, newBlockSize)
        
    def drawQueue(self, queue):
        QUEUE_HEIGHT = WIN_SIZE[1] / 5
        currentHeight = 0
        for block in queue:
            left_margin = self.gameBoxPos[0] + self.gameBoxSize[0]
            newBlockSize = self.gameBoxPos[0] / (block.width + 2)
            blockY = currentHeight * newBlockSize + QUEUE_HEIGHT
            currentHeight = currentHeight + 3 + block.height
            self.drawMiniBlock(block, left_margin + newBlockSize, blockY, newBlockSize)