'''
TO ADD:
- double jump
- scrolling level
- camera
- enemy
- jump buffer
- variable jump height
'''

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
        pygame.display.set_caption('Crappy Platformer')
        self.dt = 0.0
               
        self.camera = self.Camera(self.display)
        self.player = player.Player(self.display)
        
        self.game_state_manager = self.Game_State_Manager('menu')  
        self.menu = self.Menu(self.display, self.game_state_manager, self.camera)
        self.level = self.Level(self.display, self.game_state_manager, self.player, self.camera, self.dt)
        self.states = {'level': self.level, 'menu': self.menu}
        self.last_update = 0.0
        
    def mainLoop(self):
        while True:
            self.events = pygame.event.get() 
            for event in self.events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                    
            self.display.fill('black')        
            self.timer()
            self.states[self.game_state_manager.get_state()].run(self.events, self.dt)             
            self.render()
            self.clock.tick(FPS)
            
    def timer(self):
        self.dt = time.time() - self.last_update
        self.last_update = time.time()
        # print(self.dt)
            
    def render(self):
        scaled_display = pygame.transform.scale(self.display, (self.display.get_width() * DISPLAY_SCALE, self.display.get_height() * DISPLAY_SCALE))
        self.display.blit(scaled_display, (0,0))
        pygame.display.flip()        

    class Camera:
        def __init__(self, display):
            display = display
            self.x = 0.0
            self.y = 0.0
                        
        def get_x(self):
            return self.x
        def add_x(self, x):
            self.x += x
            
        def get_y(self):
            return self.y
        def add_y(self, y):
            self.y += y            
    
    class Game_State_Manager:
        def __init__(self, current_state):
            self.current_state = current_state
    
        def set_state(self, state):
            self.current_state = state
        
        def get_state(self):
            return self.current_state
    
    class Level:
        def __init__(self, display, game_state_manager, player, camera, dt):
            self.display = display
            self.game_state_manager = game_state_manager
            self.player = player
            self.player.x = 0
            self.player.y = 0
            self.collision_check_list = []
            self.camera = camera
            self.dt = dt

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
            self.handle_input(dt)
            self.update_tile_rects()
            self.collision_check_list = self.check_collisions()               
            self.player.update(events, dt, self.collision_check_list)
            self.render()             
            
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

        def update_tile_rects(self):
            rect_list = []
            cam_x = self.camera.get_x()
            cam_y = self.camera.get_y()
        
            for x in range(len(self.level_tiles)):
                for y in range(len(self.level_tiles[0])):
                    if self.level_tiles[x][y] == 1:
                        # draw tile sprites here later instead of rect
                        rect = pygame.Rect(y * TILE_SIZE + cam_x, x * TILE_SIZE + cam_y, TILE_SIZE, TILE_SIZE)
                        rect_list.append(rect)                 
                        
            self.tile_rect_list = rect_list
                                
        def check_collisions(self):
            check_list = []
            
            # take in the 3x3 grid surrounding the player to check for collisions
            for i in range(-1, 2):
                for j in range(-2, 3):
                    grid_y = int((self.player.x - self.camera.get_x()) / TILE_SIZE + i)
                    grid_x = int((self.player.y - self.camera.get_y()) / TILE_SIZE + j - 1)
                    
                    if 0 <= grid_x < len(self.level_tiles) and 0 <= grid_y < len(self.level_tiles[0]):
                         if self.level_tiles[grid_x][grid_y] == 1:                                
                              rect = pygame.Rect(grid_y * TILE_SIZE + self.camera.get_x(), grid_x * TILE_SIZE + self.camera.get_y(), TILE_SIZE, TILE_SIZE)    
                              check_list.append(rect)

            return check_list
        
        def show_collision_check_list(self):
            for rect in self.collision_check_list:
                pygame.draw.rect(self.display, (100,100,250), rect)
                
        def reset(self):
            pass    
        
        def handle_input(self, dt):
            keys = pygame.key.get_pressed()
            
            if keys[pygame.K_LCTRL] == True:
                # print('left ctrl down. Adding ', 100 * dt)
                self.camera.add_x(100 * dt)
                self.player.x += 100 * dt
                
            if keys[pygame.K_LALT] == True:
                # print('left alt down. Adding ', -100 * dt)
                self.camera.add_x(-100 * dt)
                self.player.x += -100 * dt
                
            # print(self.camera.get_x())
            # print(self.dt)
        
        def render(self):
            self.display.fill((110, 140, 140))    
            for rect in self.tile_rect_list:
                pygame.draw.rect(self.display, (100,100,250), rect, 2)    

            self.show_collision_check_list()
            self.player.render()
            
    class Menu:
        def __init__(self, display, game_state_manager, camera):
            self.display = display
            self.game_state_manager = game_state_manager
            self.camera = camera
        
        def run(self, events, dt):
            self.display.fill((140, 140, 110))
            for event in events:             
                 if event.type == pygame.KEYDOWN:
                     self.game_state_manager.set_state('level')
               
if __name__ == '__main__':
    game = Game()
    game.mainLoop()