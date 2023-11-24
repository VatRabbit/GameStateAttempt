import pygame, time, player
from sys import exit

DISPLAY_SCALE = 2
SCREEN_WIDTH, SCREEN_HEIGHT = 448, 320
SCALED_WIDTH = SCREEN_WIDTH / DISPLAY_SCALE
SCALED_HEIGHT = SCREEN_HEIGHT / DISPLAY_SCALE
FPS = 60
TILE_SIZE = 16

class Game:
    def __init__(self):
        pygame.init()          
        self.display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Crappy Game')
        
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
            self.player.x = 0
            self.player.y = 0
            self.collision_check_list = []

            # y then x for these
            self.level_tiles = [
                [1,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,1,1,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,2,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,1,1,1,1],
                [1,0,0,1,1,1,0,0,0,0,1,1,1,1],
                [1,0,0,0,0,0,0,0,0,0,1,1,1,1],
                [1,0,0,0,0,0,0,0,0,0,1,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            ]

            self.tile_rect_list = self.create_tile_rects()          
                    
        def run(self, events, dt):
            self.collision_check_list = self.check_collisions()               
            self.player.update(events, dt, self.collision_check_list)
            self.render(events, dt, self .collision_check_list) 
            # self.player.collision_detected()
            self.player.render()
            
        def create_tile_rects(self):
            rect_list = []    
        
            for x in range(len(self.level_tiles)):
                for y in range(len(self.level_tiles[0])):
                    if self.level_tiles[x][y] == 1:
                        # draw tile sprites here later instead of rect    
                        rect = pygame.Rect(y * TILE_SIZE, x * TILE_SIZE, TILE_SIZE, TILE_SIZE)    
                        rect_list.append(rect)
                    # check for a spawn tile while we're at it :3
                    elif self.level_tiles[x][y] == 2:
                        self.player.x = y * TILE_SIZE
                        self.player.y = x * TILE_SIZE + TILE_SIZE 
                        
            return rect_list
                        
        def blit_tiles(self):
            for rect in self.tile_rect_list:
                pygame.draw.rect(self.display, (100,100,250), rect, 2) 
                                
        def check_collisions(self):                   
            check_list = []
            
            # take in the 3x3 grid surrounding the player to check for collisions
            for i in range(-1, 2):
                for j in range(-2, 3):
                    grid_y = int(self.player.x / TILE_SIZE + i)
                    grid_x = int(self.player.y / TILE_SIZE + j - 1)
                    
                    if 0 <= grid_x < len(self.level_tiles) and 0 <= grid_y < len(self.level_tiles[0]):
                         if self.level_tiles[grid_x][grid_y] == 1:                                
                              rect = pygame.Rect(grid_y * TILE_SIZE, grid_x * TILE_SIZE, TILE_SIZE, TILE_SIZE)    
                              check_list.append(rect)

            return check_list
                
        def reset(self):
            pass    
        
        def render(self, events, dt, check_list):
            self.display.fill((110, 140, 140))    
            self.blit_tiles()
            for tile in check_list:
                pygame.draw.rect(self.display, (100,100,250), tile)             
            
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