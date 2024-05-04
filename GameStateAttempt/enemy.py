'''
will need to create a rect infront and below the enemy to check for empty space
also check for walls so it can reverse direction
'''

import pygame

class enemy(pygame.sprite.Sprite):
    def __init__(self, display, x, y):
        super().__init__()
        self.display        = display
        self.velocity       = [0, 0]
        self.position       = [x, y]
        self.rect           = pygame.Rect(0,0, 16,16)
        self.collision_list = []
        # reverse = left
        # could change this out for a + or - velocity check instead
        # and then multiply out velocity by -1
        self.reverse        = True
        
    # carry out enemy logic, set velocity and direction, and set animation states
    def AI(self, dt, tilemap, TILE_SIZE):
        self.collision_list = self.check_collisions(tilemap, TILE_SIZE)
        
        if self.reverse:
            for col in self.collision_list:
                if col.right > self.rect.left:
                    print("collision left!")
                    self.position[0] = col.right
                    self.reverse = False
        else:            
            for col in self.collision_list:  
                print(col)
                print(self.rect)             
                if col.left < self.rect.right:
                    # print("collision right!")
                    self.position[0] = col.left - 16
                    self.reverse = True
                    
        if self.reverse:
            self.velocity[0] = dt * 20 * -1
        else:
            self.velocity[0] = dt * 20 
            
        self.position[0] += self.velocity[0]
        self.rect.x = int(self.position[0])
        self.rect.y = int(self.position[1]) 

    # apply velocity to enemy
    def update(self, dt, tilemap, TILE_SIZE):
        self.AI(dt, tilemap, TILE_SIZE)
        
    # render that shit
    def render(self, offset_x):
        self.show_collision_check_list(offset_x)
        rect = self.rect.copy()
        rect.x -= offset_x        
        pygame.draw.rect(self.display, (200,10,10), rect)
        # pygame.draw.rect(self.display, (220,220,220), pygame.Rect(64 - offset_x, 128, 16, 16))
        
    # just gonna check for x-axis collisions here
    def check_collisions(self, tilemap, TILE_SIZE):
        check_list = []
        for i in range(-1, 1):               
            # seems like things are a bit sideways...
            grid_x = int((self.position[1]) / TILE_SIZE)                  
            grid_y = int((self.position[0]) / TILE_SIZE + i + 1)
            
            if tilemap[grid_x][grid_y] == 1:
                rect = pygame.Rect(grid_y * TILE_SIZE, grid_x * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                check_list.append(rect)
                
        return check_list
    
    # displays the tiles in range for collision checks
    def show_collision_check_list(self, offset_x):
        for rect in self.collision_list:
            rect.x -= offset_x
            pygame.draw.rect(self.display, (50,200,50), rect)
    
    class Animation_State_Manager:
        def __init__(self, current_state):
            self.current_state = current_state
        
        def get_state(self):
            return self.current_state
        
        def set_state(self, state):
            self.current_state = state

if __name__ == '__main__':
    pass