'''
ISSUES:
- Maybe change these animation lists into dictionaries 
- cols and rows are backwards in load_sprite_sheet()
'''

import pygame

class sprite_handler:
    def __init__(self):
        pass
        
    def load_sprites(self, screen_width, screen_height):
        self.load_player_sprites()
        self.load_bunny_sprites()
        self.load_level_bg_sprites(screen_width, screen_height)

    def load_sprite_sheet(self, sprite_sheet, cols, rows):
        sprites = []
        sprite_sheet = pygame.image.load(f"sprites/{sprite_sheet}.png").convert_alpha()
        sprite_sheet_width  = sprite_sheet.get_width()
        sprite_sheet_height = sprite_sheet.get_height()
        sprite_width  = sprite_sheet_width // cols
        sprite_height = sprite_sheet_height // rows
        
        for y in range(rows):
            for x in range(cols):
                sprite_x = x * sprite_width
                sprite_y = y * sprite_height
                
                sprite_rect = pygame.Rect(sprite_x, sprite_y, sprite_width, sprite_height)
                
                is_blank = True
                for i in range(sprite_rect.width):
                    for j in range(sprite_rect.height):
                        pixelColor = sprite_sheet.get_at((sprite_rect.x + i, sprite_rect.y + j))
                        if pixelColor[3] != 0: # check the alpha channel
                            is_blank = False
                            break

                if not is_blank:
                    sprites.append(sprite_sheet.subsurface(sprite_rect))
        
        return sprites
        
    def load_player_sprites(self):
        sprites = self.load_sprite_sheet("player", 6, 6)
    
        self.player_idle   = [sprites[ 0], sprites[ 1], sprites[ 2], sprites[ 3]                        ]
        self.player_run    = [sprites[ 4], sprites[ 5], sprites[ 6], sprites[ 7], sprites[8], sprites[9]]
        self.player_climb  = [sprites[10], sprites[11], sprites[12], sprites[13]                        ]
        self.player_crouch = [sprites[14], sprites[15], sprites[16]                                     ]
        self.player_death  = [sprites[17], sprites[18]                                                  ]
        self.player_jump   = [sprites[19], sprites[20]                                                  ]

    def load_bunny_sprites(self):
        sprites = self.load_sprite_sheet("bunny", 3, 1) 
        self.bunny_jump = []
        for sprite in sprites:
            self.bunny_jump.append(pygame.transform.scale(sprite, (24,24)))
            
    def load_level_bg_sprites(self, screen_width, screen_height):
        sprite = pygame.image.load("sprites/back.png").convert_alpha()
        self.bg_sprite = pygame.transform.scale(sprite, (screen_width, screen_height))
            
if __name__ == '__main__':
    pass