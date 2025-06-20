try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui



IMG = simplegui.load_image("https://www.cs.rhul.ac.uk/home/zmac256/cs1822/laser.png")

class Projectile:
    def __init__(self, pos, vel):
        self.pos = pos
        self.vel = vel 
        self.width = IMG.get_width()
        self.height = IMG.get_height()

    def getPosX(self):
        return self.pos.x
    def getPosY(self):
        return self.pos.y
    
    def getWidth(self):
        return self.width
    def getHeight(self):    
        return self.height

    def update(self):
        self.pos.add(self.vel)
    
    def draw(self, canvas):
        canvas.draw_image(IMG, (IMG.get_width() / 2, IMG.get_height() / 2), (IMG.get_width(), IMG.get_height()), (self.pos.x, self.pos.y), (50, 50))

    def drawDebug(self, canvas):
        topLeft = (self.getPosX() - self.getWidth() / 2, self.getPosY() - self.getHeight() / 2 * 0.9)
        topRight = (self.getPosX() + self.getWidth() / 2, self.getPosY() - self.getHeight() / 2 * 0.9)
        bottomLeft = (self.getPosX() - self.getWidth() / 2, self.getPosY() + self.getHeight() / 2 * 0.95)
        bottomRight = (self.getPosX() + self.getWidth() / 2, self.getPosY() + self.getHeight() / 2 * 0.95)

        canvas.draw_polygon([topLeft, topRight, bottomRight, bottomLeft], 3, "Red")
        canvas.draw_image(IMG, (IMG.get_width() / 2, IMG.get_height() / 2), (IMG.get_width(), IMG.get_height()), (self.pos.x, self.pos.y), (50, 50))

    def OOBCheck(self):
        if self.pos.y > 800:
            return True
    
