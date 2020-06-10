# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 17:12:29 2020

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

# game stats
score = 0
lives = 3
game_over = False

# screen and clock setup
screen = pygame.display.set_mode((600, 800))
screen_rect = screen.get_rect()
clock = pygame.time.Clock()

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
    
        # bounce ball if it hits paddle
        if pygame.sprite.collide_rect(ball, paddle):
            ball.y_speed = -5
        
        # reset ball if it passes below the bottom of screen
        if ball.lost:
            lives -= 1
            if lives == 0:
                game_over = True
            ball.reset()
        
        # check for ball hitting bricks, bounce down if it did
        collide_brick = pygame.sprite.spritecollideany(ball, bricks)
        if collide_brick:
            score += 1
            collide_brick.kill()
            ball.y_speed *= -1
        
        # fills the background with black
        screen.fill(BLACK)
        
        # draws the sprites on screen
        all_sprites.draw(screen)
        
        score_text = f"Score: {score} / Lives: {lives}"
        draw_text(screen, score_text, (8, 8))
        
        #flips the display
    pygame.display.flip()

pygame.quit()