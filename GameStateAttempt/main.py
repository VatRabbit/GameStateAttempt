'''
TO ADD:
- jump buffer
- variable jump height
- more optimizion by only rendering visible tiles
- sound class to load and handout music and sfx
- paralax scrolling bg 
- actual sprites some day
- use spritegroup functionality for enemies (self.kill() will remove sprites)
- look into spritecollide()
- event_handler methods for handling input
- limit RENDER_FPS so it doesn't start to bug from being as fast or faster than LOGIC_FPS

ISSUES:
- figure out perfect center on camera by drawing lines or something
'''

import pygame, time, player, enemy
from sprite_handler import sprite_handler
from sys import exit

RENDER_FPS    = 90
LOGIC_FPS     = 120
MAP_FPS       = 120
TILE_SIZE     = 16
DISPLAY_SCALE = 2
SCREEN_WIDTH  = 448
SCREEN_HEIGHT = 320
SCALED_WIDTH  = SCREEN_WIDTH / DISPLAY_SCALE
SCALED_HEIGHT = SCREEN_HEIGHT / DISPLAY_SCALE

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Crappy Platformer')
        self.display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))        
        
        self.render_clock = pygame.time.Clock()
        self.logic_clock  = pygame.time.Clock()
        self.dt           = 0.0
        self.render_dt    = 0.0
        self.logic_dt     = 0.0
        self.last_update  = time.time()
        self.last_logic   = time.time()
        self.last_render  = time.time()
        self.events       = []  

        self.sprite_handler = sprite_handler()
        self.sprite_handler.load_sprites()
        
        # self.animation_player_idle = self.sprite_handler.player_idle

        self.player = player.Player(self.display, self.sprite_handler.player_idle, self.sprite_handler.player_run, self.sprite_handler.player_jump)
                
        self.game_state_manager = self.Game_State_Manager('menu')  
        self.menu               = self.Menu(self.display, self.game_state_manager)
        self.level              = self.Level(self.display, self.game_state_manager, self.player, self.dt)
        self.states             = {'level': self.level, 'menu': self.menu}
        
    def main_loop(self):
        while True:
            self.events += pygame.event.get()
            for event in self.events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                    
            self.timer()    
            
            if self.logic_dt >= 1.0 / LOGIC_FPS:                            
                self.update_logic()       
                self.logic_dt -= 1.0 / LOGIC_FPS
                self.events = []               
              
            if self.render_dt >= 1.0 / RENDER_FPS:                
                self.render(self.render_dt, self.display)             
                self.render_dt -= 1.0 / RENDER_FPS
                        
    def update_logic(self):
        self.last_logic = time.time()
        self.states[self.game_state_manager.get_state()].run(self.events, self.logic_dt, self.sprite_handler)  
                                      
    def render(self, dt, display):  
        self.last_render = time.time()         
        self.states[self.game_state_manager.get_state()].render(self.render_dt, display)
        self.scaled_display = pygame.transform.scale(self.display, (display.get_width() * DISPLAY_SCALE, display.get_height() * DISPLAY_SCALE))
        display.blit(self.scaled_display, (0,0))
        pygame.display.flip()        

    def timer(self):
        current_time = time.time()
        self.dt = current_time - self.last_update
        self.last_update = current_time
        self.logic_dt  += self.logic_clock.tick()  / 1000.0
        self.render_dt += self.render_clock.tick() / 1000.0  
                
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
            self.enemy_group = pygame.sprite.Group()
            self.camera_follow_multiplyer = 10
            
            # y then x for these (it's sideways :/ )
            # currently a 28x10 map            
            self.tilemap = [
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,1],
                [1,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,1],
                [1,0,0,1,1,1,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,1,1,1,0,0,3,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,3,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            ]
            
        def run(self, events, dt, sprite_handler):
            for event in events:
                 if event.type == pygame.KEYUP:
                     if event.key == pygame.K_DELETE:
                          self.enemy_group.empty()                   
                          print('del')
                     
            if self.first_run:
                self.tilemap_rect_list = self.create_tile_rects(sprite_handler, self.display)    
                self.first_run = False                
            
            self.camera()              
            
            self.player.update(events, dt, self.tilemap)
            self.enemy_group.update(dt, self.tilemap, TILE_SIZE)
        
        def render(self, dt, display):
            display.fill((110, 140, 140))
            self.render_tiles()                       
                                
            for sprite in self.enemy_group:
                sprite.render(self.offset_x, dt)            
            self.enemy_group.draw(display)
            
            self.player.render(self.offset_x, dt, display)
            
        def render_tiles(self):
            for rect in self.tilemap_rect_list:
                temp = rect.copy()
                temp.x -= self.offset_x
                pygame.draw.rect(self.display, (100,100,250), temp, 2)
                
        # game window is 224px or 14 tiles wide.
        def camera(self):
            if self.new_state:
                self.true_offset_x = self.player.position[0] - SCALED_WIDTH / 2 + 8
                self.offset_x = int(self.true_offset_x)
                self.new_state = False
                
            if self.player.velocity[0] != 0:                
                self.true_offset_x += self.player.velocity[0]
                
            # set the offset for the camera. Subtract 0.5 (tiles) to center everything
            self.offset_x += (self.true_offset_x - self.offset_x) / self.camera_follow_multiplyer - 1
            
            if self.offset_x < 0:
                self.offset_x = 0
             
            elif self.offset_x > len(self.tilemap[0]) * TILE_SIZE - 224:
                self.offset_x  = len(self.tilemap[0]) * TILE_SIZE - 224
            
        def create_tile_rects(self, sprite_handler, display):
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
                        new_enemy = enemy.enemy(display, pos_x, pos_y, TILE_SIZE, sprite_handler.bunny_jump)
                        self.enemy_group.add(new_enemy)

            return rect_list
                
        def reset(self):
            pass
            
    class Menu:
        def __init__(self, display, game_state_manager):
            self.display = display
            self.game_state_manager = game_state_manager
            
        def run(self, events, dt, sprite_handler):
            for event in events:
                 if event.type == pygame.KEYDOWN:
                     self.game_state_manager.set_state('level')                     
            # print('running Menu')
                     
        def render(self, dt, display):
            display.fill((140, 140, 110))
            # print('rendering menu')
            
        def reset(self):
            pass
               
if __name__ == '__main__':
    game = Game()
    game.main_loop()