import sys
import pygame
import Invader
import Missile
from pygame.locals import *

class SpaceInvader:

    # Constructor of the basic game class.
    # This constructor calls initialize and main_loop method.
    def __init__(self):
        self.initialize()
        self.main_loop()

    # Initialization method. Allows the game to initialize different
    # parameters and load assets before the game runs
    def initialize(self):
        pygame.init()
        pygame.key.set_repeat(1, 1)

        self.width = 1024
        self.height = 768
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.caption = "Space Invader"
        pygame.display.set_caption(self.caption)

        self.invaderIcon = pygame.image.load("Stormtrooper.png")
        pygame.display.set_icon(self.invaderIcon)
                
        self.framerate = 60

        self.clock = pygame.time.Clock()
                
        self.gameState = 1
        
        #Sets out the font
        self.font = pygame.font.Font(None, 100)
        self.font_score = pygame.font.Font(None, 40)
        self.font_subtitle = pygame.font.Font(None, 50)
                
        #loads the sound effects in the game
        self.explosionSound = pygame.mixer.Sound("explosion.wav")
        self.shootSound = pygame.mixer.Sound("shoot.wav")
        self.moveSound = pygame.mixer.Sound("fastinvader1.wav")
        self.initializeGameVariables()

    def initializeGameVariables(self):
        self.starfieldImg = pygame.image.load('Space.png')
        self.invaderImg = pygame.image.load('Stormtrooper.png')
        #self.altInvaderImg = pygame.image.load('Stormtrooper.png')
        self.rocketLauncherImg = pygame.image.load('R2D2.png')        
        self.missileImg = pygame.image.load('Beam.png')
        self.helpImg = pygame.image.load('Help.png')

        self.rocketXPos = 512

        self.alienDirection = -1            
        self.alienSpeed = 40

        self.ticks = 0

        self.invaders = []

        yPos = 100
        for row in range (5):
            invaderlist = []
            xPos = 512
            for column in range (11):
                invader = Invader.Invader()
                invader.setPosX(xPos)
                invader.setPosY(yPos)
                invaderlist.append(invader)
                xPos += 32
            self.invaders.append(invaderlist)
            yPos += 32
 
            
        self.missileFired = None

        self.playerScore = 0

        
    # main loop method keeps the game running. This method continuously
    # calls the update and draw methods to keep the game alive.
    def main_loop(self):
        self.clock = pygame.time.Clock()
        while True:
            gametime = self.clock.get_time()
            self.update(gametime)
            self.draw(gametime)
            self.clock.tick(self.framerate)

    # Update method contains game update logic, such as updating the game
    # variables, checking for collisions, gathering input, and
    # playing audio.
    def update(self, gametime):        
        if self.gameState == 1:
            self.updateStarted(gametime)
        elif self.gameState == 2:
            self.updatePlaying(gametime)
        elif self.gameState == 3:
            self.updateEnded(gametime)
        elif self.gameState == 4:
            self.updateHelp(gametime)

    def updateHelp(self, gametime):
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    self.gameState = 1
                    break

    def updateStarted(self, gametime):        
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    self.gameState = 2
                if event.key == pygame.K_h:
                    self.gameState = 4
                    break

    def updatePlaying(self, gametime):
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.rocketXPos = self.rocketXPos + 6
                elif event.key == pygame.K_LEFT:
                    self.rocketXPos = self.rocketXPos - 6
                elif event.key == pygame.K_SPACE:
                    self.missileFired = Missile.Missile(self.rocketXPos, 650)
                    self.shootSound.play()

        isInvaderRemaining = False
        for row in range(5):
            for col in range (11):
                if self.invaders[row][col] != None:
                    isInvaderRemaining = True
                    break
        if isInvaderRemaining == False:
            self.gameState = 3
            return
        
        if self.missileFired != None:
            self.missileFired.move()
        
        if self.rocketXPos < 100:
            self.rocketXPos = 100

        if self.rocketXPos > 924:
            self.rocketXPos = 924

        self.ticks = self.ticks + gametime

        if self.ticks > 500:
            for row in range(5):
                for col in range (11):
                    if self.invaders[row][col] != None:
                        self.invaders[row][col].moveHorizontal(self.alienSpeed * self.alienDirection)
                        #plays the alien move sound
                        self.moveSound.play()

            leftMostInvader = None
            rightMostInvader = None

            for row in range(1):
                for col in range (11):
                    if self.invaders[row][col] != None:
                        leftMostInvader = self.invaders[row][col]
                        break
                    
            for row in range(1): 
                for col in range(10, -1, -1):
                    if self.invaders[row][col] != None:
                        rightMostInvader = self.invaders[row][col]
                        break

            if leftMostInvader.getPosX() < 96:
                self.alienDirection = +1
                self.alienSpeed = self.alienSpeed * 1.01 # speeds up rows as they go down more
            
                for row in range(5):
                    xPos = 96
                    for col in range (11):
                        if self.invaders[row][col] != None:
                            self.invaders[row][col].moveVertical(8)
                            self.invaders[row][col].setPosX(xPos)
                        xPos = xPos + self.invaderImg.get_width()

            if rightMostInvader.getPosX() > 924 :
                self.alienDirection = -1
                self.alienSpeed = self.alienSpeed * 1.01 # speeds up rows as they go down more
 
                for row in range(5):
                    xPos = 924 - self.invaderImg.get_width() * 10
                    for col in range (11):
                        if self.invaders[row][col] != None:
                            self.invaders[row][col].moveVertical(8)
                            self.invaders[row][col].setPosX(xPos)
                        xPos = xPos + self.invaderImg.get_width()
                    
            self.ticks = 0
        #Collision Detected 
        if self.missileFired != None:
            rectMissile = pygame.Rect(self.missileFired.getPosX(), self.missileFired.getPosY(), \
                                      self.missileImg.get_width(), self.missileImg.get_height())
            for row in range(5):
                for col in range (11):
                    if self.invaders[row][col] != None:
                        rectInvader = pygame.Rect(self.invaders[row][col].getPosX(), self.invaders[row][col].getPosY(),\
                                              self.invaderImg.get_width(), self.invaderImg.get_height())

                        rectBase = pygame.Rect((0,650),(1024,650))
                        #end game if alien reaches launcher  
                        if rectInvader.colliderect(rectBase):
                            self.gameState = 3
                            
                     #If missile collides with Invader       
                    if rectMissile.colliderect(rectInvader):
                        self.missileFired = None
                        self.invaders[row][col] = None   
                        #self.alienSpeed = self.alienSpeed * 10 # speeds up aliens everytime 1 is shot
                        #sets the score for hitting an alien
                        self.playerScore = self.playerScore + 10
                        #plays the explosion sound effect as the alien is killed
                        self.explosionSound.play()
                        break


    def updateEnded(self, gametime):
        #loop checks whether the keys X or R have been pressed and then runs corresponding code
        #i.e. R restarts game X exits the game
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_r:
                    self.initializeGameVariables()
                    self.gameState = 1   
        
        

    # Draw method, draws the current state of the game on the screen                        
    def draw(self, gametime):              
        if self.gameState == 1:
            self.drawStarted(gametime)
        elif self.gameState == 2:
            self.drawPlaying(gametime)
        elif self.gameState == 3:
            self.drawEnded(gametime)
        elif self.gameState == 4:
            self.drawHelp(gametime)

    def drawHelp(self, gametime):
        self.screen.blit(self.starfieldImg, (0,0))
        self.screen.blit(self.helpImg, ((1024-500)/2 ,125))

        #determines the width and height of the string in px 
        width, height = self.font.size("H E L P")
        #converts the text into an image
        text = self.font.render("H E L P", True, (255,255,0))
        #positions the text relative to the size of the window, in this case it is centred (total width/ 2)
        xPos = (1024 - width)/2
        #displays the text on the game screen
        self.screen.blit(text, (xPos, 10))

        width, height = self.font_subtitle.size("P R E S S   'B'   T O    G O   B A C K ")
        text = self.font_subtitle.render("P R E S S   'B'   T O   G O   B A C K", True, (255,255,0))
        xPos= (1024 - width)/2
        self.screen.blit(text, (xPos, 650))

        pygame.display.flip()

    def drawStarted(self, gametime):
        self.screen.blit(self.starfieldImg, (0,0))

        #determines the width and height of the string in px 
        width, height = self.font.size("S P A C E   I N V A D E R S")
        #converts the text into an image
        text = self.font.render("S P A C E   I N V A D E R S", True, (255,255,0))
        #positions the text relative to the size of the window, in this case it is centred (total width/ 2)
        xPos = (1024 - width)/2
        #displays the text on the game screen
        self.screen.blit(text, (xPos, 200))

        width, height = self.font_subtitle.size("P R E S S   'S'   T O   S T A R T")
        text = self.font_subtitle.render("P R E S S   'S'   T O   S T A R T", True, (255,255,0))
        xPos= (1024 - width)/2
        self.screen.blit(text, (xPos, 500))

        width, height = self.font_subtitle.size("P R E S S   'H'  F O R   H E L P ")
        text = self.font_subtitle.render("P R E S S   'H'   F O R   H E L P", True, (255,255,0))
        xPos= (1024 - width)/2
        self.screen.blit(text, (xPos, 600))

        pygame.display.flip()

    def drawPlaying(self, gametime):
        self.screen.blit(self.starfieldImg, (0,0))
        
        #draws the word score followed by the users score
        score_text = self.font_score.render("Score : %d" %self.playerScore, True, (255,255,0))
        self.screen.blit(score_text, (10,10))
        
        self.screen.blit(self.rocketLauncherImg, (self.rocketXPos, 650))
        if self.missileFired != None:
            self.screen.blit(self.missileImg, (self.missileFired.getPosX(), self.missileFired.getPosY() - self.missileImg.get_height()))
        for row in range(5):
            for col in range (11):
                if self.invaders[row][col] != None:
                    self.screen.blit(self.invaderImg, self.invaders[row][col].getPosition())
        pygame.display.flip()           

    def drawEnded(self, gametime):
        self.screen.blit(self.starfieldImg, (0,0))

        width, height = self.font_subtitle.size("Score : %d ")
        text=self.font_subtitle.render("Score : %d" %self.playerScore, True, (255,255,0))
        xPos = (1024 - width)/2
        self.screen.blit(text, (xPos,100))
        
        width, height = self.font_subtitle.size("P R E S S   'R'   T O   R E S T A R T")
        text=self.font_subtitle.render("P R E S S   'R'   T O   R E S T A R T", True, (255,255,0))
        xPos = (1024 - width)/2
        self.screen.blit(text, (xPos,300))

        width, height = self.font_subtitle.size("P R E S S   'X'   T O   Q U I T")
        text=self.font_subtitle.render("P R E S S   'X'   T O   Q U I T", True, (255,255,0))
        xPos = (1024 - width)/2
        self.screen.blit(text, (xPos,400))

        pygame.display.flip()
        
if __name__ == "__main__":
    game = SpaceInvader()
