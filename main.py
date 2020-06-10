# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 11:15:24 2020

@author: Eric
"""

import pygame

pygame.init()

# constants
FPS = 60

# colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
WATER = (176, 233, 252)

#bricks
TILES_PER_ROW = 10
NUM_ROWS = 5
#BLANK_ROWS = 2

# game stats
score = 0
lives = 100
game_over = False

# screen and clock setup
screen = pygame.display.set_mode((1280, 960))
screen_rect = screen.get_rect()
clock = pygame.time.Clock()

# character speed
char_speed = 5
boat_speed = 5

# ball sprite class
# sets size, color, starting position and speed
class Ship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        ship_image = pygame.image.load('assets\ship.png').convert_alpha()
        self.image = pygame.transform.scale(ship_image, (50, 50))
        self.rect = self.image.get_rect()
        self.reset()
 
    def reset(self):
        self.rect.center = screen_rect.center
        self.x_speed = 0
        self.y_speed = 0
        self.died = False

    # prevents the ball from bouncing off the screen   
    def update(self):
        if self.rect.right >= screen_rect.right:
            self.x_speed = -1
        if self.rect.left <= screen_rect.left:
            self.x_speed = 1
        if self.rect.top <= screen_rect.top:
            self.y_speed = 1
        if self.rect.bottom >= screen_rect.bottom:
            self.lost = True

    # updates speed
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

# paddle class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()      
        player_image = pygame.image.load('assets\pirate.png').convert_alpha()
        self.image = pygame.transform.scale(player_image, (30, 30))
        self.rect = self.image.get_rect()
        self.reset()
    
    def reset(self):
        self.rect.center = screen_rect.center
        self.x_speed = 0
        self.y_speed = 0
        self.died = False
    
    def update(self):
        keys = pygame.key.get_pressed()

        # allows paddle to be moved with left and right arrow keys
        if keys[pygame.K_RIGHT]:
            self.rect.x += char_speed
        if keys[pygame.K_LEFT]:
            self.rect.x -= char_speed
        if keys[pygame.K_UP]:
            self.rect.y -= char_speed
        if keys[pygame.K_DOWN]:
            self.rect.y += char_speed

        if keys[pygame.K_d]:
            self.rect.x += char_speed
        if keys[pygame.K_a]:
            self.rect.x -= char_speed
        if keys[pygame.K_w]:
            self.rect.y -= char_speed
        if keys[pygame.K_s]:
            self.rect.y += char_speed
            
        # prevents paddle from leaving screen
#        if self.rect.right >= screen_rect.right:
#            self.rect.right = screen_rect.right
#            
#        if self.rect.left <= screen_rect.left:
#            self.rect.left = screen_rect.left
#            
#        if self.rect.bottom <= screen_rect.bottom:
#            self.rect.bottom = screen_rect.bottom   
#            
#        if self.rect.top >= screen_rect.top:
#            self.rect.top = screen_rect.top

class Sand(pygame.sprite.Sprite):
    def __init__(self, row, col):
        super().__init__()
        sand_image = pygame.image.load('assets\sand.png').convert_alpha()
        
        # calculate new size based on TILES_PER_ROW
        tile_width = round(screen_rect.width / TILES_PER_ROW)
        orig_size = sand_image.get_rect()
        scale_factor = (tile_width / orig_size.width)
        tile_height = round(orig_size.height * scale_factor)
        new_size = (tile_width, tile_height)
 
        
        # scale the image
        self.image = pygame.transform.scale(sand_image, new_size)
        self.rect = self.image.get_rect()
        
        # position the bricks
#        row += BLANK_ROWS
        self.rect.x = col * tile_width
        self.rect.y = row * tile_height

# creates a group for all sprites
all_sprites = pygame.sprite.Group()
#sand_tiles = pygame.sprite.Group()

# instantiate the brick class, add brick to sprite group
for row in range(0, NUM_ROWS):
    for col in range(0, TILES_PER_ROW):
        brick = Sand(row,col)
        all_sprites.add(brick)
        #sand_tiles.add(brick)

# instantiate the ship class, add ship to sprite group
ship = Ship()
all_sprites.add(ship)

# instantiate the player class, add player to sprite group
player = Player()
all_sprites.add(player)


        
def draw_text(surface, text, pos=(0,0), color=WHITE, font_size=20, anchor='topleft'):
    arial = pygame.font.match_font('arial')
    font = pygame.font.Font(arial, font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    setattr(text_rect, anchor, pos)
    surface.blit(text_surface, text_rect)

# while loop that runs the game
running = True
while running:
    # sets the clock tick rate to our FPS constant
    clock.tick(FPS)

    # allows the game to be closed and quit the program on clicking the X
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if game_over:
        screen.fill(BLACK)
        draw_text(screen, "GAME OVER", screen_rect.center, font_size=80, anchor="center")
    
    # updates the sprites group on each tick of the game
    else:
        all_sprites.update()    
    
        
        # reset ball if it passes below the bottom of screen
        if ship.died:
            lives -= 1
            if lives == 0:
                game_over = True
            ship.reset()
        
        # check for ball hitting bricks, bounce down if it did
#        collide_brick = pygame.sprite.spritecollideany(ship, bricks)
#        if collide_brick:
#            score += 1
#            collide_brick.kill()
#            ship.y_speed *= -1
        
        # fills the background with black
        screen.fill(WATER)
        
        # draws the sprites on screen
        all_sprites.draw(screen)
        
        score_text = f"Score: {score} / Lives: {lives}"
        draw_text(screen, score_text, (8, 8))
        
    #flips the display
#    pygame.display.flip()
    
    pygame.display.update() 

pygame.quit()