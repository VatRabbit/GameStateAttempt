'''

TO ADD:
- enemy
- jump buffer
- variable jump height
- more optimizion by only rendering visible tiles

ISSUES:
- jumping not consistent on different frame rates
- camera doesn't center on player correctly

'''

import pygame, time, player, enemy
from sprite_handler import sprite_handler
from sys import exit

DISPLAY_SCALE = 2
SCREEN_WIDTH, SCREEN_HEIGHT = 448, 320
SCALED_WIDTH = SCREEN_WIDTH / DISPLAY_SCALE
SCALED_HEIGHT = SCREEN_HEIGHT / DISPLAY_SCALE
FPS = 60
TILE_SIZE = 16
DELTA_TIME = 0.0

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Crappy Platformer')
        self.display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))        
        
        self.clock = pygame.time.Clock()
        self.dt = 0.0
        self.last_update = 0.0
          
        self.sprite_handler = sprite_handler()
        self.sprite_handler.load_sprites()

        self.player = player.Player(self.display, self.sprite_handler.player_idle, self.sprite_handler.player_run, self.sprite_handler.player_jump)
                
        self.game_state_manager = self.Game_State_Manager('menu')  
        self.menu  = self.Menu(self.display, self.game_state_manager)
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
        DELTA_TIME = self.dt
        print(f"DELTA_TIME : {DELTA_TIME}")
        self.last_update = time.time()
        # print(f"main dt : {self.dt}")
            
    def render(self):           
        self.states[self.game_state_manager.get_state()].render()
        self.scaled_display = pygame.transform.scale(self.display, (self.display.get_width() * DISPLAY_SCALE, self.display.get_height() * DISPLAY_SCALE))
        self.display.blit(self.scaled_display, (0,0))
        pygame.display.flip()        
        
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
            self.new_state = True
            self.true_offset_x = 0.0
            self.offset_x = 0 
            self.first_run = True
            self.tile_rect_list = []            
            self.enemy_list = []
            
            # y then x for these (it's sideways :/ )
            self.level_tiles = [
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,1],
                [1,0,0,1,1,1,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            ]
            
        def run(self, events, dt):    
            if self.first_run:
                self.tile_rect_list = self.create_tile_rects()    
                self.first_run = False
            self.camera()
            self.collision_check_list = self.check_collisions()               
            self.player.update(events, dt, self.collision_check_list)
            # self.player.sign_off()
            for enemy in self.enemy_list:
                enemy.update()
                # enemy.sign_off()
                
            # print(f"main dt : {self.dt}")
            
        def camera(self):
            if self.new_state:
                self.true_offset_x = self.player.position[0] - SCALED_WIDTH / 2 + 8
                self.offset_x = int(self.true_offset_x)
                self.new_state = False
                
            if self.player.velocity[0] != 0:
                self.true_offset_x += self.player.velocity[0]

            # set the offset for the camera. Subtract 0.5 (tiles) to center everything
            self.offset_x += (self.true_offset_x - self.offset_x) / 12 - 0.5
            
        def create_tile_rects(self):
            rect_list = []
        
            for x in range(len(self.level_tiles)):
                for y in range(len(self.level_tiles[0])):
                    if self.level_tiles[x][y] == 1:
                        # draw tile sprites here later instead of rect
                        rect = pygame.Rect(y * TILE_SIZE, x * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                        rect_list.append(rect)
                    
                    # check for player spawn tile
                    elif self.level_tiles[x][y] == 2:
                        self.player.position[0] = y * TILE_SIZE
                        self.player.position[1] = x * TILE_SIZE + TILE_SIZE
                        
                    # check for enemies! 
                    elif self.level_tiles[x][y] == 3:  
                        print("enemy found!")
                        pos_x = y * TILE_SIZE
                        pos_y = x * TILE_SIZE                        
                        new_enemy = enemy.enemy(self.display, pos_x, pos_y, self.dt)
                        self.enemy_list.append(new_enemy)

            return rect_list
        
        # take in the 3x4 grid surrounding the player to check for collisions
        def check_collisions(self):
            check_list = []
            for i in range(-1, 2):
                for j in range(-1, 3):
                    grid_y = int((self.player.position[0]) / TILE_SIZE + i)
                    grid_x = int((self.player.position[1]) / TILE_SIZE + j - 1)
                    
                    if 0 <= grid_x < len(self.level_tiles) and 0 <= grid_y < len(self.level_tiles[0]):
                         if self.level_tiles[grid_x][grid_y] == 1:
                              rect = pygame.Rect(grid_y * TILE_SIZE, grid_x * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                              check_list.append(rect)

            return check_list
        
        def render(self):
            self.display.fill((110, 140, 140))
            self.render_tiles()
            self.show_collision_check_list()            
            for enemy in self.enemy_list:
                enemy.render(self.offset_x)
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