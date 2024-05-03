'''
will need to create a rect infront and below the enemy to check for empty space
also check for walls so it can reverse direction
'''

import pygame

class enemy(pygame.sprite.Sprite):
    def __init__(self, display, x, y, dt, tilemap):
        super().__init__()
        
        self.display = display        
        
        self.velocity      = [0, 0]
        self.true_location = [x, y]
        self.location      = [0, 0]
        self.rect = pygame.Rect(0,0,16,16)
        self.collision_list = []
        self.reverse = False
        
    # carry out enemy logic, set velocity and direction, and set animation states
    def AI(self, dt):
        # if rect.x  
        
        self.velocity[0] = dt * 20
     
    '''
    def check_collisions(self, tilemap):
        check_list = []
        for i in range(-1, 2):
            for j in range(-1, 3):
                grid_y = int((self.player.position[0]) / TILE_SIZE + i)
                grid_x = int((self.player.position[1]) / TILE_SIZE + j - 1)
                    
                if 0 <= grid_x < len(self.level_tiles) and 0 <= grid_y < len(self.level_tiles[0]):
                     if self.level_tiles[grid_x][grid_y] == 1:
                          rect = pygame.Rect(grid_y * TILE_SIZE, grid_x * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                          check_list.append(rect)

        return check_list
    '''    
            
    # apply velocity to enemy
    def update(self, dt):
        self.AI(dt)
        self.true_location[0] += self.velocity[0]
        self.location[0] = int(self.true_location[0])
        self.location[1] = int(self.true_location[1])
        self.rect.x = self.location[0]
        self.rect.y = self.location[1]
    
    # render that shit
    def render(self, offset_x):
        self.rect.x -= offset_x
        pygame.draw.rect(self.display, (200,10,10), self.rect)
    
    class Animation_State_Manager:
        def __init__(self, current_state):
            self.current_state = current_state
        
        def get_state(self):
            return self.current_state
        
        def set_state(self, state):
            self.current_state = state

if __name__ == '__main__':
    pass