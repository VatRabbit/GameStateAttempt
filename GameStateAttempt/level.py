import pygame, enemy

class Level:
    def __init__(self, display, game_state_manager, player, tile_size, scaled_width, screen_width, screen_height):
        self.display = display
        self.game_state_manager = game_state_manager
        self.player = player                     
        self.new_state = True
        self.true_offset_x = 0.0
        self.offset_x = 0 
        self.first_run = True
        self.tilemap_rect_list = []            
        self.enemy_group = pygame.sprite.Group()
        self.camera_follow_multiplyer = 10
        self.TILE_SIZE = tile_size
        self.SCALED_WIDTH = scaled_width
        
        self.bg_timer = 0.0
        self.bg_image = pygame.Surface((screen_width, screen_height))
        self.bg_rect  = pygame.Rect(0, 0, screen_width, screen_height)
        
            
        # y then x for these (it's sideways :/ )
        # currently a 28x12 map            
        self.tilemap = [
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,2,0,0,0,0,0,0,0,0,0,1,1,1,0,1,0,1,0,1,1,1,0,0,1],
            [1,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,3,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,3,0,0,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        ]
            
    def run(self, events, dt, sprite_handler):
        for event in events:
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DELETE:
                        self.enemy_group.empty()                                           
                     
        if self.first_run:
            self.tilemap_rect_list = self.create_tile_rects(sprite_handler, self.display)
            self.bg_image = sprite_handler.bg_sprite
            print(sprite_handler.bg_sprite)
            self.first_run = False                
            
        self.camera()              
            
        self.player.update(events, dt, self.tilemap)
        self.enemy_group.update(dt, self.tilemap, self.TILE_SIZE)
        
    def render(self, dt, display):
        display.fill((110, 140, 140))
        self.render_background(dt, self.offset_x)
        self.render_tiles()     
        for sprite in self.enemy_group:
            sprite.render(self.offset_x, dt)            
        self.enemy_group.draw(display)
            
        self.player.render(self.offset_x, dt, display)
            
    def render_tiles(self):
        for rect in self.tilemap_rect_list:
            temp = rect.copy()
            temp.x -= self.offset_x
            pygame.draw.rect(self.display, (100,100,250), temp, 2)
                
    # game window is 224px or 14 tiles wide.
    def camera(self):
        if self.new_state:
            self.true_offset_x = self.player.position[0] - self.SCALED_WIDTH / 2 + 8
            self.offset_x = int(self.true_offset_x)
            self.new_state = False
                
        self.true_offset_x += self.player.velocity[0]
                
        # set the offset for the camera. Subtract 0.5 (tiles) to center everything
        self.offset_x += (self.true_offset_x - self.offset_x) / self.camera_follow_multiplyer - 1
            
        # keep the camera within the bounds of the level
        if self.offset_x < 0:
            self.offset_x = 0
             
        elif self.offset_x > len(self.tilemap[0]) * self.TILE_SIZE - 224:
            self.offset_x  = len(self.tilemap[0]) * self.TILE_SIZE - 224
            
    def create_tile_rects(self, sprite_handler, display):
        rect_list = []
        
        for x in range(len(self.tilemap)):
            for y in range(len(self.tilemap[0])):
                if self.tilemap[x][y] == 1:                        
                    rect = pygame.Rect(y * self.TILE_SIZE, x * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE)
                    rect_list.append(rect)
                    
                # check for player spawn tile
                elif self.tilemap[x][y] == 2:
                    self.player.position[0] = y * self.TILE_SIZE
                    self.player.position[1] = x * self.TILE_SIZE + self.TILE_SIZE
                        
                # check for enemies! 
                elif self.tilemap[x][y] == 3:  
                    # print("enemy found!")
                    pos_x = y * self.TILE_SIZE
                    pos_y = x * self.TILE_SIZE                        
                    new_enemy = enemy.enemy(display, pos_x, pos_y, self.TILE_SIZE, sprite_handler.bunny_jump)
                    self.enemy_group.add(new_enemy)

        return rect_list
    
    def render_background(self, dt, offset_x):
        # self.bg_timer += dt
        rect = self.bg_rect.copy()
        rect.x -= offset_x / 10
        self.display.blit(self.bg_image, rect)
                
    def reset(self):
        pass
    
if __name__ == '__main__':
    pass