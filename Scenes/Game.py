import pygame
from .GameTools.Block import Block, genBlock
from .GameTools.GameGraphics import Graphics
from constants import *

SCORE_SIZE = 60
GAME_SIZE = (10, 14)
WIDTH = GAME_SIZE[0]
HEIGHT = GAME_SIZE[1]

class Game:
    def __init__(self, scene, width = WIDTH, height = HEIGHT, queueSize = 3):
        self.score = 0
        self.graphics = Graphics(scene,(width, height))
        self.scene = scene

        self.blockQueue = []
        self.blockOrigin = (int(width / 2) - 2,-2)
        for i in range(queueSize):
            block = genBlock(self.blockOrigin)
            self.blockQueue.append(block)

        self.currentBlock = genBlock(self.blockOrigin) 
        self.occupiedTiles = []
        self.tickCount = 0
        self.heldBlock = None
        self.usedHold = False
        
        self.size = (width, height)
        self.placeBlocks = 0
        pygame.mixer.init()
        pygame.mixer.music.load("Scenes\GameTools\game.wav")
        pygame.mixer.music.play(-1)

    #uses graphics library to draw game status
    def draw(self):
        self.graphics.drawGame(self.currentBlock,self.occupiedTiles,self.score, self.heldBlock, self.blockQueue)
    
    #gets all coordinates for tiles in game
    def getOccupiedSpots(self):
        spots = []
        for tile in self.occupiedTiles:
            area = (tile.x, tile.y)
            spots.append(area)
        return(spots)

    #returns how many ticks there should be before tetris block moves again
    def getSpeed(self):
        #I put in roughly the speeds I wanted into a quadratic regression calculator to calculate how fast the blocks should move
        x = self.placeBlocks + self.score / 100
        if x < 320: #threshold, after this it doesn't get any faster
            return int(.0006 * x**2 - 5.3 * x + 664)
        return(50)

    #determines if the current block is able to drop
    def canDrop(self):
        for tile in self.currentBlock.tiles:
            if not tile.canDrop(self.occupiedTiles) or tile.y + 1 >= self.size[1]:            
                return False
        return(True)

    #moves the current block to the hold state and switches it out with the previously held block if there is one
    def hold(self):
        if not self.usedHold:
            self.usedHold = True
            if self.heldBlock:
                self.currentBlock, self.heldBlock = self.heldBlock, self.currentBlock
                self.currentBlock.setOrigin(self.blockOrigin)
            else:
                self.heldBlock = self.currentBlock
                self.getBlock()               
    
    #handles pygame events (keyboard presses, etc.)
    def pygameEvent(self, event):
        if event.type == pygame.QUIT:
            self.scene.mode = "EXIT"
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_a):
                if self.currentBlock.canMove(-1,0,self.occupiedTiles,self.size[0],self.size[1]):
                    self.currentBlock.move(-1, 0)
            if event.key in (pygame.K_DOWN, pygame.K_s):
                if self.canDrop():
                    self.currentBlock.move(0,1)
            if event.key in (pygame.K_RIGHT, pygame.K_d):
                if self.currentBlock.canMove(1,0,self.occupiedTiles,self.size[0],self.size[1]):
                    self.currentBlock.move(1,0)
            if event.key in (pygame.K_UP, pygame.K_w):
                if self.currentBlock.canRotate(self.occupiedTiles,self.size[0], self.size[1]):
                    self.currentBlock.rotate()
                elif self.currentBlock.canClockwiseRotate(self.occupiedTiles, self.size[0], self.size[1]):
                    for i in range(3):
                        self.currentBlock.rotate()
            if event.key == pygame.K_SPACE:
                while self.canDrop():
                    self.currentBlock.drop()
                    self.draw()
                    pygame.time.delay(10)
                self.placeBlock()
            if event.key == pygame.K_h:
                self.hold()
        self.draw()

    #drops whenever it can at a set interval
    def tick(self):
        if self.tickCount >= self.getSpeed():
            if self.canDrop():
                self.currentBlock.drop()
            else:
                self.placeBlock()
            self.draw()
            self.tickCount = 0
        self.tickCount = self.tickCount + 1

    #removes the first block from the queue and adds a new block to the end
    def getBlock(self):
        self.usedHold = False
        self.currentBlock = self.blockQueue[0]
        self.blockQueue = self.blockQueue[1:]
        self.blockQueue.append(genBlock(self.blockOrigin))
    
    #determines if a row is full
    def fullRow(self, row):
        for col in range(self.size[0]):
            if not (col, row) in self.getOccupiedSpots():
                return(False)
        return(True)

    #highlights a row of blocks
    def highlightRow(self, row):
        for tile in self.occupiedTiles:
            if tile.y == row:
                tile.highlight()
        self.draw()
        pygame.time.delay(250)

    #removes a row of tiles
    def delRow(self, rowNumber):
        rowTiles = list([tile for tile in self.occupiedTiles if tile.y == rowNumber])
        while(len(rowTiles) > 0):
            delTile = rowTiles.pop(0)
            self.occupiedTiles.remove(delTile)
        for tile in self.occupiedTiles:
            if tile.y < rowNumber:
                tile.drop()

    #places a block when it can no longer move
    def placeBlock(self):
        self.currentBlock.highlight()
        self.draw()
        pygame.time.delay(100)
        self.currentBlock.dehighlight()
        self.placeBlocks = self.placeBlocks + 1
        for tile in self.currentBlock.tiles:
            if tile.y < 0:
                self.scene.mode = "LOSE"
                self.scene.score = self.score
                
            self.occupiedTiles.append(tile)
        self.getBlock()
        
        rowsToCheck = [tile.y for tile in self.currentBlock.tiles]
        clearedRows = []
        if rowsToCheck:
            rowCount = 0
            for row in range(self.size[1]):
                if self.fullRow(row):
                    clearedRows.append(row)
            if rowCount == 4:
                self.score = self.score + 600
        for row in clearedRows:
            self.highlightRow(row)
            self.delRow(row)
            rowCount = rowCount + 1
            self.score = self.score + 100