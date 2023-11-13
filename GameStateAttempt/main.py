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
        self.display.fill('red')
        self.player.update(events)
        
class Player(pygame.sprite.Sprite):
    def __init__(self, display):
        super().__init__()
        self.display = display
        self.loadSpriteSheet()       
        self.animationStateManager = self.AnimationStateManager('idle')
        self.animationIdle = self.AnimationIdle(display, self.spriteListIdle)
        self.animationRun = self.AnimationRun(display, self.spriteListRun)
        self.animationStates = {'idle': self.animationIdle, 'run': self.animationRun}
        self.sprites = self.spriteListIdle
        self.spriteRect = self.sprites[0].get_rect(topleft = (0,0))
        self.reverse = False
        
    def update(self, events):
        self.handleInput(events)       
        self.animationStates[self.animationStateManager.getState()].run(self.spriteRect, self.reverse)
        
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
        
    def handleInput(self, events):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] == True and keys[pygame.K_RIGHT] == True:
            self.animationStateManager.setState('idle')
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.type == pygame.K_LEFT or event.type == pygame.K_RIGHT:
                        self.animationIdle.frame = 0
                    
        elif keys[pygame.K_LEFT] == True:
            self.animationStateManager.setState('run')
            self.reverse = True
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.animationRun.frame = 0                                            
                        
        elif keys[pygame.K_RIGHT] == True:
            self.animationStateManager.setState('run')
            self.reverse = False
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.animationRun.frame = 0                        
            
        elif keys[pygame.K_LEFT] == False and keys[pygame.K_RIGHT] == False:
            self.animationStateManager.setState('idle')
            for event in events:
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.animationIdle.frame = 0
            
        '''
        for event in events:
            if event.type == pygame.KEYUP:
                print('key up')
                
                if event.key == pygame.K_RIGHT:
                    print('right key up')
                    
                    if event.key == pygame.K_LEFT:
                        print('left key still down')
                        self.animationStateManager.setState('run')
                        self.reverse = True
                    else:
                        print('no keys down')                        
                        
                if event.key == pygame.K_LEFT:
                    print('left key up')
                    
                    if event.key == pygame.K_RIGHT:
                        print('right key still down')
                        self.animationStateManager.setState('run')
                        self.reverse = False
                    else:
                        print('no keys down')
                    

            if event.type == pygame.KEYDOWN:
                print('key down')                                
                
                if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]:
                    print('both keys down')                 
                    self.animationRun.frame = 0
                    self.animationStateManager.setState('idle')
                    
                if keys[pygame.K_RIGHT]:
                    print('right key down')
                    self.animationIdle.frame = 0
                    self.reverse = False
                    self.animationStateManager.setState('run')
                    
                if keys[pygame.K_LEFT]:
                    print('left key down')
                    self.animationIdle.frame = 0
                    self.reverse = True
                    self.animationStateManager.setState('run')
        '''
                
    class AnimationStateManager:
        def __init__(self, currentState):
            self.currentState = currentState
        
        def getState(self):
            return self.currentState
        
        def setState(self, state):
            self.currentState = state
        
    class AnimationIdle:
        def __init__(self, display, sprites):
            self.display = display
            self.frame = 0
            self.animationCooldown = 125
            self.lastUpdate = pygame.time.get_ticks()
            self.sprites = sprites
            
        def run(self, rect, reverse):
            currentTime = pygame.time.get_ticks()
            
            if (currentTime - self.lastUpdate >= self.animationCooldown):
                self.frame += 1
                self.lastUpdate = currentTime
                if (self.frame >= len(self.sprites)):
                    self.frame = 0     
            
            if reverse == True:
                reverseSprite = pygame.transform.flip(self.sprites[self.frame], True, False)
                self.display.blit(reverseSprite, rect)
            else:
                self.display.blit(self.sprites[self.frame], rect)
            
    class AnimationRun:
        def __init__(self, display, sprites):
            self.display = display
            self.frame = 0
            self.animationCooldown = 125
            self.lastUpdate = pygame.time.get_ticks()
            self.sprites = sprites
            
        def run(self, rect, reverse):
            currentTime = pygame.time.get_ticks()
            
            if (currentTime - self.lastUpdate >= self.animationCooldown):
                self.frame += 1
                self.lastUpdate = currentTime
                if (self.frame >= len(self.sprites)):
                    self.frame = 0
                    
            if reverse == True:
                reverseSprite = pygame.transform.flip(self.sprites[self.frame], True, False)
                self.display.blit(reverseSprite, rect)
            else:
                self.display.blit(self.sprites[self.frame], rect)
               
if __name__ == '__main__':
    game = Game()
    game.mainLoop()