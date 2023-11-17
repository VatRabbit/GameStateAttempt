import pygame, time
from sys import exit

DISPLAY_SCALE = 2
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 200  
SCALED_WIDTH = SCREEN_WIDTH // DISPLAY_SCALE
SCALED_HEIGHT = SCREEN_HEIGHT // DISPLAY_SCALE
SPEED = 125
FPS = 60

class Game:
    def __init__(self):
        pygame.init()          
        self.display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        
        self.player = Player(self.display)
        
        self.gameStateManager = self.GameStateManager('menu')  
        self.menu = self.Menu(self.display, self.gameStateManager)         
        self.level = self.Level(self.display, self.gameStateManager, self.player)         
        self.states = {'level': self.level, 'menu': self.menu}   
        
        self.dt = 0.0
        
    def mainLoop(self):
        last_update = 0.0
        
        while True:   
            self.events = pygame.event.get() 
            for event in self.events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                    
            self.display.fill('black')
            
            self.dt = time.time() - last_update
            last_update = time.time()
            
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
            self.display.fill((140, 140, 110))
            for event in events:             
                 if event.type == pygame.KEYDOWN:
                     self.gameStateManager.setState('level')
        
    class Level:
        def __init__(self, display, gameStateManager, player):
            self.display = display
            self.gameStateManager = gameStateManager
            self.player = player
        
        def run(self, events):
            self.display.fill((110, 140, 140))
            self.player.update(events)
        
class Player(pygame.sprite.Sprite):
    def __init__(self, display):
        super().__init__()
        self.display = display
        self.loadSpriteSheet()       
        
        self.animationStateManager = self.AnimationStateManager('idle')
        self.animationIdle = self.AnimationIdle(display, self.spriteListIdle)
        self.animationRun = self.AnimationRun(display, self.spriteListRun)
        self.animationJump = self.AnimationJump(display, self.spriteListJump)
        self.animationStates = {'idle': self.animationIdle, 'run': self.animationRun, 'jump': self.animationJump}
        
        self.sprites = self.spriteListIdle
        self.spriteRect = self.sprites[0].get_rect(bottomleft = (20,100))
        
        self.reverse = False
        self.gravity = 0     
        self.x, self.y = 50.0 / DISPLAY_SCALE, 200.0 / DISPLAY_SCALE

    def update(self, events):                  
        self.handleInput(events, game.dt)   
        self.apply_gravity(game.dt) 
        self.update_player_rect() 
        self.animationStates[self.animationStateManager.getState()].run(self.spriteRect, self.reverse)
        
    def printSprites(self):
        for i in range(len(self.animationRun)):
            self.display.blit(self.animationRun[i], (50*i,50))
            
    def update_player_rect(self):
        if self.x < 0:
            self.x = 0
        elif self.x + self.spriteRect.width > SCALED_WIDTH:
            self.x = SCALED_WIDTH - self.spriteRect.width

        self.spriteRect.bottomleft = (self.x,self.y)
           
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
        
    def apply_gravity(self, dt):
        self.y += self.gravity * dt
        
        if self.y < SCREEN_HEIGHT / DISPLAY_SCALE:
            if self.gravity < 1000: # terminal velocity
                self.gravity += 1000 * dt   # acceleration due to gravity
            
        if self.y > SCREEN_HEIGHT / DISPLAY_SCALE:
            self.y = SCREEN_HEIGHT / DISPLAY_SCALE
                
    def handleInput(self, events, dt):
        keys = pygame.key.get_pressed() 
        
        if self.y == SCREEN_HEIGHT / DISPLAY_SCALE:
             for event in events:
                 if event.type == pygame.KEYDOWN:
                     if event.key == pygame.K_SPACE:                         
                         self.gravity = -300                

        if keys[pygame.K_LEFT] == True and keys[pygame.K_RIGHT] == True:
            self.animationStateManager.setState('idle')
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.type == pygame.K_LEFT or event.type == pygame.K_RIGHT:
                        self.animationIdle.frame = 0
                    
        elif keys[pygame.K_LEFT] == True:
            self.animationStateManager.setState('run')
            self.reverse = True
            self.x -= SPEED * dt
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.animationRun.frame = 0                                            
                        
        elif keys[pygame.K_RIGHT] == True:
            self.animationStateManager.setState('run')
            self.reverse = False
            self.x += SPEED * dt
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
                        
        if self.y < SCREEN_HEIGHT / DISPLAY_SCALE:
            self.animationStateManager.setState('jump')
        
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
            self.animationCooldown = 75
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
                
    class AnimationJump:
        def __init__(self, display, sprites):
            self.display = display
            self.sprites = sprites
            self.frame = 0
            
        def run(self, rect, reverse):                    
            if reverse == True:
                reverseSprite = pygame.transform.flip(self.sprites[self.frame], True, False)
                self.display.blit(reverseSprite, rect)
            else:
                self.display.blit(self.sprites[self.frame], rect)   
               
if __name__ == '__main__':
    game = Game()
    game.mainLoop()