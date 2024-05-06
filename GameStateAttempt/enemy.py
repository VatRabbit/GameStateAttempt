'''
To Do:
- swap out self.rect for self.collision_rect where needed
'''

import pygame

SPEED = 40
ANIMATION_SPEED = 7

class enemy(pygame.sprite.Sprite):
    def __init__(self, display, x, y, TILE_SIZE, sprites):
        super().__init__()
        self.display         = display
        self.velocity        = [0, 0]
        self.position        = [x, y]
        self.rect            = pygame.Rect(0,0, 24,24)
        self.collision_rect  = pygame.Rect(0,0, 14,16)
        # self.collision_list  = []
        # self.collision_range = []
        
        # reverse = left
        # could change this out for a + or - velocity check instead
        # and then multiply velocity by -1
        self.reverse     = True
        self.ground_rect = pygame.Rect(0,0, TILE_SIZE,TILE_SIZE) 
        self.wall_rect   = pygame.Rect(0,0, TILE_SIZE,TILE_SIZE)
        
        self.animation_state_manager = self.Animation_State_Manager('jump')
        self.animation_jump          = self.Animation_Jump(display, sprites)
        self.animation_states        = {'jump': self.animation_jump}
        
    # carry out enemy logic, set velocity and direction, and set animation states
    def AI(self, dt, tilemap, TILE_SIZE):
        self.collision_list = self.check_collisions(TILE_SIZE)
        grounded = self.check_ground(tilemap, TILE_SIZE)
        
        if self.reverse:
            # all I really need is the y and x coordinates of wall_rect, really. Rect could be a waste
            if tilemap[int(self.wall_rect.y / TILE_SIZE)][int(self.wall_rect.x / TILE_SIZE)] == 1:
                if self.wall_rect.right > self.collision_rect.left:
                     self.collision_rect.left = self.wall_rect.right
                     self.reverse = False 
            if grounded == False:
                 self.reverse = False
        else:
            if tilemap[int(self.wall_rect.y / TILE_SIZE)][int(self.wall_rect.x / TILE_SIZE)] == 1:
                if self.wall_rect.left < self.collision_rect.right:
                    self.collision_rect.right = self.wall_rect.left
                    self.reverse = True
            if grounded == False:
                self.reverse = True
                    
        if self.reverse:
            self.velocity[0] = dt * SPEED * -1
        else:
            self.velocity[0] = dt * SPEED
            
        self.position[0] += self.velocity[0]
        self.rect.x       = int(self.position[0])
        self.rect.y       = int(self.position[1]) - 8
        self.collision_rect.midbottom = self.rect.midbottom
        
    # apply velocity to enemy
    def update(self, dt, tilemap, TILE_SIZE):
        self.AI(dt, tilemap, TILE_SIZE)
        
    # render that shit
    def render(self, offset_x, dt):
        rect = self.rect.copy()
        rect.x -= offset_x
        col_rect = self.collision_rect.copy()
        col_rect.x -= offset_x
        wall_rect = self.wall_rect.copy()
        wall_rect.x -= offset_x
        ground_rect = self.ground_rect.copy()
        ground_rect.x -= offset_x
        
        pygame.draw.rect(self.display, (250,100,100), col_rect, 2)        
        pygame.draw.rect(self.display, (200,200,200), wall_rect, 2)
        pygame.draw.rect(self.display, (150,150,200), ground_rect, 2)
        self.animation_states[self.animation_state_manager.get_state()].run(rect, self.reverse, dt)
        
    # just gonna check for x-axis collisions here
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
                
        self.ground_rect = rect
        # print(tilemap[int(rect.y / TILE_SIZE)][int(rect.x / TILE_SIZE)])
        
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
        def __init__(self, display, sprites):
            self.display    = display
            self.sprites    = sprites
            self.frame      = 0
            self.true_frame = 0.0
            
        def run(self, rect, reverse, dt):
            if reverse == True:
                reverse_sprite = pygame.transform.flip(self.sprites[self.frame], True, False)
                self.display.blit(reverse_sprite, rect)
            else:
                self.display.blit(self.sprites[self.frame], rect)
            self.true_frame += dt * ANIMATION_SPEED
            if self.true_frame >= 1:
                self.frame += 1
                self.true_frame -= 1
                print(len(self.sprites))
                if self.frame > len(self.sprites) - 1:
                    self.frame = 0
                    
if __name__ == '__main__':
    pass