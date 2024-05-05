'''
To Do:
- idk
'''

import pygame

class enemy(pygame.sprite.Sprite):
    def __init__(self, display, x, y, TILE_SIZE):
        super().__init__()
        self.display        = display
        self.velocity       = [0, 0]
        self.position       = [x, y]
        self.rect           = pygame.Rect(0,0, TILE_SIZE,TILE_SIZE)
        self.collision_list = []
        # reverse = left
        # could change this out for a + or - velocity check instead
        # and then multiply velocity by -1
        self.reverse        = True
        self.speed          = 20
        self.ground_rect    = pygame.Rect(0,0, TILE_SIZE,TILE_SIZE)
        
    # carry out enemy logic, set velocity and direction, and set animation states
    def AI(self, dt, tilemap, TILE_SIZE):
        self.collision_list = self.check_collisions(tilemap, TILE_SIZE)
        grounded = self.check_ground(tilemap, TILE_SIZE)
        
        if self.reverse:
            for col in self.collision_list:
                if col.right > self.rect.left:
                    self.position[0] = col.right
                    self.reverse = False 
            if grounded == False:
                self.reverse = False
        else:
            for col in self.collision_list:            
                if col.left < self.rect.right:
                    self.position[0] = col.left - TILE_SIZE
                    self.reverse = True
            if grounded == False:
                self.reverse = True
                    
        if self.reverse:
            self.velocity[0] = dt * self.speed * -1
        else:
            self.velocity[0] = dt * self.speed
            
        self.position[0] += self.velocity[0]
        self.rect.x       = int(self.position[0])
        self.rect.y       = int(self.position[1])
        
    # apply velocity to enemy
    def update(self, dt, tilemap, TILE_SIZE):
        self.AI(dt, tilemap, TILE_SIZE)
        
    # render that shit
    def render(self, offset_x):
        self.show_collision_check_list(offset_x)
        rect = self.rect.copy()
        rect.x -= offset_x
        pygame.draw.rect(self.display, (200,50,50), rect)
        
        ground_rect = self.ground_rect.copy()
        ground_rect.x -= offset_x
        pygame.draw.rect(self.display, (150,150,200), ground_rect)
        
    # just gonna check for x-axis collisions here
    def check_collisions(self, tilemap, TILE_SIZE):
        check_list = []
        for i in range(-1, 1):
            # seems like things are a bit sideways...
            grid_y = int((self.position[1]) / TILE_SIZE)                  
            grid_x = int((self.position[0]) / TILE_SIZE + i + 1)
            
            if tilemap[grid_y][grid_x] == 1:
                rect = pygame.Rect(grid_x * TILE_SIZE, grid_y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                check_list.append(rect)
                
        return check_list
    
    # returns true if ground is ahead. False otherwise
    def check_ground(self, tilemap, TILE_SIZE):  
        rect = None
        
        if self.reverse:
            rect = pygame.Rect(int(self.position[0] / TILE_SIZE) * TILE_SIZE, int(self.position[1] / TILE_SIZE + 1) * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        else:
            rect = pygame.Rect(int(self.position[0] / TILE_SIZE + 1) * TILE_SIZE, int(self.position[1] / TILE_SIZE + 1) * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                
        self.ground_rect = rect
        # print(tilemap[int(rect.y / TILE_SIZE)][int(rect.x / TILE_SIZE)])
        
        if tilemap[int(rect.y / TILE_SIZE)][int(rect.x / TILE_SIZE)] == 0:
            return False            
        else:
            return True

    # displays the tiles in range for collision checks
    def show_collision_check_list(self, offset_x):
        for rect in self.collision_list:
            rect.x -= offset_x
            pygame.draw.rect(self.display, (150,200,150), rect)
    
    class Animation_State_Manager:
        def __init__(self, current_state):
            self.current_state = current_state
        
        def get_state(self):
            return self.current_state
        
        def set_state(self, state):
            self.current_state = state

if __name__ == '__main__':
    pass