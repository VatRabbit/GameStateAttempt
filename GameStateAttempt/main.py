'''

TO ADD:
- enemy
- jump buffer
- variable jump height

ISSUES:
- jumping not consistent on different frame rates
- camera doesn't center on player correctly

'''

import pygame, time, player
from sprite_handler import sprite_handler
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
        pygame.display.set_caption('Crappy Platformer')
        self.display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))        
        
        # maybe set up a Time class?
        self.clock = pygame.time.Clock()
        self.dt = 0.0
        self.last_update = 0.0
          
        self.sprite_handler = sprite_handler()
        self.sprite_handler.load_sprites()

        self.player = player.Player(self.display, self.sprite_handler.player_idle, self.sprite_handler.player_run, self.sprite_handler.player_jump)
        # self.player.load_sprite_sheet()
        
        self.game_state_manager = self.Game_State_Manager('menu')  
        self.menu = self.Menu(self.display, self.game_state_manager)
        self.level = self.Level(self.display, self.game_state_manager, self.player, self.dt)
        self.states = {'level': self.level, 'menu': self.menu}
        
    def main_loop(self):
        while True:
            self.events = pygame.event.get() 
            for event in self.events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit() 
                    
            self.states[self.game_state_manager.get_state()].run(self.events, self.dt)
            
            self.render()            
                        
            self.timer()
            self.clock.tick(FPS)
           
    def timer(self):
        self.dt = time.time() - self.last_update
        self.last_update = time.time()
            
    def render(self):           
        self.states[self.game_state_manager.get_state()].render()
        self.scaled_display = pygame.transform.scale(self.display, (self.display.get_width() * DISPLAY_SCALE, self.display.get_height() * DISPLAY_SCALE))
        self.display.blit(self.scaled_display, (0,0))
        pygame.display.flip()        

    # I'll figure this out eventually...
    class Camera:
        def __init__(self):
            pass
        
    class Game_State_Manager:
        def __init__(self, current_state):
            self.current_state = current_state
    
        def set_state(self, state):
            self.current_state = state
        
        def get_state(self):
            return self.current_state
    
    class Level:
        def __init__(self, display, game_state_manager, player, dt):
            self.display = display
            self.game_state_manager = game_state_manager
            self.player = player
            self.collision_check_list = []            
            self.dt = dt
            self.true_offset_x = 0.0
            self.offset_x = 0
            self.new_state = True

            # y then x for these (it's sideways :/ )
            self.level_tiles = [
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,2,0,0,0,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,0,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            ]
            
            self.tile_rect_list = self.create_tile_rects()          
                    
        def run(self, events, dt):
            '''
            if self.new_state:
                self.true_offset_x = self.player.x - SCALED_WIDTH / 2 + 8
                self.offset_x = int(self.true_offset_x)
                self.new_state = False
                
            if self.player.velocity[0] != 0:
                self.true_offset_x += self.player.velocity[0]            
            
            '''
            '''
            if self.true_offset_x - self.offset_x != 0:                 
                 print(f"offset:      {self.offset_x}") 
                 self.offset_x = int(self.offset_x)
            '''

            # self.offset_x += (self.true_offset_x - self.offset_x + 12) / 12
            # print(f"true_offset: {self.true_offset_x}")
            # print(f"offset:      {self.offset_x}") 
            # print(f"player_x:    {self.player.x}")

            self.collision_check_list = self.check_collisions()               
            self.player.update(events, dt, self.collision_check_list)
            
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
        
        def check_collisions(self):
            check_list = []
            
            # take in the 3x4 grid surrounding the player to check for collisions
            for i in range(-1, 2):
                for j in range(-1, 3):
                    grid_y = int((self.player.x) / TILE_SIZE + i)
                    grid_x = int((self.player.y) / TILE_SIZE + j - 1)
                    
                    if 0 <= grid_x < len(self.level_tiles) and 0 <= grid_y < len(self.level_tiles[0]):
                         if self.level_tiles[grid_x][grid_y] == 1:                                
                              rect = pygame.Rect(grid_y * TILE_SIZE, grid_x * TILE_SIZE, TILE_SIZE, TILE_SIZE)    
                              check_list.append(rect)

            return check_list
        
        def render(self):
            self.display.fill((110, 140, 140))    
            self.render_tiles()
            self.show_collision_check_list()
            self.player.render(self.offset_x)
            
        def render_tiles(self):
            for rect in self.tile_rect_list:
                temp = rect.copy()
                temp.x -= self.offset_x                
                pygame.draw.rect(self.display, (100,100,250), temp, 2)        
                
        # displays the tiles in range for collision checks
        def show_collision_check_list(self):
            for rect in self.collision_check_list:
                rect.x -= self.offset_x
                pygame.draw.rect(self.display, (100,100,250), rect)  

        def reset(self):
            pass
            
    class Menu:
        def __init__(self, display, game_state_manager):
            self.display = display
            self.game_state_manager = game_state_manager
            
        def run(self, events, dt):            
            for event in events:             
                 if event.type == pygame.KEYDOWN:
                     self.game_state_manager.set_state('level')
                     
        def render(self):
            self.display.fill((140, 140, 110))
            
        def reset(self):
            pass
               
if __name__ == '__main__':
    game = Game()
    game.main_loop()