try:
    import simplegui

except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
# This class is used to handle the keyboard input
class Keyboard:
    def __init__(self):
        self.right = False # Boolean to check if the right arrow/d key is pressed
        self.left = False # Boolean to check if the left arrow/a key is pressed
        self.space = False # Boolean to check if the space key is pressed
        self.debug = False # Boolean to check if the p key is pressed
        self.mute = False # Boolean to check if the m key is pressed

    #simplegui.KEY_MAP['right'] is the right arrow key, simplegui.KEY_MAP['d'] is the d key etc.

    def keyDown(self, key): # This function is called when a key is pressed down
        if key == simplegui.KEY_MAP['right'] or key == simplegui.KEY_MAP['d']:
            self.right = True
            
        if key == simplegui.KEY_MAP['left'] or key == simplegui.KEY_MAP['a']:
            self.left = True
        
        if key == simplegui.KEY_MAP['space']:
            self.space = True
        
        if key == simplegui.KEY_MAP['p']:
            self.debug = not self.debug
        
        if key == simplegui.KEY_MAP['m']:
            self.mute = not self.mute

    def keyUp(self, key): # This function is called when a key is released
        if key == simplegui.KEY_MAP['right'] or key == simplegui.KEY_MAP['d']:
            self.right = False
            
        if key == simplegui.KEY_MAP['left'] or key == simplegui.KEY_MAP['a']:
            self.left = False
        
        if key == simplegui.KEY_MAP['space']:
            self.space = False