# << import local classes

from spritesheet import SpriteSheet
from controls import Controls
from keyboard import Keyboard
from vector import Vector
from player import Player

try:
    import simplegui

except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

# >> 
    
# << global variables
CANVASHEIGHT = 800
CANVASWIDTH = 800

BACKGROUND = simplegui.load_image("https://www.cs.rhul.ac.uk/home/zmac256/cs1822/background.png")
SPACESHIP = simplegui.load_image("https://www.cs.rhul.ac.uk/home/zmac256/cs1822/ship.png")
MAINMENU = simplegui.load_image("https://www.cs.rhul.ac.uk/home/zmac256/cs1822/mainmenu.png")
INFOMENU = simplegui.load_image("https://www.cs.rhul.ac.uk/home/zmac256/cs1822/infomenu.png")



PLAYER = None
KBD = None
CONTROLS = None

BACKSHOWN = False
PLAYING = False
VICTORY = False
FAIL = False

# >>

def play_button(): # defines the properties of the play button.
    global PLAYER, KBD, CONTROLS
    # << when play button is pressed, it initialises the player, keyboard and controls objects.
    PLAYER = Player(Vector(CANVASWIDTH / 2, CANVASHEIGHT - 100), SPACESHIP)
    KBD = Keyboard()
    CONTROLS = Controls(PLAYER, KBD)
    # >>
    frame.set_keydown_handler(KBD.keyDown)
    frame.set_keyup_handler(KBD.keyUp)
    frame.set_draw_handler(playgame)
    frame.start()

def back_button(): # sets the draw handler to the main menu; only appears in the info menu.
    global BACKSHOWN
    BACKSHOWN = False
    frame.set_draw_handler(main_menu)
    frame.start()

def info_button(): # sets the draw handler to the info menu.
    global BACKSHOWN
    BACKSHOWN = True
    frame.set_draw_handler(info_menu)
    frame.start()

def quit_button(): # if the PLAYER variable is not None, it stops the Player clock and stops the frame.
    if(PLAYER != None):
        PLAYER.clock.stop()
    
    frame.stop()

def clickHandler(position): # handles the click events for the main menu, info menu and the victory and fail screens. Is always active checking for events

    # Global variables for game state
    global BACKSHOWN, PLAYING, VICTORY, FAIL

    # If the game is not currently playing
    if(not PLAYING): 
        # If the back button is shown
        if(BACKSHOWN):
            # Check if the click position is within the back button's area
            if(position[0] >= 587 and position[0] <= 771 and position[1] >= 35 and position[1] <= 124):
                back_button() # Call the back button function
        else:
            # Check if the click position is within the play button's area
            if(position[0] >= 53 and position[0] <= 356 and position[1] >= 474 and position[1] <= 581):
                PLAYING = True # Set the game state to playing
                play_button() # Call the play button function
            
            # Check if the click position is within the info button's area
            if(position[0] >= 437 and position[0] <= 741 and position[1] >= 474 and position[1] <= 581):
                info_button() # Call the info button function

            # Check if the click position is within the quit button's area
            if(position[0] >= 246 and position[0] <= 551 and position[1] >= 625 and position[1] <= 724):
                quit_button() # Call the quit button function
    else:
        # If the game is in a victory state
        if VICTORY:
            # Check if the click position is within the 'play again' button's area
            if(position[0] >= 24 and position[0] <= 377 and position[1] >= 637 and position[1] <= 751):
                # Reset game state
                PLAYER = None
                KBD = None
                CONTROLS = None
                PLAYING = False
                VICTORY = False
                frame.set_draw_handler(main_menu) # Set the draw handler to the main menu
                frame.start() # Start the frame
            # Check if the click position is within the quit button's area
            if (position[0] >= 418 and position[0] <= 771 and position[1] >= 637 and position[1] <= 751):
                quit_button() # Call the quit button function
        # If the game is in a fail state
        if FAIL:
            # Check if the click position is within the 'play again' button's area
            if(position[0] >= 52 and position[0] <= 359 and position[1] >= 668 and position[1] <= 762):
                # Reset game state
                PLAYER = None
                KBD = None
                CONTROLS = None
                PLAYING = False
                FAIL = False
                frame.set_draw_handler(main_menu) # Set the draw handler to the main menu
                frame.start() # Start the frame
            # Check if the click position is within the quit button's area
            if (position[0] >= 428 and position[0] <= 734 and position[1] >= 668 and position[1] <= 762):
                quit_button() # Call the quit button function
            
        

def main_menu(canvas): # Draws the image for the main menu of the game
    canvas.draw_image(MAINMENU, (MAINMENU.get_width() / 2, MAINMENU.get_height() / 2), (MAINMENU.get_width(), MAINMENU.get_height()), (CANVASWIDTH / 2, CANVASHEIGHT / 2), (CANVASWIDTH, CANVASHEIGHT))

def info_menu(canvas): # Draws the image for the info menu of the game
    global BACKSHOWN, BACK, QUIT
    canvas.draw_image(INFOMENU, (INFOMENU.get_width() / 2, INFOMENU.get_height() / 2), (INFOMENU.get_width(), INFOMENU.get_height()), (CANVASWIDTH / 2, CANVASHEIGHT / 2), (CANVASWIDTH, CANVASHEIGHT))

def playgame(canvas): # Main draw handler for the game loop, handles drawing the background image, updating the player and controls, and drawing the player and all of its objects (laser, meteor, etc.)
    global FAIL, VICTORY
    canvas.draw_image(BACKGROUND, (BACKGROUND.get_width() / 2, BACKGROUND.get_height() / 2), (BACKGROUND.get_width(), BACKGROUND.get_height()), (CANVASWIDTH / 2, CANVASHEIGHT / 2), (CANVASWIDTH, CANVASHEIGHT))
    if(PLAYER.deathCheck() != True): # If the player is not dead
        if(not PLAYER.bossDefeated):   # If the boss is not defeated  , draws the current score and level of the player and updates all the objects in the game.
            canvas.draw_text("SCORE: " + str(PLAYER.getScore()), (10, 30), 30, "Red", "monospace")
            canvas.draw_text("LEVEL: " + str(PLAYER.getLevel()), (10, 60), 30, "Red", "monospace")
            CONTROLS.update()
            PLAYER.update()
            PLAYER.draw(canvas) 
        else: # If the boss is defeated, loads the victory screen and stops the player clock.
            VICTORY = True
            victory = simplegui.load_image("https://www.cs.rhul.ac.uk/home/zmac256/cs1822/victory.png")
            canvas.draw_image(victory, (victory.get_width() / 2, victory.get_height() / 2), (victory.get_width(), victory.get_height()), (CANVASWIDTH / 2, CANVASHEIGHT / 2), (800, 800))
            canvas.draw_text("FINAL SCORE: " + str(PLAYER.getScore()), (350, 30), 30, "Red", "monospace")
            PLAYER.clock.stop()
    else: # If the player is dead, loads the fail screen and stops the player clock.
        FAIL = True
        gameover = simplegui.load_image("https://www.cs.rhul.ac.uk/home/zmac256/cs1822/gameover.png")
        canvas.draw_image(gameover, (gameover.get_width() / 2, gameover.get_height() / 2), (gameover.get_width(), gameover.get_height()), (CANVASWIDTH / 2, CANVASHEIGHT / 2), (800, 800))
        canvas.draw_text("FINAL SCORE: " + str(PLAYER.getScore()), (10, 30), 30, "Red", "monospace")
        PLAYER.clock.stop()

# Initialise the frame and set the mouse click handler to the clickHandler function and the draw handler to the main_menu function
frame = simplegui.create_frame("Galaga Clone", CANVASHEIGHT, CANVASWIDTH)

frame.set_mouseclick_handler(clickHandler)
frame.set_draw_handler(main_menu)

# Start the frame/game
frame.start()



