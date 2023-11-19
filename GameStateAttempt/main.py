import pygame, time, player
from sys import exit

DISPLAY_SCALE = 2
# 32 x 15 tile screen
SCREEN_WIDTH, SCREEN_HEIGHT = 512, 320   
SCALED_WIDTH = SCREEN_WIDTH / DISPLAY_SCALE
SCALED_HEIGHT = SCREEN_HEIGHT / DISPLAY_SCALE
SPEED = 125
FPS = 60
# 32 x 32 pixel tiles
TILE_SIZE = 32

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
            self.player.x = 2 * TILE_SIZE
            self.player.y = 4 * TILE_SIZE            
            ''' Wrong way :c
            self.level_tiles = [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 1, 1, 1]                
            ]  
            '''
            self.level_tiles = [
                [0,0,0,0,1],
                [0,0,0,0,1],
                [0,1,0,0,1],
                [0,0,0,0,1],
                [0,0,1,0,1],
                [0,0,1,0,1],
                [0,0,0,0,1],
                [0,0,0,0,1]
            ]

            self.tile_rect_list = self.create_tile_rects()
            
            # print(self.level_tiles)
            # print(self.level_tiles[][7])            
                    
        def run(self, events, dt):
            self.display.fill((110, 140, 140))
            check_tile_list = self.collision_check_list()   
            # print(check_tile_list)
            self.blit_tiles()
            self.player.update(events, dt)
            
        def create_tile_rects(self):
            rect_list = []    
        
            for x in range(len(self.level_tiles)):
                for y in range(len(self.level_tiles[0])):
                    if self.level_tiles[x][y] == 1:
                        # draw tile sprites here later instead of rect    
                        rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)    
                        rect_list.append(rect)
                        
            return rect_list
                        
        def blit_tiles(self):
            for rect in self.tile_rect_list:
                pygame.draw.rect(self.display, (100,100,250), rect, 2) 
                
        def collision_check_list(self):
            x = self.player.x / TILE_SIZE
            y = self.player.y / TILE_SIZE
            
            # print(self.player.x, self.player.y)
            
            check_list = []
            
            # take in the 3x3 grid surrounding the player to check for collisions
            for i in range(-1, 3):
                for j in range(-1, 3):
                    grid_x = int(x + i)
                    grid_y = int(y + j)
                    
                    if 0 <= grid_x < len(self.level_tiles) and 0 <= grid_y < len(self.level_tiles[0]):
                         if self.level_tiles[grid_x][grid_y] == 1:
                              # rect_grid = pygame.Rect(grid_x, grid_y, TILE_SIZE, TILE_SIZE)    
                              rect = pygame.Rect(grid_x * TILE_SIZE, grid_y * TILE_SIZE, TILE_SIZE, TILE_SIZE)    
                              check_list.append(rect)
                              # print(rect_grid)
                        
            print(grid_x, grid_y)
            print(check_list)
            return check_list
                
        def reset(self):
            pass    
                        
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