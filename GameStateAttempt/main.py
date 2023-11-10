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
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    self.gameStateManager.setState('level')                    

            self.states[self.gameStateManager.getState()].run()
            self.display.fill('black')
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
        
    def run(self):
        self.display.fill('blue')
        
class Level:
    def __init__(self, display, gameStateManager, player):
        self.display = display
        self.gameStateManager = gameStateManager
        self.player = player
        
    def run(self):
        self.display.fill('red')
        self.player.update()
        
class Player(pygame.sprite.Sprite):
    def __init__(self, display):
        super().__init__()
        self.display = display  
        # 33x32p x 6 spritesheet
        self.spriteSheet = pygame.image.load('player/player.png').convert_alpha()

    def update(self):
        pass
        
if __name__ == '__main__':
    game = Game()
    game.mainLoop()