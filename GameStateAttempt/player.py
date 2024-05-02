import pygame

TERMINAL_VELOCITY = 5
G_ACCELERATION = 25
JUMP = -7
SPEED = 175
COYOTE_LIMIT = 0.1

class Player(pygame.sprite.Sprite):
    def __init__(self, display, sprites_idle, sprites_run, sprites_jump):
        super().__init__()
        self.display = display       
        
        self.animation_state_manager = self.Animation_State_Manager('idle')
        self.animation_idle = self.Animation_Idle(display, sprites_idle)
        self.animation_run  = self.Animation_Run(display, sprites_run)
        self.animation_jump = self.Animation_Jump(display, sprites_jump)
        self.animation_states = {'idle': self.animation_idle, 'run': self.animation_run, 'jump': self.animation_jump}
        
        # self.sprites = self.sprite_list_idle
        self.rect = pygame.Rect(0,0, 16,16)
        self.collision_rect = pygame.Rect(0,0,10,16)
        
        # handles which direction the sprite should be facing during animations
        self.reverse = False
        # velocity[0] = left/right, velocity[1] = up/down
        self.velocity = [0,0]
        self.position = [0,0]
        self.x, self.y = 0.0, 0.0
        self.coyote_time = 0.0
        self.jump_buffer = 0.0
        self.jump_height_counter = 0.0
        self.double_jump_ready = False
        # self.collider = pygame.Rect(0,0,0,0)
        self.is_grounded = False
        self.last_y = 0.0
        
    def check_grounded(self, collision_list):
        tollerance = 0.7
        self.is_grounded = False
        
        for rect in collision_list:
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

    def update(self, events, dt, col_list):
        self.handle_input(events, dt)
        
        # handle self.x, left/right movement and check left/right collisions 
        self.update_x_velocity()
        self.handle_x_collisions(col_list)
                
        # handle self.y, up/down movement and check for up/down collisions
        self.apply_gravity(dt)
        self.update_y_velocity()
        self.check_grounded(col_list)
        self.handle_y_collisions(col_list)
          
        self.update_player_rect()
        self.coyote_counter(dt)
        
    def render(self, offset_x):
        rect = self.rect
        rect.x -= offset_x
        self.animation_states[self.animation_state_manager.get_state()].run(rect, self.reverse)
        
    def update_x_velocity(self):
        self.x += self.velocity[0]
        self.collision_rect.left = self.x
        
    def update_y_velocity(self):
        self.y += self.velocity[1]
        self.collision_rect.bottom = self.y
        
    def handle_x_collisions(self, collision_list):
        tollerance = 10
        
        for rect in collision_list:
            if rect.colliderect(self.collision_rect):
                # check for left collision first
                if self.collision_rect.left - tollerance <= rect.right <= self.collision_rect.left + tollerance:
                    self.x = rect.right
                    self.collision_rect.left = self.x
                    self.velocity[0] = 0

                # check for right collision next
                elif self.collision_rect.right + tollerance >= rect.left >= self.collision_rect.right - tollerance:
                    self.x = rect.left - self.collision_rect.width 
                    self.collision_rect.left = self.x
                    self.velocity[0] = 0
                
    def handle_y_collisions(self, collision_list):
        # max of 8
        tollerance = 8
        
        for rect in collision_list:
            if rect.colliderect(self.collision_rect):                                
                if self.collision_rect.bottom + tollerance >= rect.top >= self.collision_rect.bottom - tollerance:
                    self.y = rect.top
                    self.collision_rect.bottom = self.y    
                    # self.velocity[1] = 0
                
                elif self.collision_rect.top - tollerance <= rect.bottom <= self.collision_rect.top + tollerance:                    
                    self.y = rect.bottom + self.collision_rect.height
                    self.collision_rect.bottom = self.y       
                    self.velocity[1] = 0
                    
    # This is not being used I think. Either scrap it or redo it ig.
    def collision_detected(self):
        pygame.draw.rect(self.display, (250,250,50), self.collider)
    
    def apply_gravity(self, dt):
         self.velocity[1] += G_ACCELERATION * dt
         if self.velocity[1] > TERMINAL_VELOCITY:
             self.velocity[1] = TERMINAL_VELOCITY

    def update_player_rect(self):
        # self.collision_rect.bottomleft = self.x, self.y
        self.rect.midbottom = self.collision_rect.midbottom
        
    def handle_input(self, events, dt):
        keys = pygame.key.get_pressed()

        if self.is_grounded or self.coyote_time <= COYOTE_LIMIT:
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
        def __init__(self, display, sprites):
            self.display = display
            self.frame = 0
            self.animation_cooldown = 125
            self.last_update = pygame.time.get_ticks()
            self.sprites = sprites
            
        def run(self, rect, reverse):
            current_time = pygame.time.get_ticks()
            
            if (current_time - self.last_update >= self.animation_cooldown):
                self.frame += 1
                self.last_update = current_time
                if (self.frame >= len(self.sprites)):
                    self.frame = 0
            
            if reverse == True:
                reverse_sprite = pygame.transform.flip(self.sprites[self.frame], True, False)
                self.display.blit(reverse_sprite, rect)
            else:
                self.display.blit(self.sprites[self.frame], rect)
                
    class Animation_Jump:
        def __init__(self, display, sprites):
            self.display = display
            self.sprites = sprites
            self.frame = 0
            
        def run(self, rect, reverse):
            if reverse == True:
                reverse_sprite = pygame.transform.flip(self.sprites[self.frame], True, False)
                self.display.blit(reverse_sprite, rect)
            else:
                self.display.blit(self.sprites[self.frame], rect)
                
    class Animation_Run:
        def __init__(self, display, sprites):
            self.display = display
            self.frame = 0
            self.animation_cooldown = 75
            self.last_update = pygame.time.get_ticks()
            self.sprites = sprites
            
        def run(self, rect, reverse):
            current_time = pygame.time.get_ticks()
            
            if (current_time - self.last_update >= self.animation_cooldown):
                self.frame += 1
                self.last_update = current_time
                if (self.frame >= len(self.sprites)):
                    self.frame = 0
                    
            if reverse == True:
                reverse_sprite = pygame.transform.flip(self.sprites[self.frame], True, False)
                self.display.blit(reverse_sprite, rect)
            else:
                self.display.blit(self.sprites[self.frame], rect)

if __name__ == '__main__':
    pass