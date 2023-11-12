import pygame
from sys import exit

SCREENWIDTH, SCREENHEIGHT = 400, 400  
FPS = 60
DISPLAY_SCALE = 2

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
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            self.display.fill('black')
            self.states[self.gameStateManager.getState()].run(self.events) 
            scaledDisplay = pygame.transform.scale(self.display, (self.display.get_width() * DISPLAY_SCALE, self.display.get_height() * DISPLAY_SCALE))
            self.display.blit(scaledDisplay, (0,0))
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
        self.loadSpriteSheet()       
        self.animationStateManager = self.AnimationStateManager('idle')
        self.animationIdle = self.AnimationIdle(display)
        self.animationRun = self.AnimationRun(display)
        self.animationStates = {'idle': self.animationIdle, 'run': self.animationRun}
        self.sprites = self.spriteListIdle
        self.spriteRect = self.sprites[0].get_rect(topleft = (0,0))
        
    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.K_RIGHT:                    
                    self.animationStateManager.setState('run')
                else:
                    self.animationStateManager.setState('idle')
            
        self.animationStates[self.animationStateManager.getState()].run(self.sprites, self.spriteRect)
        
    def printSprites(self):
        for i in range(len(self.animationRun)):
            self.display.blit(self.animationRun[i], (50*i,50))

    def loadSpriteSheet(self):
        # 198 x 192p spritesheet with 6 collumbs and 6 rows 
        self.sprites = []
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
        
        self.spriteListIdle   = [self.sprites[0],  self.sprites[1],  self.sprites[2],  self.sprites[3]]
        self.spriteListRun    = [self.sprites[4],  self.sprites[5],  self.sprites[6],  self.sprites[7],
                                 self.sprites[8],  self.sprites[9]]
        self.spriteListClimb  = [self.sprites[10], self.sprites[11], self.sprites[12], self.sprites[13]]
        self.spriteListCrouch = [self.sprites[14], self.sprites[15], self.sprites[16]]
        self.spriteListDeath  = [self.sprites[17], self.sprites[18]]
        self.spriteListJump   = [self.sprites[19], self.sprites[20]]     
        
    class AnimationStateManager:
        def __init__(self, currentState):
            self.currentState = currentState
        
        def getState(self):
            return self.currentState
        
        def setState(self, state):
            self.currentState = state
        
    class AnimationIdle:
        def __init__(self, display):          
            self.display = display
            self.frame = 0
            self.animationCooldown = 125
            self.lastUpdate = pygame.time.get_ticks()
            
        def run(self, sprites, rect):
            currentTime = pygame.time.get_ticks()
            
            if (currentTime - self.lastUpdate >= self.animationCooldown):
                self.frame += 1
                self.lastUpdate = currentTime
                if (self.frame >= len(sprites)):
                    self.frame = 0     
            self.display.blit(sprites[self.frame], rect)
            
    class AnimationRun:
        def __init__(self, display):
            self.display = display
            self.frame = 0
            self.animationCooldown = 100
            self.lastUpdate = pygame.time.get_ticks()
            
        def run(self, sprites, rect):
            currentTime = pygame.time.get_ticks
            
            if (currentTime - self.lastUpdate >= self.animationCooldown):
                self.frame += 1
                self.lastUpdate = currentTime
                if (self.frame >= len(sprites)):
                    self.frame = 0
            self.display.blit(sprites[self.frame], (rect))
            
if __name__ == '__main__':
    game = Game()
    game.mainLoop()