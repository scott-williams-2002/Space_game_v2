#Space Battle Game by Scott Williams 

import pygame
import os

pygame.font.init()
pygame.mixer.init()

#set up screen 

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NFT Game")

# colors 

WHITE = (255,255,255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BACKGROUND = (200, 200, 250)

BORDER = pygame.Rect(450, 0, 10, HEIGHT)

#mp3 sound variables declared 

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'explosion.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'lazer.mp3'))
MISSLE_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'mis.mp3'))
WINNER_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'winner_sound.mp3'))


#declares the font's sizes and shapes 

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

#variables 

FPS = 60
VEL = 5
BULLET_VEL = 10
MAX_BULLETS = 5
MAX_MISSLES = 1  

# event handlers

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

#loads images

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'yellow_spaceship_2.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (100, 55)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'red_spaceship_2.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (100, 55)), 270)


#draws window with bullet and missle lists 

def draw_window(yellow, red, red_bullets, yellow_bullets, red_health, yellow_health, red_mis, yellow_mis):
    WIN.fill(BACKGROUND)
    pygame.draw.rect(WIN, BLACK, BORDER)

    #healh  displays 

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, BLACK)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, BLACK)
    WIN.blit(red_health_text, (10, 10))
    WIN.blit(yellow_health_text, (900 - yellow_health_text.get_width() - 10, 10))

    # blits ship to the screen at FPS of 60

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    # draws bullets and updates at 60 FPS

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    for bullet in red_mis:
        pygame.draw.rect(WIN, (185,12,252), bullet)

    for bullet in yellow_mis:
        pygame.draw.rect(WIN, (0,0,0), bullet)
    pygame.display.update()

# handles yellow keypress movement 

def yellow_handle_movement(keys_pressed,yellow):
    if keys_pressed[pygame.K_LEFT] and yellow.x - VEL > 455:#left 
        yellow.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and yellow.x + VEL < 845:#right
        yellow.x += VEL
    if keys_pressed[pygame.K_UP] and yellow.y - VEL > 0: #up
        yellow.y -= VEL
    if keys_pressed[pygame.K_DOWN] and yellow.y - VEL < 390: #down
        yellow.y += VEL

# handles red keypress movement 

def red_handle_movement(keys_pressed,red):
    if keys_pressed[pygame.K_a] and red.x - VEL > 0:#left 
        red.x -= VEL
    if keys_pressed[pygame.K_d] and red.x + VEL < 400:#right
        red.x += VEL
    if keys_pressed[pygame.K_w] and red.y - VEL > 0: #up
        red.y -= VEL
    if keys_pressed[pygame.K_s] and red.y - VEL < 390: #down
        red.y += VEL

#handles bullets and missles 

def handle_bullets(yellow_bullets, red_bullets, yellow, red, yellow_mis, red_mis):
    for bullet in red_bullets:
        bullet.x += BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        
        elif bullet.x > 900:
            red_bullets.remove(bullet)

    for bullet in yellow_bullets:
        bullet.x -= BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x < 0:
            yellow_bullets.remove(bullet)


    for bullet in yellow_mis:
        bullet.x -= BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_mis.remove(bullet)
        elif bullet.x < 0:
            yellow_mis.remove(bullet)

    for bullet in red_mis:
        bullet.x += BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_mis.remove(bullet)
        elif bullet.x > 900:
            red_mis.remove(bullet)

    
#draws winner and restarts the game after a 5 second delay 

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, BLACK)
    WIN.blit(draw_text, (900/2 - draw_text.get_width()/2, 500/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)
    



    


def main():

    yellow = pygame.Rect(600, 100, 55, 100)
    red = pygame.Rect(0, 100, 55, 100)

    yellow_mis = []
    red_mis = []

    red_bullets = []
    yellow_bullets = []
    
    

    red_health = 100
    yellow_health = 100

    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x + red.width, red.y + red.height//2 -2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_0 and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x, yellow.y + yellow.height//2 -2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_2 and len(red_mis) < MAX_MISSLES:
                    bullet = pygame.Rect(red.x + red.width, red.y + red.height//2 -2, 10, 5)
                    red_mis.append(bullet)
                    MISSLE_FIRE_SOUND.play()

                if event.key == pygame.K_9 and len(yellow_mis) < MAX_MISSLES:
                    bullet = pygame.Rect(yellow.x, yellow.y + yellow.height//2 -2, 10, 5)
                    yellow_mis.append(bullet)
                    MISSLE_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"
            WINNER_SOUND.play()

        if yellow_health <= 0:
            winner_text = "Red Wins!"
            WINNER_SOUND.play()
        
        if winner_text != "":
            draw_winner(winner_text)
            break


        
        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red, yellow_mis, red_mis)

        draw_window(yellow, red, red_bullets, yellow_bullets, red_health, yellow_health, red_mis, yellow_mis)
        




    main()


if __name__ == "__main__":
    main()


