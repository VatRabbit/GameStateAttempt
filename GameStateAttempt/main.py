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
        sprites = []
        spritesNumberWidth = 6
        spritesNumberHeight = 6
        spriteSheet = pygame.image.load('player/player.png').convert_alpha()
        spriteSheetWidth = spriteSheet.get_width()
        spriteSheetHeight = spriteSheet.get_height()
        spriteWidth = spriteSheetWidth // spritesNumberWidth
        spriteHeight = spriteSheetHeight // spritesNumberHeight
        
        for y in range(spritesNumberWidth):
            for x in range(spritesNumberHeight):                        
                spriteX = x * spriteWidth
                spriteY = y * spriteHeight                
                
                spriteRect = pygame.Rect(spriteX, spriteY, spriteWidth, spriteHeight)
                
                isBlank = True
                for i in range(spriteRect.width):
                    for j in range(spriteRect.height):
                        pixelColor = spriteSheet.get_at((spriteRect.x + i, spriteRect.y + j))
                        if pixelColor[3] != 0: # check the alpha channel
                            isBlank = False
                            break

                if not isBlank:
                    sprites.append(spriteSheet.subsurface(spriteRect))
        
        self.spriteListIdle   = [sprites[0],  sprites[1],  sprites[2],  sprites[3]]
        self.spriteListRun    = [sprites[4],  sprites[5],  sprites[6],  sprites[7], sprites[8],  sprites[9]]
        self.spriteListClimb  = [sprites[10], sprites[11], sprites[12], sprites[13]]
        self.spriteListCrouch = [sprites[14], sprites[15], sprites[16]]
        self.spriteListDeath  = [sprites[17], sprites[18]]
        self.spriteListJump   = [sprites[19], sprites[20]]     
        
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