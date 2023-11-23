import pygame
from main import SCALED_HEIGHT

TERMINAL_VELOCITY = 5
G_ACCELERATION = 20
JUMP = -8
SPEED = 100

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

        self.reverse = False
        # 0 = left/right, 1 = up/down
        self.velocity = [0,0]
        self.x, self.y = 0.0, 0.0        
        # add air timer
        self.air_timer = 0.0
        self.collider = pygame.Rect(0,0,0,0)

    def air_timer(self):
        if self.grounded == False:
            self.air_timer += 0.0        
        
    def apply_gravity(self, dt):
        if self.y <= SCALED_HEIGHT:
            self.velocity[1] += G_ACCELERATION * dt
            if self.velocity[1] > TERMINAL_VELOCITY:
                self.velocity[1] = TERMINAL_VELOCITY
            print(self.velocity[1])
               
    def handle_x_collisions(self, collision_list):
        for rect in collision_list:
            if rect.colliderect(self.collision_rect):
                if self.velocity[0] > 0:
                    # print('collision right')
                    self.collider = rect
                    self.x = rect.left - self.collision_rect.width
                
                elif self.velocity[0] < 0:
                    # print('collision left')
                    self.collider = rect
                    self.x = rect.right
                                                    
    def handle_y_collisions(self, collision_list):
        for rect in collision_list:
            if rect.colliderect(self.collision_rect):
                if self.velocity[1] > 0:
                    # print('collision bot')
                    self.collider = rect
                    self.y = rect.top
                    # print(self.collision_rect.top, self.y, rect.top)
                    self.collision_rect.bottom = self.y
                    self.velocity[1] = 0
                    
                '''
                elif self.velocity[1] < 0:
                    # print('collision top')
                    self.collider = rect
                    self.y = rect.bottom + self.collision_rect.height
                    self.collision_rect.bottom = self.y
                    self.velocity[1] = 0
                '''
                                   
    def collision_detected(self):
        # print('collision!')
        pygame.draw.rect(self.display, (250,250,50), self.collider)

    def update(self, events, dt, col_list):
        self.handle_input(events, dt)
        
        # handle self.x, left/right movement and check left/right collisions 
        self.update_x_velocity()
        self.handle_x_collisions(col_list)
        # print(self.x)
        
        # handle self.y, up/down movement and check for up/down collisions
        self.apply_gravity(dt)
        self.update_y_velocity()
        self.handle_y_collisions(col_list)
        # print(self.y)
        
        print(self.velocity[1])
        self.update_player_rect()
        
    def render(self):
        self.animation_states[self.animation_state_manager.get_state()].run(self.rect, self.reverse)
        
    def update_x_velocity(self):
        self.x += self.velocity[0]
        self.collision_rect.x = self.x
        
    def update_y_velocity(self):
        self.y += self.velocity[1]
        if self.y > SCALED_HEIGHT:
            self.y = SCALED_HEIGHT
        self.collision_rect.y = self.y

    def update_player_rect(self):
        # self.collision_rect.bottomleft = self.x, self.y
        self.rect.midbottom = self.collision_rect.midbottom
        
    def handle_input(self, events, dt):
        keys = pygame.key.get_pressed()
        
        if self.velocity[1] == 0:
             for event in events:
                 if event.type == pygame.KEYDOWN:
                     if event.key == pygame.K_SPACE:
                         self.velocity[1] = JUMP
                         print('jumping!')

        if keys[pygame.K_LEFT] == True and keys[pygame.K_RIGHT] == True:
            self.animation_state_manager.set_state('idle')
            self.velocity[0] = 0
            # print('stopped')
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.type == pygame.K_LEFT or event.type == pygame.K_RIGHT:
                        self.animationIdle.frame = 0
                    
        elif keys[pygame.K_LEFT] == True:
            self.animation_state_manager.set_state('run')
            self.reverse = True
            self.velocity[0] = -SPEED * dt
            # print('moving left')
            
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.animation_run.frame = 0
                        
        elif keys[pygame.K_RIGHT] == True:
            self.animation_state_manager.set_state('run')
            self.reverse = False
            self.velocity[0] = SPEED * dt
            # print('moving right')
            
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.animation_run.frame = 0
            
        elif keys[pygame.K_LEFT] == False and keys[pygame.K_RIGHT] == False:
            self.animation_state_manager.set_state('idle')
            self.velocity[0] = 0
            # print('stopped')
            for event in events:
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.animation_idle.frame = 0
                        
        if self.velocity[1] != 0:
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