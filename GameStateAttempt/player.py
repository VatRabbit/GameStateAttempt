
import pygame
from main import DISPLAY_SCALE, SCREEN_HEIGHT, SPEED, SCALED_WIDTH

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
        self.gravity = 0     
        self.x, self.y = 50.0 / DISPLAY_SCALE, 300.0 / DISPLAY_SCALE
        
    def apply_gravity(self, dt):
        self.y += self.gravity * dt
        
        if self.y < SCREEN_HEIGHT / DISPLAY_SCALE:
            if self.gravity < 1000: # terminal velocity
                self.gravity += 1000 * dt   # acceleration due to gravity
            
        if self.y > SCREEN_HEIGHT / DISPLAY_SCALE:
            self.y = SCREEN_HEIGHT / DISPLAY_SCALE
            
    def handle_collisions(self, collision_list):
        # get all surrounding tiles and check them for collisions
        for collision in collision_list:
            pass
        
    def handle_input(self, events, dt):
        keys = pygame.key.get_pressed() 
        
        if self.y == SCREEN_HEIGHT / DISPLAY_SCALE:
             for event in events:
                 if event.type == pygame.KEYDOWN:
                     if event.key == pygame.K_SPACE:                         
                         self.gravity = -400                

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
                        
        if self.y < SCREEN_HEIGHT / DISPLAY_SCALE:
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

    def update(self, events, dt):
        self.handle_input(events, dt)   
        self.apply_gravity(dt)
        # self.handle_collisions() 
        self.update_player_rect() 
        self.animation_states[self.animation_state_manager.get_state()].run(self.rect, self.reverse)

    def update_player_rect(self): 
        if self.x < 0:
            self.x = 0
          
        elif self.x > SCALED_WIDTH - self.collision_rect.width:                        
            self.x = SCALED_WIDTH - self.collision_rect.width
                        
        self.collision_rect.bottomleft = (self.x,self.y)
        self.rect.midbottom = self.collision_rect.midbottom
        # print(self.x)
        
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