import pygame
from main import DISPLAY_SCALE, SCALED_HEIGHT, SCREEN_HEIGHT, SPEED, SCALED_WIDTH, TILE_SIZE

TERMINAL_VELOCITY = 250
G_ACCELERATION = 1500
JUMP = -500

class Player(pygame.sprite.Sprite):
    def __init__(self, display):
        super().__init__()
        self.display = display
        self.load_sprite_sheet()       
        
        self.animation_state_manager = self.Animation_State_Manager('idle')
        self.animation_idle = self.Animation_Idle(display, self.sprite_list_idle)
        self.animation_run = self.Animation_Run(display, self.sprite_list_run)
        self.animation_jump = self.Animation_Jump(display, self.sprite_list_jump)
        self.animation_states = {'idle': self.animation_idle, 'run': self.animation_run, 'jump': self.animation_jump}
        
        self.sprites = self.sprite_list_idle
        self.rect = self.sprites[0].get_rect(bottomleft = (20,100))
        self.collision_rect = pygame.Rect(0,0,10,20)
        
        self.is_grounded = False
        self.reverse = False
        self.gravity = 0     
        # look for Spawn Tile and set player starting pos with it
        self.velocity = [0,0]
        self.x, self.y = 0.0, 0.0  
        self.ground_rect = pygame.Rect(0,0,0,0)
        
        # add air timer
        self.air_timer = 0.0

    def air_timer(self):
        if self.grounded == False:
            self.air_timer += 0.0        
        
    def apply_gravity(self, dt):
         if self.is_grounded and self.gravity > 0:
             self.gravity = 0             
         else:
             self.gravity += G_ACCELERATION * dt
        
         if self.y < SCALED_HEIGHT:      
             # allow for jumping if grounded and -acceleration
             if self.is_grounded == True or self.y == SCALED_HEIGHT:
                 if self.gravity < 0:
                    self.y += self.gravity * dt
                    if self.gravity <=  TERMINAL_VELOCITY: # terminal velocity
                         self.gravity += G_ACCELERATION * dt   # acceleration due to gravity                                
                    else:
                        self.gravity = TERMINAL_VELOCITY                        
                                  
             else:
                  self.y += self.gravity * dt
                  if self.gravity <  TERMINAL_VELOCITY: # terminal velocity
                         self.gravity += G_ACCELERATION * dt   # acceleration due to gravity  
                      
         else:
            self.y = SCALED_HEIGHT
            self.is_grounded = True
            # self.gravity = 0
            
         if self.gravity > TERMINAL_VELOCITY:
             self.gravity = TERMINAL_VELOCITY
             
         print(self.gravity)
            
    def handle_collisions(self, collision_list):
        # get all surrounding tiles and check them for collisions
        y_tollerance = 5.0
        x_tollerance = 0.0
        
        for rect in collision_list:
            if self.collision_rect.colliderect(rect):
                if rect.top + y_tollerance >= self.y >= rect.top - y_tollerance:
                     self.ground_rect = rect 
                     self.y = rect.top                     
                     self.is_grounded = True                     
                     # print('grounded')
                     print('y set to rect.top: ', self.y)                    
                     print(self.ground_rect.right, self.x, self.x + self.collision_rect.width, self.ground_rect.left)
                     
        if (
            self.is_grounded
            and self.ground_rect.right >= self.x
            and self.x + self.collision_rect.width >= self.ground_rect.left
            and self.ground_rect.top + x_tollerance >= self.y >= self.ground_rect.top - x_tollerance
        ):
            self.is_grounded = True
            self.y = self.ground_rect.top
            # print('grounded')
        else:
            self.is_grounded = False

    def update(self, events, dt, col_list):
        self.handle_input(events, dt) 
        self.apply_gravity(dt)          
        self.handle_collisions(col_list)         
        self.update_player_rect() 
        
    def render(self):
        self.animation_states[self.animation_state_manager.get_state()].run(self.rect, self.reverse)

    def update_player_rect(self): 
        self.collision_rect.bottomleft = (self.x,self.y)
        self.rect.midbottom = self.collision_rect.midbottom
        
    def handle_input(self, events, dt):
        keys = pygame.key.get_pressed()
        
        if self.is_grounded == True:
             for event in events:
                 if event.type == pygame.KEYDOWN:
                     if event.key == pygame.K_SPACE:
                         # self.is_grounded = False
                         # self.y -= 1
                         self.gravity = JUMP
                         print('jumping!')

        if keys[pygame.K_LEFT] == True and keys[pygame.K_RIGHT] == True:
            self.animation_state_manager.set_state('idle')
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.type == pygame.K_LEFT or event.type == pygame.K_RIGHT:
                        self.animationIdle.frame = 0
                    
        elif keys[pygame.K_LEFT] == True:
            self.animation_state_manager.set_state('run')
            self.reverse = True
            self.x -= SPEED * dt
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.animation_run.frame = 0                                            
                        
        elif keys[pygame.K_RIGHT] == True:
            self.animation_state_manager.set_state('run')
            self.reverse = False
            self.x += SPEED * dt
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.animation_run.frame = 0                        
            
        elif keys[pygame.K_LEFT] == False and keys[pygame.K_RIGHT] == False:
            self.animation_state_manager.set_state('idle')
            for event in events:
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.animation_idle.frame = 0    
                        
        if self.is_grounded == False:        
            self.animation_state_manager.set_state('jump')   
            
    def load_sprite_sheet(self):
        # 198 x 192p spritesheet with 6 collumbs and 6 rows 
        sprites = []
        spritesNumberWidth = 6
        spritesNumberHeight = 6
        spriteSheet = pygame.image.load('GameStateAttempt/player/player.png').convert_alpha()
        spriteSheetWidth = spriteSheet.get_width()
        spriteSheetHeight = spriteSheet.get_height()
        spriteWidth = spriteSheetWidth // spritesNumberWidth
        spriteHeight = spriteSheetHeight // spritesNumberHeight
        
        for y in range(spritesNumberWidth):
            for x in range(spritesNumberHeight):                        
                spriteX = x * spriteWidth
                spriteY = y * spriteHeight                
                
                spriteRect = pygame.Rect(spriteX, spriteY, spriteWidth, spriteHeight)
                
                isBlank = True
                for i in range(spriteRect.width):
                    for j in range(spriteRect.height):
                        pixelColor = spriteSheet.get_at((spriteRect.x + i, spriteRect.y + j))
                        if pixelColor[3] != 0: # check the alpha channel
                            isBlank = False
                            break

                if not isBlank:
                    sprites.append(spriteSheet.subsurface(spriteRect))
        
        self.sprite_list_idle   = [sprites[0],  sprites[1],  sprites[2],  sprites[3]]
        self.sprite_list_run    = [sprites[4],  sprites[5],  sprites[6],  sprites[7], sprites[8],  sprites[9]]
        self.sprite_list_climb  = [sprites[10], sprites[11], sprites[12], sprites[13]]
        self.sprite_list_crouch = [sprites[14], sprites[15], sprites[16]]
        self.sprite_list_death  = [sprites[17], sprites[18]]
        self.sprite_list_jump   = [sprites[19], sprites[20]]  
                
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