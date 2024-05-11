'''
TO ADD:
- jump buffer
- variable jump height
- more optimizion by only rendering visible tiles
- audio_handler class to load and handout music and sfx
- paralax scrolling bg 
- actual sprites some day
- use spritegroup functionality for enemies (self.kill() will remove sprites)
- look into spritecollide()
- event_handler methods for handling input
- limit RENDER_FPS so it doesn't start to bug from being as fast or faster than LOGIC_FPS

ISSUES:
- figure out perfect center on camera by drawing lines or something
'''

import pygame, time, player, level, menu, sprite_handler
from sys import exit

# this is an issue
DISPLAY_SCALE = 2

RENDER_FPS    = 90
LOGIC_FPS     = 120
MAP_FPS       = 120
TILE_SIZE     = 16
SCREEN_WIDTH  = 682
SCREEN_HEIGHT = 384
SCALED_WIDTH  = SCREEN_WIDTH / DISPLAY_SCALE
SCALED_HEIGHT = SCREEN_HEIGHT / DISPLAY_SCALE

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Crappy Platformer')
        self.display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))        
        
        self.render_clock = pygame.time.Clock()
        self.logic_clock  = pygame.time.Clock()        
        self.last_update  = time.time()
        self.last_logic   = time.time()
        self.last_render  = time.time()
        self.dt           = 0.0
        self.render_dt    = 0.0
        self.logic_dt     = 0.0
        self.events       = []  

        self.sprite_handler = sprite_handler.sprite_handler()
        self.sprite_handler.load_sprites(SCREEN_WIDTH, SCREEN_HEIGHT)   

        self.player = player.Player(self.display, self.sprite_handler.player_idle, self.sprite_handler.player_run, self.sprite_handler.player_jump)
                
        self.game_state_manager = self.Game_State_Manager('menu')  
        self.menu               = menu.Menu(self.display, self.game_state_manager)
        self.level              = level.Level(self.display, self.game_state_manager, self.player, TILE_SIZE, SCALED_WIDTH, SCREEN_WIDTH, SCREEN_HEIGHT)
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
                self.events.clear()             
              
            if self.render_dt >= 1.0 / RENDER_FPS:                
                self.render(self.display)             
                self.render_dt -= 1.0 / RENDER_FPS
                        
    def update_logic(self):
        self.last_logic = time.time()
        self.states[self.game_state_manager.get_state()].run(self.events, self.logic_dt, self.sprite_handler)  
                                      
    def render(self, display):  
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
               
if __name__ == '__main__':
    game = Game()
    game.main_loop()