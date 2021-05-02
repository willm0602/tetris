import pygame
from constants import COLORS, FONT, WIN_SIZE

def write(y, fontsize, text, color, win, x = None):
    font = pygame.font.SysFont(FONT, fontsize)
    textLabel = font.render(text, True, color)
    if not x:
        x = (WIN_SIZE[0] - (textLabel.get_width())) / 2
    win.blit(textLabel, (x, y))
    
def drawButton(coords, size, text, win, textColor = "BLACK", fillColor = "BTN_COLOR", borderColor = None, borderSize = 0):
    x, y = coords[0], coords[1]
    width, height = size[0], size[1]
    if borderColor:
        pygame.draw.rect(win, borderColor, (x, y, width, height))
        x += borderSize
        y += borderSize
        width = width - 2 * borderSize
        height = height - 2 * borderSize
    textColor = COLORS[textColor]
    fillColor = COLORS[fillColor]
    pygame.draw.rect(win, fillColor, (x, y, width, height))
    font = pygame.font.SysFont(FONT, int(2 * height / 3))
    btnLabel = font.render(text, True, textColor)
    x = x + (width -  btnLabel.get_width()) / 2
    y = y + (height - btnLabel.get_height()) / 2
    win.blit(btnLabel, (x, y))
    
    
class TextInput():
    def __init__(self, maxsize) -> None:
        self.result = ""
        self.maxSize = maxsize
    
    def addChar(self, c):
        if c == 'backspace':
            if len(self.result):
                self.result = self.result[:-1]
        elif len(self.result) < self.maxSize and c.isalpha():
            self.result = self.result + c.upper()
            
    def draw(self, win, coords, size):
        drawButton(coords, size, '  '.join(self.result), win, "WHITE", "BLACK")
        
def getCenterBtnCoords(size, y):
    totalGap = WIN_SIZE[0] - size[0]
    totalGap = totalGap / 2
    totalGap = int(totalGap)
    coords   = (totalGap, y)
    return(coords)