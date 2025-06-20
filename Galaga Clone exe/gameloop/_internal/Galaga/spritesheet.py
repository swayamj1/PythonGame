global CANVASHEIGHT, CANVASWIDTH
try:
    import simplegui

except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
    
class SpriteSheet:

    def __init__(self, img, width, height, columns, rows, pos = 0):
        self.img = img
        self.width = width
        self.height = height
        self.columns = columns
        if(pos != 0):
            self.pos = pos
        self.rows = rows

        self._init_dimension()
        self.frame_index = [0, 0]
    
    def getColumns(self):
        return self.columns
    def getRows(self):
        return self.rows
    

    def getPosX(self):
        return self.pos.x
    def getPosY(self):
        return self.pos.y

    def _init_dimension(self):
        self.frame_width = self.width / self.columns
        self.frame_height = self.height / self.rows
        self.frame_center_x = self.frame_width / 2
        self.frame_center_y = self.frame_height / 2

    def getFrameWidth(self):
        return self.frame_width
    def getFrameHeight(self):
        return self.frame_height
    def draw(self, canvas):
        source_centre = (
                self.frame_width * self.frame_index[0] + self.frame_center_x,
                self.frame_height * self.frame_index[1] + self.frame_center_y
            )
        source_size = (self.frame_width, self.frame_height)
        dest_centre = (self.pos.x, self.pos.y)
        dest_size = (self.frame_width, self.frame_height)

        canvas.draw_image(self.img, 
                        source_centre, 
                        source_size, 
                        dest_centre, 
                        dest_size)
    def draw(self, canvas, position):
        source_centre = (
                self.frame_width * self.frame_index[0] + self.frame_center_x,
                self.frame_height * self.frame_index[1] + self.frame_center_y
            )
        source_size = (self.frame_width, self.frame_height)
        dest_centre = (position.x, position.y)
        dest_size = (self.frame_width, self.frame_height)

        canvas.draw_image(self.img, 
                        source_centre, 
                        source_size, 
                        dest_centre, 
                        dest_size)
