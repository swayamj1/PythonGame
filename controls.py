from vector import Vector
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

# Global variables
LASERSFX = simplegui.load_sound("https://www.cs.rhul.ac.uk/home/zmac256/cs1822/laser_shooting_sfx.wav")
LASERSFX.set_volume(0.5)

# This class is responsible for handling the interaction between the player and the keyboard, performing the necessary actions when the keys are pressed like moving the player, shooting, muting the game and enabling debug mode.

class Controls:
    def __init__(self, player, keyboard):
        self.clock = simplegui.create_timer(300, self.timer) # Timer object to create a cooldown for the player's shooting ability.
        self.player = player # current player object
        self.keyboard = keyboard # current keyboard object
        self.cooldown = False # boolean to check if the player's shooting ability is on cooldown or not.

    def timer(self): # This method is used to create a cooldown for the player's shooting ability.
        if self.cooldown == True:
            self.cooldown = False
            self.clock.stop()
        else:
            self.cooldown = True

    def update(self):
        # If the right/d key is pressed, the player's velocity is increased by 1 in the x direction.
        if self.keyboard.right:
            self.player.vel.add(Vector(1, 0))
        # If the left/a key is pressed, the player's velocity is decreased by 1 in the x direction. 
        if self.keyboard.left:
            self.player.vel.add(Vector(-1,0))
        # If the mute key is pressed, the game is muted
        if self.keyboard.mute:
            self.player.mute = True
        else: # Else if its already muted, it is unmuted
            self.player.mute = False

        if self.keyboard.debug: # If the debug key is pressed, the debug mode is enabled; drawing the hitboxes of the player and the projectiles.
            self.player.debugMode = True
        else: # Else if debug mode is already enabled, the debug mode is disabled.
            self.player.debugMode = False

        if self.keyboard.space: # If the space key is pressed, the player's shooting ability is activated.
            # The cooldown timer starts, which runs repeatedly at an interval of 300ms, setting the cooldown to True if its False, and the other way around.
            self.clock.start()
            if self.cooldown == False: # If the cooldown is False, the player's shooting ability is activated.
                if(self.player.mute == False): # If the game is not muted, the laser sound effect is played.
                    LASERSFX.play()
                self.player.create_projectile()
                self.cooldown = True # The cooldown is set to True.


