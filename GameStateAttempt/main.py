'''
TO ADD:
- enemy
- jump buffer
- variable jump height
- more optimizion by only rendering visible tiles
- stop camera scrolling at ends of map
- sound class to load and handout music and sfx
- paralax scrolling bg 
- actual sprites some day

ISSUES:
- jumping not consistent on different frame rates
- camera doesn't center on player correctly
- maybe have more delta time issue
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
           
    def timer(self):
        self.dt = time.time() - self.last_update
        self.last_update = time.time()
        self.clock.tick(FPS)
            
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
            self.new_state = True
            self.true_offset_x = 0.0
            self.offset_x = 0 
            self.first_run = True
            self.tilemap_rect_list = []            
            self.enemy_list = []
            
            # y then x for these (it's sideways :/ )
            # currently a 10x28 map
            self.tilemap = [
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,1],
                [1,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,3,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            ]
            
        def run(self, events, dt):    
            if self.first_run:
                self.tilemap_rect_list = self.create_tile_rects(dt)    
                self.first_run = False                
            
            self.camera()              
            
            self.player.update(events, dt, self.tilemap)
            for enemy in self.enemy_list:
                enemy.update(dt, self.tilemap, TILE_SIZE)

        def camera(self):
            if self.new_state:
                self.true_offset_x = self.player.position[0] - SCALED_WIDTH / 2 + 8
                self.offset_x = int(self.true_offset_x)
                self.new_state = False
                
            if self.player.velocity[0] != 0:
                self.true_offset_x += self.player.velocity[0]

            # set the offset for the camera. Subtract 0.5 (tiles) to center everything
            self.offset_x += (self.true_offset_x - self.offset_x) / 12 - 0.5
            
        def create_tile_rects(self, dt):
            rect_list = []
        
            for x in range(len(self.tilemap)):
                for y in range(len(self.tilemap[0])):
                    if self.tilemap[x][y] == 1:                        
                        rect = pygame.Rect(y * TILE_SIZE, x * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                        rect_list.append(rect)
                    
                    # check for player spawn tile
                    elif self.tilemap[x][y] == 2:
                        self.player.position[0] = y * TILE_SIZE
                        self.player.position[1] = x * TILE_SIZE + TILE_SIZE
                        
                    # check for enemies! 
                    elif self.tilemap[x][y] == 3:  
                        # print("enemy found!")
                        pos_x = y * TILE_SIZE
                        pos_y = x * TILE_SIZE                        
                        new_enemy = enemy.enemy(self.display, pos_x, pos_y, dt, self.tilemap_rect_list)
                        self.enemy_list.append(new_enemy)

            return rect_list
        
        def render(self):
            self.display.fill((110, 140, 140))
            self.render_tiles()                     
            for enemy in self.enemy_list:
                enemy.render(self.offset_x)
            self.player.render(self.offset_x)
            
        def render_tiles(self):
            for rect in self.tilemap_rect_list:
                temp = rect.copy()
                temp.x -= self.offset_x
                pygame.draw.rect(self.display, (100,100,250), temp, 2)
                
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