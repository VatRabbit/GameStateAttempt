import pygame

class enemy(pygame.sprite.Sprite):
    def __init__(self, display):
        super().__init__()
        
        self.display = display
        
        self.velocity      = [0, 0]
        self.true_location = [0, 0]
        self.location      = [0, 0]
    
    # carry out enemy logic, set velocity and direction, and set animation states
    def AI(self):
        pass
    
    # apply velocity to enemy
    def update(self):
        self.location[0] = int(self.true_location[0])
        self.location[1] = int(self.true_location[1])
    
    # render that shit
    def render(self):
        pass
    
    class Animation_State_Manager:
        def __init__(self, current_state):
            self.current_state = current_state
        
        def get_state(self):
            return self.current_state
        
        def set_state(self, state):
            self.current_state = state
