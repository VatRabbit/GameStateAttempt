'''
TO ADD:
- jump buffer
- player should be able to run accross 1 tile gaps without falling 
- player acceleration and deceleration
- need to apply rendering dt to animation states for stability across framerates?

ISSUES:
- Jumping doesn't work with delta time because it's missing acceleration increments when it misses frames

MISC:
- Swap out for global variables. They're better for values that can be tweaked
'''

JUMP                 = -3.5
GRAVITY              = 12
SPEED                = 150
ANIMATION_SPEED_RUN  = 14
ANIMATION_SPEED_IDLE = 8

import pygame

from main import TILE_SIZE

class Player(pygame.sprite.Sprite):
    def __init__(self, display, sprites_idle, sprites_run, sprites_jump):
        super().__init__()
        self.display = display       
                
        self.animation_idle          = self.Animation_Idle(sprites_idle)
        self.animation_run           = self.Animation_Run(sprites_run)
        self.animation_jump          = self.Animation_Jump(sprites_jump)        
        self.animation_state_manager = self.Animation_State_Manager('idle')
        self.animation_states        = {'idle': self.animation_idle, 'run': self.animation_run, 'jump': self.animation_jump}        
         
        self.image          = pygame.Surface((32,32))
        self.rect           = pygame.Rect(0,0, 32,32)
        self.collision_rect = pygame.Rect(0,0,  9,20)
        self.collision_list = []
        
        # handles which direction the sprite should be facing during animations
        self.reverse = False
        
        # velocity[0] = left/right, velocity[1] = up/down
        self.velocity = [0,0]
        #position[0] = x axis, position[1] = y axis
        self.position = [0,0]
        
        self.last_y              = 0.0        
        self.terminal_velocity   = 5
        self.coyote_limit        = 0.1
        self.coyote_time         = 0.0
        self.jump_buffer         = 0.0
        self.jump_height_counter = 0.0
        self.double_jump_ready   = False
        self.is_grounded         = False
                
    def check_grounded(self):
        tollerance = 1
        self.is_grounded = False
        
        for rect in self.collision_list:
            if rect.colliderect(self.collision_rect) and self.velocity[1] >= 0:
                self.is_grounded = True
                self.velocity[1] = tollerance
                self.double_jump_ready = True
                break

    def coyote_counter(self, dt):
        if self.is_grounded == False:
            self.coyote_time += dt
        else:
            self.coyote_time = 0.0

    def update(self, events, dt, tilemap):
        self.handle_input(events, dt)
        self.collision_list = self.check_collisions(tilemap)
        
        # handle self.position[0], left/right movement and check left/right collisions 
        self.update_x_velocity()
        self.handle_x_collisions()
                
        # handle self.position[1], up/down movement and check for up/down collisions
        self.apply_gravity(dt)
        self.update_y_velocity()
        self.check_grounded()
        self.handle_y_collisions()
          
        self.update_player_rect()
        self.coyote_counter(dt)
        
    def render(self, offset_x, dt, display):
        self.rect.x -= offset_x
        self.show_collision_check_list(offset_x)
        self.image = self.animation_states[self.animation_state_manager.get_state()].run(self.reverse, dt)
        display.blit(self.image, self.rect)
        
    def update_x_velocity(self):
        self.position[0] += self.velocity[0]
        self.collision_rect.left = self.position[0]
        
    def update_y_velocity(self):
        self.position[1] += self.velocity[1]
        self.collision_rect.bottom = self.position[1]
        
    def apply_gravity(self, dt):         
         self.velocity[1] += GRAVITY * dt    
         if self.velocity[1] > self.terminal_velocity:
             self.velocity[1] = self.terminal_velocity

    def update_player_rect(self):
        self.rect.midbottom = self.collision_rect.midbottom
     
    def check_collisions(self, tilemap):
        check_list = []
        for i in range(-1, 2):
            for j in range(-2, 2):
                grid_x = int((self.position[0]) / TILE_SIZE + i)
                grid_y = int((self.position[1]) / TILE_SIZE + j)
                  
                if 0 <= grid_y < len(tilemap) and 0 <= grid_x < len(tilemap[0]):
                     if tilemap[grid_y][grid_x] == 1:
                          rect = pygame.Rect(grid_x * TILE_SIZE, grid_y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                          check_list.append(rect)
                          
        return check_list
    
    # displays the tiles in range for collision checks
    def show_collision_check_list(self, offset_x):
        for rect in self.collision_list:
            rect.x -= offset_x
            pygame.draw.rect(self.display, (100,100,250), rect)

    def handle_x_collisions(self):
        # max of 8
        tollerance = 8
        
        for rect in self.collision_list:
            if rect.colliderect(self.collision_rect):
                # check for left collision first
                if self.collision_rect.left - tollerance <= rect.right <= self.collision_rect.left + tollerance:
                    self.position[0] = rect.right
                    self.collision_rect.left = self.position[0]
                    self.velocity[0] = 0

                # check for right collision next
                elif self.collision_rect.right + tollerance >= rect.left >= self.collision_rect.right - tollerance:
                    self.position[0] = rect.left - self.collision_rect.width 
                    self.collision_rect.left = self.position[0]
                    self.velocity[0] = 0
                
    def handle_y_collisions(self):
        
        tollerance = 8
        
        for rect in self.collision_list:
            if rect.colliderect(self.collision_rect):                                
                if self.collision_rect.bottom + tollerance >= rect.top >= self.collision_rect.bottom - tollerance:
                    self.position[1] = rect.top
                    self.collision_rect.bottom = self.position[1]    
                
                elif self.collision_rect.top - tollerance <= rect.bottom <= self.collision_rect.top + tollerance:                    
                    self.position[1] = rect.bottom + self.collision_rect.height
                    self.collision_rect.bottom = self.position[1]       
                    self.velocity[1] = 0
        
    def handle_input(self, events, dt):
        keys = pygame.key.get_pressed() 

        if self.is_grounded or self.coyote_time <= self.coyote_limit:
             for event in events:
                 if event.type == pygame.KEYDOWN:
                     if event.key == pygame.K_SPACE:
                         self.velocity[1] = JUMP
                         
        '''
        elif self.double_jump_ready == True:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.velocity[1] = JUMP
                        self.double_jump_ready = False
        '''
                        
        if keys[pygame.K_LEFT] == True and keys[pygame.K_RIGHT] == True:
            self.animation_state_manager.set_state('idle')
            self.velocity[0] = 0

            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.type == pygame.K_LEFT or event.type == pygame.K_RIGHT:
                        self.animationIdle.frame = 0
                    
        elif keys[pygame.K_LEFT] == True:
            self.animation_state_manager.set_state('run')
            self.reverse = True
            self.velocity[0] = -SPEED * dt
            
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.animation_run.frame = 0
                        
        elif keys[pygame.K_RIGHT] == True:
            self.animation_state_manager.set_state('run')
            self.reverse = False
            self.velocity[0] = SPEED * dt
            
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.animation_run.frame = 0
            
        elif keys[pygame.K_LEFT] == False and keys[pygame.K_RIGHT] == False:
            self.animation_state_manager.set_state('idle')
            self.velocity[0] = 0
            
            for event in events:
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.animation_idle.frame = 0
                        
        if self.is_grounded == False:
            self.animation_state_manager.set_state('jump')
                
    class Animation_State_Manager:
        def __init__(self, current_state):
            self.current_state = current_state
        
        def get_state(self):
            return self.current_state
        
        def set_state(self, state):
            self.current_state = state
                    
    class Animation_Idle:
        def __init__(self, sprites):            
            self.sprites     = sprites
            self.true_frame  = 0.0
            self.frame       = 0                                    
            
        def run(self, reverse, dt):
            self.true_frame += dt * ANIMATION_SPEED_IDLE
            
            if self.true_frame >= 1:                
                self.frame += 1
                self.true_frame -= 1
                if self.frame > len(self.sprites) - 1:
                    self.frame = 0
                    
            if reverse:
                reverse_sprite = pygame.transform.flip(self.sprites[self.frame], True, False)
                return reverse_sprite                
            else:
                return self.sprites[self.frame]
                
    class Animation_Jump:
        def __init__(self, sprites):
            self.sprites     = sprites
            
        def run(self, reverse, dt):                    
            if reverse:
                reverse_sprite = pygame.transform.flip(self.sprites[0], True, False)
                return reverse_sprite
            else:
                return self.sprites[0]
                
    class Animation_Run:
        def __init__(self, sprites):
            self.sprites     = sprites
            self.true_frame  = 0.0
            self.frame       = 0  
            
        def run(self, reverse, dt):
            self.true_frame += dt * ANIMATION_SPEED_RUN
            
            if self.true_frame >= 1:                
                self.frame += 1     
                self.true_frame -= 1
                if self.frame > len(self.sprites) - 1:
                    self.frame = 0
                    
            if reverse:
                reverse_sprite = pygame.transform.flip(self.sprites[self.frame], True, False)
                return reverse_sprite
            else:
                return self.sprites[self.frame]

if __name__ == '__main__':
    pass