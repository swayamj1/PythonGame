try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
from vector import Vector
import math

class asteroidboss:
    IMG = simplegui.load_image("https://www.cs.rhul.ac.uk/home/zmac256/cs1822/bossasteroid.png")

    def __init__(self):
        self.health = 50
        self.width = self.IMG.get_width()
        self.height = self.IMG.get_height()
        self.pos = Vector(420, 30)
        self.scalar = 2
    
    def getPosX(self):
        return self.pos.x
    def getPosY(self):
        return self.pos.y
    
    def getWidth(self):
        return self.width
    def getHeight(self):
        return self.height
    
    def getHealth(self):
        return self.health
    def getScalar(self):
        return self.scalar
    
    
    def reduceScalar(self):
        self.scalar -= 0.01
        self.health -= 1
    
    def draw(self, canvas):
        canvas.draw_image(self.IMG, (self.IMG.get_width() / 2, self.IMG.get_height() / 2), (self.IMG.get_width(), self.IMG.get_height()), (self.pos.x, self.pos.y), (self.width * self.scalar, self.height * self.scalar), (math.pi / 4) * -1)