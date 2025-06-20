try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

import random

from spritesheet import SpriteSheet

# IMG = simplegui.load_image("https://www.cs.rhul.ac.uk/home/zmac256/cs1822/asteroid1.png")
# SCALAR = 3.225
IMG = simplegui.load_image("https://www.cs.rhul.ac.uk/home/zmac256/cs1822/collisionexplosion.png")

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

class Explosion:
    def __init__(self, pos):
        self.pos = pos
        self.spritesheet = SpriteSheet(IMG, IMG.get_width(), IMG.get_height(), 7, 1)

        self.num_frames = 0
    
    def getPosX(self):
        return self.pos.x
    def getPosY(self):
        return self.pos.y
    
    def done(self):
        if self.num_frames == 7:
            return True
    
    def next_frame(self):
        self.num_frames += 1
        self.spritesheet.frame_index[0] = (self.spritesheet.frame_index[0] + 1) % self.spritesheet.getColumns()
        if self.spritesheet.frame_index[0] == 0:
            self.spritesheet.frame_index[1] = (self.spritesheet.frame_index[1] + 1) % self.spritesheet.getRows()

    def draw(self, canvas):
        CLOCK.tick()
        if(CLOCK.transition(5) == True):
            self.next_frame()
        if not self.done():
            self.spritesheet.draw(canvas, self.pos)
        
        