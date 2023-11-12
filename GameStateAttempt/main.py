import pygame
from sys import exit

SCREENWIDTH, SCREENHEIGHT = 800, 600  
FPS = 60

class Game:
    def __init__(self):
        pygame.init()          
        self.display = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        self.clock = pygame.time.Clock()
        self.player = Player(self.display)
        self.gameStateManager = GameStateManager('menu')  
        self.menu = Menu(self.display, self.gameStateManager)         
        self.level = Level(self.display, self.gameStateManager, self.player)         
        self.states = {'level': self.level, 'menu': self.menu}   
        
    def mainLoop(self):
        while True:   
            self.events = pygame.event.get() 
            for event in self.events:
                if event == pygame.QUIT:
                    pygame.quit()
                    exit()
            self.display.fill('black')
            self.states[self.gameStateManager.getState()].run(self.events)            
            pygame.display.update()
            self.clock.tick(FPS)
    
class GameStateManager:
    def __init__(self, currentState):
        self.currentState = currentState
    
    def setState(self, state):
        self.currentState = state
        
    def getState(self):
        return self.currentState
    
class Menu:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        
    def run(self, events):        
        self.display.fill('blue')
        for event in events:             
             if event.type == pygame.KEYDOWN:
                 self.gameStateManager.setState('level')
        
class Level:
    def __init__(self, display, gameStateManager, player):
        self.display = display
        self.gameStateManager = gameStateManager
        self.player = player
        
    def run(self, events):
        for event in events:
            pass
                 
        self.display.fill('red')
        self.player.update(events)
        
class Player(pygame.sprite.Sprite):
    def __init__(self, display):
        super().__init__()
        self.display = display
        self.sprites = []
        self.loadSpriteSheet() 
        self.frame = 0
        self.lastUpdate = pygame.time.get_ticks()
        self.animationCooldown = 100
        #self.animationStates = {'idle': pass, 'run': pass}
        self.animationState = 'idle'
        
    def update(self, events):
        # scaledSprite = pygame.transform.scale(self.animationIdle[0], (self.animationIdle[0].get_width() * 2, self.animationIdle[0].get_height() * 2))
        # self.display.blit(scaledSprite, (100, 100))
        # self.printSprites()
        self.animate(events)
        
    def printSprites(self):
        for i in range(len(self.animationRun)):
            self.display.blit(self.animationRun[i], (50*i,50))

    def loadSpriteSheet(self):
        # 198 x 192p spritesheet with 6 collumbs and 6 rows 
        self.spritesNumberWidth = 6
        self.spritesNumberHeight = 6
        self.spriteSheet = pygame.image.load('player/player.png').convert_alpha()
        self.spriteSheetWidth = self.spriteSheet.get_width()
        self.spriteSheetHeight = self.spriteSheet.get_height()
        self.spriteWidth = self.spriteSheetWidth // self.spritesNumberWidth
        self.spriteHeight = self.spriteSheetHeight // self.spritesNumberHeight
        
        for y in range(self.spritesNumberWidth):
            for x in range(self.spritesNumberHeight):                        
                self.spriteX = x * self.spriteWidth
                self.spriteY = y * self.spriteHeight                
                
                spriteRect = pygame.Rect(self.spriteX, self.spriteY, self.spriteWidth, self.spriteHeight)
                
                isBlank = True
                for i in range(spriteRect.width):
                    for j in range(spriteRect.height):
                        pixelColor = self.spriteSheet.get_at((spriteRect.x + i, spriteRect.y + j))
                        if pixelColor[3] != 0: # check the alpha channel
                            isBlank = False
                            break

                if not isBlank:
                    self.sprites.append(self.spriteSheet.subsurface(spriteRect))
        
        self.animationIdle   = [self.sprites[0],  self.sprites[1],  self.sprites[2],  self.sprites[3]]
        self.animationRun    = [self.sprites[4],  self.sprites[5],  self.sprites[6],  self.sprites[7],
                                self.sprites[8],  self.sprites[9]]
        self.animationClimb  = [self.sprites[10], self.sprites[11], self.sprites[12], self.sprites[13]]
        self.animationCrouch = [self.sprites[14], self.sprites[15], self.sprites[16]]
        self.animationDeath  = [self.sprites[17], self.sprites[18]]
        self.animationJump   = [self.sprites[19], self.sprites[20]]
                               
        '''   
        self.spriteStates = {'Idle0'  : self.sprites[0],
                             'Idle1'  : self.sprites[1],
                             'Idle2'  : self.sprites[2],
                             'Idle3'  : self.sprites[3],
                             'Run0'   : self.sprites[4],
                             'Run1'   : self.sprites[5],
                             'Run2'   : self.sprites[6],
                             'Run3'   : self.sprites[7],
                             'Run4'   : self.sprites[8],
                             'Run5'   : self.sprites[9],
                             'Climb0' : self.sprites[10],
                             'Climb1' : self.sprites[11],
                             'Climb2' : self.sprites[12],
                             'Climb3' : self.sprites[13],
                             'Crouch0': self.sprites[14],
                             'Crouch1': self.sprites[15],
                             'Crouch2': self.sprites[16],
                             'Death0' : self.sprites[17],
                             'Death1' : self.sprites[18],
                             'Jump0'  : self.sprites[19],
                             'Jump1'  : self.sprites[20]}

                             
        self.animationIdle = {'Idle0' : self.sprites[0],
                              'Idle1' : self.sprites[1],
                              'Idle2' : self.sprites[2],
                              'Idle3' : self.sprites[3]}
                
        self.animationRun = {'Run0' : self.sprites[4],
                             'Run1' : self.sprites[5],
                             'Run2' : self.sprites[6],
                             'Run3' : self.sprites[7],
                             'Run4' : self.sprites[8],
                             'Run5' : self.sprites[9]}
        
        self.animationClimb = {'Climb0' : self.sprites[10],
                               'Climb1' : self.sprites[11],
                               'Climb2' : self.sprites[12],
                               'Climb3' : self.sprites[13]}
        
        self.animationCrouch = {'Crouch0': self.sprites[14],
                                'Crouch1': self.sprites[15],
                                'Crouch2': self.sprites[16]}
        
        self.animationDeath = {'Death0' : self.sprites[17],
                               'Death1' : self.sprites[18]}
        
        self.animationJump = {'Jump0' : self.sprites[19],
                              'Jump1' : self.sprites[20]}
        '''
        
    def animate(self, events):
        currentTime = pygame.time.get_ticks()

        if (currentTime - self.lastUpdate >= self.animationCooldown):
            self.frame += 1
            self.lastUpdate = currentTime
            if (self.frame >= len(self.animationIdle)):
                self.frame = 0                
                
        self.display.blit(self.animationIdle[self.frame], (100,100))
        
if __name__ == '__main__':
    game = Game()
    game.mainLoop()