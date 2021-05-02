import json
import random
from .Tile import Tile
from constants import COLORS

def getVal(tile):
        return 4 * tile.y + tile.x

class Block:
    '''
    uses an int to bin conversion to determine where there are tiles
    for an explanation of how the conversion works, see model.txt
    '''
    def __init__(self, code, origin):  
        self.code = code
        color = self.code[0]
        self.color = COLORS[color]
        self.setOrigin(origin)
        self.width = max([len(row) for row in code[1:]])
        self.height = len(self.code) - 1
        
    def drop(self):
        newTiles = []
        for tile in self.tiles:
            tile.drop()
            newTiles.append(tile)
        self.tiles = newTiles

    def getCoords(self):
        coords = []
        for tile in self.tiles:
            coords.append((tile.x, tile.y))
        return(coords)
    
    def containsCoords(self,x,y):
        for tile in self.tiles:
            if tile.x == x and tile.y == y:
                return True
        return False

    def setOrigin(self, origin):
        originX = origin[0]
        originY = origin[1]
        self.tiles = []
        for rowIndex, row in enumerate(self.code[1:]):
            for colIndex, val in enumerate(row):
                if val == '#':
                    x = originX + colIndex
                    y = originY + rowIndex
                    tile = Tile(x, y, self.color)
                    self.tiles.append(tile)
        return(self)
                    
    def canMove(self,right,down,occupied, maxWidth, maxHeight):
        checkingSpots = []
        for tile in self.tiles:
            checkX = tile.x + right
            checkY = tile.y + down
            if checkX < 0 or checkX >= maxWidth:
                return False

            if not self.containsCoords(checkX, checkY):
                checkingSpots.append((checkX, checkY))
        
        for tile in occupied:
            for checking in checkingSpots:
                if checking[0] == tile.x and checking[1] == tile.y:
                    return(False)
        return(True)
    
    def move(self, x, y):
        for tile in self.tiles:
            tile.move(x,y)
    
    def sort(self):
        self.tiles.sort(key = getVal)
    
    def canRotate(self, occupied, maxX, maxY):
        self.sort()
        origin = self.tiles[1]
        possibleRotations = []
        for tile in self.tiles:
            rotatedX = origin.x - (tile.y - origin.y)
            rotatedY = origin.y + (tile.x - origin.x)
            if rotatedX < 0 or rotatedX >= maxX or rotatedY > maxY or rotatedY < -2:
                return False
            possibleRotations.append((rotatedX, rotatedY))
        for rotation in possibleRotations:
            for tile in occupied:
                if rotation[0] == tile.x and rotation[1] == tile.y:
                    return False 
        return True

    def canClockwiseRotate(self,occupied, maxX, maxY):
        origin = self.tiles[1]
        possibleRotations = []
        for tile in self.tiles:
            rotatedX = origin.x + (tile.y - origin.y)
            rotatedY = origin.y - (tile.x - origin.x)
            if rotatedX < 0 or rotatedX >= maxX or rotatedY > maxY or rotatedY < -1:
                return False
            possibleRotations.append((rotatedX, rotatedY))
        for rotation in possibleRotations:
            for tile in occupied:
                if rotation[0] == tile.x and rotation[1] == tile.y:
                    return False 
        return True
    
    def __str__(self):
        return('|'.join([tile.__str__() for tile in self.tiles]))
    
    def rotate(self):
        origin = self.tiles[1]
        for tile in self.tiles:
            tile.rotate(origin)
            
    def highlight(self):
        self.tiles = [tile.highlight() for tile in self.tiles]
        
    def dehighlight(self):
        self.tiles = [tile.dehighlight() for tile in self.tiles]
modelsFile = open("models.json")
models = json.load(modelsFile)

def genBlock(origin):
    model = random.choice(models)
    block = Block(model, origin)
    return(block)