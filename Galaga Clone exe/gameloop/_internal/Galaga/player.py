from vector import Vector
from spritesheet import SpriteSheet
from projectile import Projectile
from asteroid import Asteroid
from explosion import Explosion
from asteroidboss import asteroidboss

import random

try :
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
SCALAR = 2.175

MUTED = simplegui.load_image("https://www.cs.rhul.ac.uk/home/zmac256/cs1822/Muted.png")
UNMUTED = simplegui.load_image("https://www.cs.rhul.ac.uk/home/zmac256/cs1822/Unmuted.png")
COLLISIONEXP = simplegui.load_image("https://www.cs.rhul.ac.uk/home/zmac256/cs1822/collisionexplosion.png")

SOUNDTRACK = simplegui.load_sound("https://www.cs.rhul.ac.uk/home/zmac256/cs1822/GalagaTheme.wav")

EXPLOSION = simplegui.load_sound("https://www.cs.rhul.ac.uk/home/zmac256/cs1822/explosionsfx.wav")
BIGEXPLOSION = simplegui.load_sound("https://www.cs.rhul.ac.uk/home/zmac256/cs1822/bigexplosionsfx.wav")
BIGEXPLOSIONPLAYED = False

class Player:

    def __init__(self, pos, image):
        self.pos = pos
        self.score = 0
        self.level = 1
        self.tempScore = 0
        self.levelUpDrawTimer = 0

        self.resetSounds()

        self.bossPhase = False
        self.bossDefeated = False
        self.bossSpawned = False
        self.debugMode = False
        self.mute = False
        self.dead = False

        self.vel = Vector()
        self.image = image
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.lasers = []
        self.asteroids = []
        self.collisionexplosions = []
        self.bossasteroid = None

        self.interval = 3000
        self.clock = simplegui.create_timer(self.interval, self.timer)
        self.clock.start()
    
    def timer(self):
        #remember to change this back to 100 !!!!!!!!!
        if (self.score < 100):
            self.create_asteroid()
        else:
            if(self.bossSpawned == False):
                self.create_boss_asteroid()
                self.bossSpawned = True
                self.bossPhase = True
                self.level = "BOSS FIGHT"
                self.reduceInterval()
            self.create_asteroid()

    # <<< Getter functions 
    def getInterval(self):
        return self.interval
    
    def getLevel(self):
        return self.level
    def getScore(self):
        return self.score
    
    def getPosX(self):
        return self.pos.x
    def getPosY(self):
        return self.pos.y
    
    def getWidth(self):
        return self.width
    def getHeight(self):
        return self.height
    
    def isMuted(self):
        return self.mute
    
    def isDead(self):
        return self.dead
    # >>>

    def checkInterval(self):
        if(self.interval - 250 >= 1000 and not self.bossPhase):
            return True
        else:
            return False
        
    def resetSounds(self):
        global BIGEXPLOSIONPLAYED

        SOUNDTRACK.pause()
        SOUNDTRACK.rewind()
        EXPLOSION.pause()
        EXPLOSION.rewind()
        BIGEXPLOSION.pause()
        BIGEXPLOSION.rewind()
        BIGEXPLOSIONPLAYED = False

    

    def reduceInterval(self):
        if not self.bossPhase:
            self.interval -= 250
            self.clock.stop()
            self.clock = simplegui.create_timer(self.interval, self.timer)
            self.clock.start()
            self.level += 1
        else:
            self.interval = 500
            self.clock.stop()
            self.clock = simplegui.create_timer(self.interval, self.timer)
            self.clock.start()
        

    def create_boss_asteroid(self):
        self.bossasteroid = asteroidboss()
        
    def create_asteroid(self):
        rnd = random.randint(50, 751)
        asteroid_pos = Vector(rnd, -50)
        asteroid = Asteroid(asteroid_pos, 800)
        if(not self.bossPhase):
            self.asteroids.append(asteroid)
        else:
            asteroid.setSpeed()
            self.asteroids.append(asteroid)


    def deathCheck(self):
        global BIGEXPLOSIONPLAYED
        if len(self.asteroids) > 0:
            for asteroid in self.asteroids:
                if self.getPosX() - (self.getWidth() / 2) * SCALAR <= asteroid.getPosX() + (asteroid.getWidth() / 2) * asteroid.getScalar() and self.getPosX() + (self.getWidth() / 2) * SCALAR >= asteroid.getPosX() - (asteroid.getWidth() / 2) * asteroid.getScalar() and self.getPosY() - (self.getHeight() / 2) * SCALAR <= asteroid.getPosY() + (asteroid.getHeight() / 2) * asteroid.getScalar() and self.getPosY() + (self.getHeight() / 2) * SCALAR >= asteroid.getPosY() - (asteroid.getHeight() / 2) * asteroid.getScalar():
                    self.dead = True
                    if(not self.isMuted() and not BIGEXPLOSIONPLAYED):
                        SOUNDTRACK.pause()
                        SOUNDTRACK.rewind()
                        BIGEXPLOSION.play()
                        BIGEXPLOSIONPLAYED = True
                    return True
        return False
    
    def update(self):
        self.pos.add(self.vel)
        self.vel.multiply(0.85)
        if len(self.asteroids) > 0:
            for asteroid in self.asteroids:
                asteroid.update()
        if len(self.lasers) > 0:
            for laser in self.lasers:
                laser.update()
        
        if(self.tempScore != self.score):
            if (self.score % 10 == 0 and self.score != 0 and self.checkInterval()):
                self.levelUpDrawTimer = 120
                self.reduceInterval()
                self.tempScore = self.score
        
        if(self.bossPhase and not self.bossDefeated):
            for laser in self.lasers:
                if laser.getPosX() - laser.getWidth() / 2 <= self.bossasteroid.getPosX() + (self.bossasteroid.getWidth() / 2) * self.bossasteroid.getScalar() and laser.getPosX() + laser.getWidth() / 2 >= self.bossasteroid.getPosX() - (self.bossasteroid.getWidth()) * self.bossasteroid.getScalar() / 2 and laser.getPosY() - laser.getHeight() / 2 <= self.bossasteroid.getPosY() + (self.bossasteroid.getHeight() / 2) * self.bossasteroid.getScalar() and laser.getPosY() + laser.getHeight() / 2 >= self.bossasteroid.getPosY() - (self.bossasteroid.getHeight() / 2) * self.bossasteroid.getScalar():
                        if(self.bossasteroid.getHealth() > 0):
                            currentpos = Vector(laser.getPosX(), laser.getPosY() - laser.getHeight() / 2)
                            self.bossasteroid.reduceScalar()
                            self.collisionexplosions.append(Explosion(currentpos))
                            self.lasers.remove(laser)
                        else:
                            self.lasers.remove(laser)
                            self.bossDefeated = True

        if len(self.asteroids) > 0 and len(self.lasers) > 0:
            for laser in self.lasers:
                for asteroid in self.asteroids:
                    if laser.getPosX() - laser.getWidth() / 2 <= asteroid.getPosX() + (asteroid.getWidth() / 2) * asteroid.getScalar() and laser.getPosX() + laser.getWidth() / 2 >= asteroid.getPosX() - (asteroid.getWidth()) * asteroid.getScalar() / 2 and laser.getPosY() - laser.getHeight() / 2 <= asteroid.getPosY() + (asteroid.getHeight() / 2) * asteroid.getScalar() and laser.getPosY() + laser.getHeight() / 2 >= asteroid.getPosY() - (asteroid.getHeight() / 2) * asteroid.getScalar():
                        self.score += 1
                        if(not self.isMuted()):
                            EXPLOSION.play()
                        currentpos = Vector(asteroid.getPosX(), asteroid.getPosY() + asteroid.getHeight() / 2)
                        self.collisionexplosions.append(Explosion(currentpos))
                        self.asteroids.remove(asteroid)
                        self.lasers.remove(laser)

        if not self.isMuted() and not self.isDead():
            SOUNDTRACK.play()
        else:
            SOUNDTRACK.pause()
        
        self.OOBCheck()

    def create_projectile(self):
        projectile_pos = Vector(self.pos.x, self.pos.y)
        projectile_vel = Vector(0, -(12))  # Assuming upward direction

        self.lasers.append(Projectile(projectile_pos, projectile_vel))
    
    def draw(self, canvas): 
        if(self.bossPhase and not self.bossDefeated):
            self.bossasteroid.draw(canvas)
        
        for laser in self.lasers:
            if self.debugMode:
                laser.drawDebug(canvas)
            else:
                laser.draw(canvas)
        for asteroid in self.asteroids:
            if self.debugMode:
                asteroid.drawDebug(canvas)
            else:
                asteroid.draw(canvas)
        for explosion in self.collisionexplosions:
            if explosion.done():
                self.collisionexplosions.remove(explosion)
                continue
            explosion.draw(canvas)

        
            
        if(self.levelUpDrawTimer > 0 and self.levelUpDrawTimer < 120):
            canvas.draw_text("Meteor Intensity Increasing!", (230, 30) , 30, "Red", "monospace")
        
        if not self.isMuted():
            canvas.draw_image(UNMUTED, (UNMUTED.get_width() / 2, UNMUTED.get_height() / 2), (UNMUTED.get_width(), UNMUTED.get_height()), (800 - UNMUTED.get_width() / 2 - 15, 0 + UNMUTED.get_height() / 2 + 15), (UNMUTED.get_width(), UNMUTED.get_height()))
        else:
            canvas.draw_image(MUTED, (MUTED.get_width() / 2, MUTED.get_height() / 2), (MUTED.get_width(), MUTED.get_height()), (800 - MUTED.get_width() / 2 - 15, 0 + MUTED.get_height() / 2 + 15), (MUTED.get_width(), MUTED.get_height()))

        self.levelUpDrawTimer -= 1
        if self.debugMode:
            if self.getScore() == 5:
                self.bossDefeated = True
            
            canvas.draw_text("DEBUG MODE", (10, 90), 30, "Red", "monospace")
            topLeft = (self.getPosX() - (self.getWidth() / 2) * SCALAR, self.getPosY() - (self.getHeight() / 2) * SCALAR)
            topRight = (self.getPosX() + (self.getWidth() / 2) * SCALAR, self.getPosY() - (self.getHeight() / 2) * SCALAR)
            bottomLeft = (self.getPosX() - (self.getWidth() / 2) * SCALAR, self.getPosY() + (self.getHeight() / 2) * SCALAR)
            bottomRight = (self.getPosX() + (self.getWidth() / 2) * SCALAR, self.getPosY() + (self.getHeight() / 2) * SCALAR)

            canvas.draw_polygon([topLeft , topRight , bottomRight , bottomLeft], 3, "Red")

        canvas.draw_image(self.image, (self.getWidth() / 2, self.getHeight() / 2), (self.getWidth(), self.getHeight()), (self.getPosX(), self.getPosY()), (100, 100))

    def OOBCheck(self):
        for laser in self.lasers:
            if laser.OOBCheck():
                self.lasers.remove(laser)
        for asteroid in self.asteroids:
            if asteroid.OOBCheck():
                self.asteroids.remove(asteroid)

        if self.pos.x > 800:
            self.pos.x = 0
        elif self.pos.x < 0:
            self.pos.x = 800