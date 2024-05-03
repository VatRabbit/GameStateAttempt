import pygame

from main import DELTA_TIME

class enemy(pygame.sprite.Sprite):
    def __init__(self, display, x, y, dt):
        super().__init__()
        
        self.display = display
        self.dt = dt
        
        self.velocity      = [0, 0]
        self.true_location = [x, y]
        self.location      = [0, 0]
        self.rect = pygame.Rect(0,0,16,16)
        
        print('I am alive!')
        print(f'true location: {self.true_location}')
        print(f'location     : {self.location}')
        
    # carry out enemy logic, set velocity and direction, and set animation states
    def AI(self):
        self.velocity[0] += 100 * DELTA_TIME
        # print(f"velocity : {self.velocity}")
        # print(f"dt : {self.dt}")
    
    # apply velocity to enemy
    def update(self):
        self.AI()
        self.true_location[0] += self.velocity[0]
        self.location[0] = int(self.true_location[0])
        self.location[1] = int(self.true_location[1])
        self.rect.x = self.location[0]
        self.rect.y = self.location[1]
        # print(f"enemy velocity x : {self.velocity[0]}")
        # print(f'true location    : {self.true_location}')        
        # print(self.rect.x, self.rect.y)
    
    # render that shit
    def render(self, offset_x):
        self.rect.x -= offset_x
        pygame.draw.rect(self.display, (200,10,10), self.rect)
        # print('rendering')
    
    class Animation_State_Manager:
        def __init__(self, current_state):
            self.current_state = current_state
        
        def get_state(self):
            return self.current_state
        
        def set_state(self, state):
            self.current_state = state

    def sign_off(self):
        print(f"enemy position  : {self.location}")