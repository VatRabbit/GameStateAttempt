import pygame

class Menu:
    def __init__(self, display, game_state_manager):
        self.display = display
        self.game_state_manager = game_state_manager
            
    def run(self, events, dt, sprite_handler):
        for event in events:
                if event.type == pygame.KEYDOWN:
                    self.game_state_manager.set_state('level')                     
        # print('running Menu')
                     
    def render(self, dt, display):
        display.fill((140, 140, 110))
        # print('rendering menu')
            
    def reset(self):
        pass
if __name__ == '__main__':
    pass