'''
To Do:
- have enemies reverse direction when colliding with eachother
- could have some issues with the reverse cd with multiple enemies 
- in a tight area together

ISSUES:
'''

import pygame

SPEED = 50
ANIMATION_SPEED = 7

class enemy(pygame.sprite.Sprite):
    def __init__(self, display, x, y, TILE_SIZE, sprites):
        super().__init__()
        self.display       = display
        self.reverse       = True
        self.velocity      = [0, 0]
        self.position      = [x, y]        
        self.reverse_timer = 0.0
        self.reverse_cd    = 0.1
        
        self.image          = pygame.Surface((24,24))        
        self.rect           = pygame.Rect(0,0, 24,24)
        self.collision_rect = pygame.Rect(0,0, 14,16)                
        self.wall_rect      = pygame.Rect(0,0, TILE_SIZE,TILE_SIZE)  
        
        self.animation_state_manager = self.Animation_State_Manager('jump')
        self.animation_jump          = self.Animation_Jump(sprites)
        self.animation_states        = {'jump': self.animation_jump}
        
    # carry out enemy logic, set velocity and direction, and set animation states
    def AI(self, dt, tilemap, TILE_SIZE):
        if self.reverse:
            self.velocity[0] = dt * SPEED * -1
        else:
            self.velocity[0] = dt * SPEED        
        
        self.position[0] += self.velocity[0]
        self.rect.x       = int(self.position[0])
        self.rect.y       = int(self.position[1]) - (self.rect.height - TILE_SIZE)
        self.collision_rect.midbottom = self.rect.midbottom
        self.collision_list = self.check_collisions(TILE_SIZE)        
        
        self.reverse_timer += dt
        grounded = self.check_ground(tilemap, TILE_SIZE)
        
        if self.reverse and self.reverse_timer > self.reverse_cd:
            # all I really need is the y and x coordinates of wall_rect, really. Rect could be a waste
            if tilemap[int(self.wall_rect.y / TILE_SIZE)][int(self.wall_rect.x / TILE_SIZE)] == 1:
                if self.wall_rect.right > self.collision_rect.left:
                     self.collision_rect.left = self.wall_rect.right
                     self.reverse = False 
                     self.reverse_timer = 0
            if grounded == False:                
                 self.reverse = False
                 self.reverse_timer = 0 
                 
        elif not self.reverse and self.reverse_timer > self.reverse_cd:
            if tilemap[int(self.wall_rect.y / TILE_SIZE)][int(self.wall_rect.x / TILE_SIZE)] == 1:
                if self.wall_rect.left < self.collision_rect.right:
                    self.collision_rect.right = self.wall_rect.left
                    self.reverse = True
                    self.reverse_timer = 0
            if grounded == False:
                self.reverse = True
                self.reverse_timer = 0        
                
    # apply velocity to enemy
    def update(self, dt, tilemap, TILE_SIZE):
        self.AI(dt, tilemap, TILE_SIZE)
        
    # render that shit
    def render(self, offset_x, dt):        
        self.rect.x -= offset_x        
        self.image = self.animation_states[self.animation_state_manager.get_state()].run(self.reverse, dt)
        
    # just gonna check for x-axis collisions here
    # maybe should combine the two collision check methods eventually    
    def check_collisions(self, TILE_SIZE):
        rect = None
        
        if self.reverse:
            rect = pygame.Rect(int(self.collision_rect.centerx / TILE_SIZE - 1) * TILE_SIZE, int(self.collision_rect.centery / TILE_SIZE) * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        else:
            rect = pygame.Rect(int(self.collision_rect.centerx / TILE_SIZE + 1) * TILE_SIZE, int(self.collision_rect.centery / TILE_SIZE) * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            
        self.wall_rect = rect

    # returns true if ground is ahead. False otherwise
    def check_ground(self, tilemap, TILE_SIZE):  
        rect = None
        
        if self.reverse:
            rect = pygame.Rect(int(self.collision_rect.centerx / TILE_SIZE) * TILE_SIZE, int(self.collision_rect.centery / TILE_SIZE + 1) * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        else:
            rect = pygame.Rect(int(self.collision_rect.centerx / TILE_SIZE) * TILE_SIZE, int(self.collision_rect.centery / TILE_SIZE + 1) * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        
        if tilemap[int(rect.y / TILE_SIZE)][int(rect.x / TILE_SIZE)] == 0:
            return False            
        else:
            return True

    class Animation_State_Manager:
        def __init__(self, current_state):
            self.current_state = current_state
        
        def get_state(self):
            return self.current_state
        
        def set_state(self, state):
            self.current_state = state
            
    class Animation_Jump:
        def __init__(self, sprites):
            self.sprites    = sprites
            self.frame      = 0
            self.true_frame = 0.0
            
        def run(self, reverse, dt):
            self.true_frame += dt * ANIMATION_SPEED           
            
            if self.true_frame >= 1:
                self.frame += 1
                self.true_frame -= 1
                if self.frame > len(self.sprites) - 1:
                    self.frame = 0
                    
            if reverse:                
                return pygame.transform.flip(self.sprites[self.frame], True, False)                                                 
            else:                
                return self.sprites[self.frame]                                
                
if __name__ == '__main__':
    pass