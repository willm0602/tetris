
def getHighlightVal(val):
    val = val * 5 / 4
    val = min(int(val), 255)
    return(val)
    
class Tile:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.normal = color
        r, g, b = color
        self.highlighted = [getHighlightVal(val) for val in color]
        self.color = self.normal         

    def drop(self):
        self.y = self.y + 1

    def getCoords(self):
        return(self.x, self.y)

    def canDrop(self, otherTiles):
        for tile in otherTiles:
            if tile.x == self.x and self.y + 1 == tile.y:
                return False
        return True

        
    def move(self, x, y):
        self.x = self.x + x
        self.y = self.y + y

    def rotate(self, origin):
        rotatedX = origin.x - (self.y - origin.y)
        rotatedY = origin.y + (self.x - origin.x)
        self.x = rotatedX
        self.y = rotatedY
        
    def highlight(self):
        self.color = self.highlighted
        return(self)
        
    def dehighlight(self):
        self.color = self.normal
        return(self)
    
    def __str__(self):
        return f"{self.x}, {self.y}, {self.color}"
    