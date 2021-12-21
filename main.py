import pygame
import os
import datetime
import time
import random
import math

from pygame.constants import K_LEFT, K_RIGHT, KEYDOWN
from pygame.key import get_pressed
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1000, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Google Dinosaur Clone')

SCORE_FONT = pygame.font.SysFont('press start 2p', 30)
GAME_OVER_FONT = pygame.font.SysFont('press start 2p', 40)

FPS = 60
DINO_WIDTH = DINO_HEIGHT = 70
CACTUS_WIDTH = 50
CACTUS_HEIGHT = 70

DINO_1_IMAGE = pygame.image.load(os.path.join('assets', 'dino1.png'))
DINO_1 = pygame.transform.scale(DINO_1_IMAGE, (DINO_WIDTH, DINO_HEIGHT))
DINO_2_IMAGE = pygame.image.load(os.path.join('assets', 'dino2.png'))
DINO_2 = pygame.transform.scale(DINO_2_IMAGE, (DINO_WIDTH, DINO_HEIGHT))
CACTUS_IMAGE = pygame.image.load(os.path.join('assets', 'cactus.jpg'))
CACTUS = pygame.transform.scale(CACTUS_IMAGE, (CACTUS_WIDTH, CACTUS_HEIGHT))
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'desert.png')), (WIDTH, HEIGHT))

def draw_window(dino, cactus, score, cactus_vel, hi):
    # draw background
    WIN.blit(BACKGROUND, (0, 0))

    # draw dino
    x = (int(datetime.datetime.now().strftime('%f')) // 100000) % 2 # state changes every 0.1s(=100000us)
    if x < 1:
        WIN.blit(DINO_1, (dino.x, dino.y))
    else:
        WIN.blit(DINO_2, (dino.x, dino.y))

    # draw cactus
    for c in cactus:        
        WIN.blit(CACTUS, (c.x, c.y))

    # draw scoreboard
    temp = 'HI  ' + str(hi).zfill(5) + '  ' + str(score).zfill(5)
    draw_text = SCORE_FONT.render(temp, 1, (105, 105, 105))   
    WIN.blit(draw_text, (WIDTH - 200, 10))

    pygame.display.update()

def handle_cactus(cactus, cactus_vel):
    x = (int(datetime.datetime.now().strftime('%f')) // 100000) % 2 # state changes every 0.1s(=100000us)
    if len(cactus) == 0 or x and cactus[-1].x < 900 - cactus_vel * 37:
        decision = random.choice(range(0, 20))
        if not decision: # generate a cactus
            new_cactus = pygame.Rect(900, 262, CACTUS_WIDTH, CACTUS_HEIGHT)
            cactus.append(new_cactus)
    for c in cactus:
        c.x -= cactus_vel
        if c.x < 0:
            cactus.remove(c)

def main():
    dino = pygame.Rect(60, 270, DINO_WIDTH, DINO_HEIGHT)
    cactus = []
    cactus_vel = 15
    start_score_time = time.time()
    score = 0

    f = open("hi.txt", "r")
    hi = int(f.readline()) # high score

    clock = pygame.time.Clock()
    jump_time = -1
    jump = False
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()        

        # handle jump (take pyhsics into account)
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_SPACE]:
            if not jump:
                jump = True
                jump_time = time.time()
        if jump:
            next_y = -700 * (time.time() - jump_time) + 0.5 * 2100 * (time.time() - jump_time) ** 2 + 270
            if next_y > 270: 
                next_y = 270
                jump = False
            dino.y = next_y 

        handle_cactus(cactus, cactus_vel)
        
        score = int(time.time() - start_score_time)
        if cactus_vel < 25: cactus_vel = (score // 10) + 15 # cactus_vel++ for every 10 points

        draw_window(dino, cactus, score, cactus_vel, hi)

        # Check wheter or not the game is over
        for c in cactus:
            if not jump and c.x - dino.x - cactus_vel + 20 < DINO_WIDTH:
                run = False
                break
            elif dino.colliderect(c):
                run = False
                break
    
    # Game Over 
    wait = True
    restart = False
    draw_text = GAME_OVER_FONT.render('Press Left: Exit', 0, (105, 105, 105))   
    WIN.blit(draw_text, (WIDTH // 2 - draw_text.get_width() // 2 - 32, 100))
    draw_text = GAME_OVER_FONT.render('Press Right: Restart', 0, (105, 105, 105))   
    WIN.blit(draw_text, (WIDTH // 2 - draw_text.get_width() // 2, 150))
    pygame.display.update()
    while wait:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                wait = False
                pygame.quit() 
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    wait = False
                if event.key == K_RIGHT:
                    wait = False
                    restart = True       
    if restart: main() # restart

if __name__ == '__main__':
    main()