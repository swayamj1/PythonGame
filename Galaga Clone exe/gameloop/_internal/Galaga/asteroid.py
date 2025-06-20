try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

import random

from spritesheet import SpriteSheet

IMG = simplegui.load_image("https://www.cs.rhul.ac.uk/home/zmac256/cs1822/meteor-spritesheet.png")
SCALAR = 0.95

class Clock:
    def __init__(self):
        self.time = 0

    def tick(self):
        current_time = self.time
        self.time += 1
        return current_time
    
    def transition(self, frame_duration):
        return self.time % frame_duration == 0
    

CLOCK = Clock()

class Asteroid:
    def __init__(self, pos, screen_height):
        self.pos = pos
        self.speed = random.randint(2, 5)
        self.spritesheet = SpriteSheet(IMG, IMG.get_width(), IMG.get_height(), 8, 1)
        self.width = self.spritesheet.getFrameWidth()
        self.height = self.spritesheet.getFrameHeight()
        self.screen_height = screen_height

        self.num_frames = 0
        
    def getScalar(self):
        return SCALAR

    def setSpeed(self):
        self.speed = 4

    def getWidth(self):
        return self.width
    def getHeight(self):
        return self.height
    
    def getPosX(self):
        return self.pos.x
    def getPosY(self):
        return self.pos.y
    
    def done(self):
        if self.num_frames == 8:
            self.num_frames = 0
            return True
    
    def next_frame(self):
        self.num_frames += 1
        self.spritesheet.frame_index[0] = (self.spritesheet.frame_index[0] + 1) % self.spritesheet.getColumns()
        if self.spritesheet.frame_index[0] == 0:
            self.spritesheet.frame_index[1] = (self.spritesheet.frame_index[1] + 1) % self.spritesheet.getRows()
    
    def update(self):
        self.pos.y += self.speed
        self.OOBCheck()

    def draw(self, canvas):
        CLOCK.tick()
        if(CLOCK.transition(10) == True):
            self.next_frame()
        if self.done():
            self.spritesheet.frame_index = [0, 0]
        
        self.spritesheet.draw(canvas, self.pos)
    
    def drawDebug(self, canvas):
        CLOCK.tick()
        if(CLOCK.transition(10) == True):
            self.next_frame()
        if self.done():
            self.spritesheet.frame_index = [0, 0]
        
        
        topLeft = (self.getPosX() - (self.getWidth() / 2) * SCALAR , self.getPosY() - (self.getHeight() / 2) * SCALAR)
        topRight = (self.getPosX() + (self.getWidth() / 2) * SCALAR, self.getPosY() - (self.getHeight() / 2) * SCALAR)
        bottomLeft = (self.getPosX() - (self.getWidth() / 2) * SCALAR, self.getPosY() + (self.getHeight() / 2) * SCALAR)
        bottomRight = (self.getPosX() + (self.getWidth() / 2) * SCALAR, self.getPosY() + (self.getHeight() / 2) * SCALAR)

        canvas.draw_polygon([topLeft, topRight, bottomRight, bottomLeft], 3, "Red")
        self.spritesheet.draw(canvas, self.pos)
    
    def OOBCheck(self):
        if self.pos.y > self.screen_height + 100:
            return True
        else:
            return False