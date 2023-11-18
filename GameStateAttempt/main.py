import pygame, time, player
from sys import exit

DISPLAY_SCALE = 2
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 300  
SCALED_WIDTH = SCREEN_WIDTH / DISPLAY_SCALE
SCALED_HEIGHT = SCREEN_HEIGHT / DISPLAY_SCALE
SPEED = 125
FPS = 60

class Game:
    def __init__(self):
        pygame.init()          
        self.display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        
        self.player = player.Player(self.display)
        
        self.game_state_manager = self.Game_State_Manager('menu')  
        self.menu = self.Menu(self.display, self.game_state_manager)         
        self.level = self.Level(self.display, self.game_state_manager, self.player)         
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
            
            self.states[self.game_state_manager.get_state()].run(self.events, self.dt) 
            
            scaled_display = pygame.transform.scale(self.display, (self.display.get_width() * DISPLAY_SCALE, self.display.get_height() * DISPLAY_SCALE))
            self.display.blit(scaled_display, (0,0))
            pygame.display.flip()            
            
            self.clock.tick(FPS)
    
    class Game_State_Manager:
        def __init__(self, current_state):
            self.current_state = current_state
    
        def set_state(self, state):
            self.current_state = state
        
        def get_state(self):
            return self.current_state
    
    class Level:
        def __init__(self, display, game_state_manager, player):
            self.display = display
            self.game_state_manager = game_state_manager
            self.player = player
            self.platform = pygame.Rect(SCALED_WIDTH // 2, SCALED_HEIGHT // 1.75, 40 / DISPLAY_SCALE, 40 / DISPLAY_SCALE) 
        
        def run(self, events, dt):            
            self.display.fill((110, 140, 140))
            pygame.draw.rect(self.display, (100,100,250), self.player.collision_rect)
            pygame.draw.line(self.display, (100,100,250), (290,0),(290,290), 1)
            if self.platform.colliderect(self.player.rect):
                pygame.draw.rect(self.display, (100, 200, 200), self.platform)
            else:
                pygame.draw.rect(self.display, (200, 100, 200), self.platform)
            self.player.update(events, dt)

    class Menu:
        def __init__(self, display, game_state_manager):
            self.display = display
            self.game_state_manager = game_state_manager
        
        def run(self, events, dt):        
            self.display.fill((140, 140, 110))
            for event in events:             
                 if event.type == pygame.KEYDOWN:
                     self.game_state_manager.set_state('level')
               
if __name__ == '__main__':
    game = Game()
    game.mainLoop()