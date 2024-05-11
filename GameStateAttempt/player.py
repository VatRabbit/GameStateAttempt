'''
TO ADD:
- jump buffer
- if player has been running for x time, their top speed can increase
- need to apply rendering dt to animation states for stability across framerates?

ISSUES:
- Player shouldn't activate jumping animation unitl their fall rate reaches a certain value?
'''

JUMP                 = -3.5
GRAVITY              = 10
TERMINAL_VELOCITY    = 5
COYOTE_LIMIT         = 0.1
ACCELERATION         = 3
MAX_VELOCITY         = 1.5
ANIMATION_SPEED_RUN  = 14
ANIMATION_SPEED_IDLE = 8
JUMP_BUFFER_LIMIT    = 0.15

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
        self.velocity     = [0,0]
        self.position     = [0,0]
        
        self.last_y              = 0.0        
        
        self.coyote_time         = 0.0
        self.jump_buffer         = 1.0
        self.jump_height_counter = 0.0
        self.double_jump_ready   = False
        self.is_grounded         = False

        self.space_bar_released  = True

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

    def update_player_rect(self):
        self.rect.midbottom = self.collision_rect.midbottom
        
    def apply_gravity(self, dt):
         self.velocity[1] += GRAVITY * dt    
         if self.velocity[1] > TERMINAL_VELOCITY:
             self.velocity[1] = TERMINAL_VELOCITY
             
    def coyote_counter(self, dt):
        if self.is_grounded == False:
            self.coyote_time += dt
        else:
            self.coyote_time = 0.0
     
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
    
    def check_grounded(self):
        tollerance = 1
        self.is_grounded = False
        
        for rect in self.collision_list:
            if rect.colliderect(self.collision_rect) and self.velocity[1] >= 0:
                self.is_grounded = True
                self.velocity[1] = tollerance
                self.double_jump_ready = True
                break

    # displays the tiles in range for collision checks
    def show_collision_check_list(self, offset_x):
        for rect in self.collision_list:
            rect.x -= offset_x
            pygame.draw.rect(self.display, (100,100,250), rect)

    def handle_x_collisions(self):
        # max of 8
        tollerance = 8
        # this will help player to run over 1-tile gaps
        y_tollerance = 8
        
        for rect in self.collision_list:
            if rect.colliderect(self.collision_rect):
                # check for left collision first
                # also fudge the y a bit
                if self.collision_rect.left - tollerance <= rect.right <= self.collision_rect.left + tollerance:
                    if rect.top < self.collision_rect.bottom < rect.top + y_tollerance:                        
                        self.position[1] = rect.top 
                    else:
                        self.position[0] = rect.right
                        self.collision_rect.left = self.position[0]
                        self.velocity[0] = 0

                # check for right collision next
                # also fudge the y a bit        
                elif self.collision_rect.right + tollerance >= rect.left >= self.collision_rect.right - tollerance:                    
                    if rect.top < self.collision_rect.bottom < rect.top + y_tollerance:                        
                        self.position[1] = rect.top 
                    else:
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
    
    def update_x_velocity(self):
        self.position[0] += self.velocity[0]
        self.collision_rect.left = self.position[0]
        
    def update_y_velocity(self):
        self.position[1] += self.velocity[1]
        self.collision_rect.bottom = self.position[1]
        
    def handle_input(self, events, dt):
        keys = pygame.key.get_pressed() 
        
        # Handles jumping        
        for event in events:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.space_bar_released = True
                    
        if self.space_bar_released and keys[pygame.K_SPACE] == True:            
            self.jump_buffer = 0
            self.space_bar_released = False
        
        if self.jump_buffer < JUMP_BUFFER_LIMIT:            
            if self.is_grounded or self.coyote_time < COYOTE_LIMIT:
                self.velocity[1] = JUMP
                self.jump_buffer += 1
                self.coyote_time += 1           
        
        if self.jump_buffer < 0.15:
            self.jump_buffer += dt
        else:
            self.jump_buffer = 0.15
                         
        '''
        elif self.double_jump_ready == True:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.velocity[1] = JUMP
                        self.double_jump_ready = False
        '''
                        
        # Check if the player is holding left and right at the same time
        if keys[pygame.K_LEFT] == True and keys[pygame.K_RIGHT] == True:
            self.animation_state_manager.set_state('idle')
            if self.velocity[0] > 0:
                self.velocity[0] -= ACCELERATION * dt
                if self.velocity[0] < 0:
                    self.velocity[0] = 0
            elif self.velocity[0] < 0:
                self.velocity[0] += ACCELERATION * dt
                if self.velocity[0] > 0:
                    self.velocity[0] = 0

            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.type == pygame.K_LEFT or event.type == pygame.K_RIGHT:
                        self.animationIdle.frame = 0
                    
        # Check for left key down
        elif keys[pygame.K_LEFT] == True:
            self.animation_state_manager.set_state('run')
            self.reverse = True
            self.velocity[0] -= ACCELERATION * dt
            if self.velocity[0] > 0:
                self.velocity[0] -= ACCELERATION * dt
            if self.velocity[0] < -MAX_VELOCITY:
                self.velocity[0] = -MAX_VELOCITY
            
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.animation_run.frame = 0
             
        # Check for right key down
        elif keys[pygame.K_RIGHT] == True:
            self.animation_state_manager.set_state('run')
            self.reverse = False
            self.velocity[0] += ACCELERATION * dt
            if self.velocity[0] < 0:
                self.velocity[0] += ACCELERATION * dt
            if self.velocity[0] > MAX_VELOCITY:
                self.velocity[0] = MAX_VELOCITY
            
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.animation_run.frame = 0
                        
        # Check if left and right are both up            
        elif keys[pygame.K_LEFT] == False and keys[pygame.K_RIGHT] == False:
            self.animation_state_manager.set_state('idle')
            if self.velocity[0] > 0:
                self.velocity[0] -= ACCELERATION * dt * 1.5
                if self.velocity[0] < 0:
                    self.velocity[0] = 0
            elif self.velocity[0] < 0:
                self.velocity[0] += ACCELERATION * dt * 1.5
                if self.velocity[0] > 0:
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