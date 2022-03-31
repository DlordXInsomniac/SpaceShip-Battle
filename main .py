from operator import le
import pygame
import os
pygame.font.init()

WIDTH, HEIGHT = 900,500
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

FPS = 60
VEL = 4
BULLET_VEL = 6
MAX_BULLETS = 5

FST_HIT = pygame.USEREVENT + 1
SCND_HIT = pygame.USEREVENT + 2

BORDER = pygame.Rect(WIDTH//2 - 2.5,0,5,HEIGHT)

HEALTH_FONT = pygame.font.SysFont('clarendon', 40)
WINNER_FONT = pygame.font.SysFont('motterTektura',100)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("SPACE SHOOTERS")

SPACESHIP_IMG = pygame.image.load(os.path.join('assets','battleship.png'))
SPACESHIP2 = pygame.transform.rotate(pygame.transform.scale(SPACESHIP_IMG,(60,60)),90)
SPACESHIP1 = pygame.transform.rotate(pygame.transform.scale(SPACESHIP_IMG,(60,60)),270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('assets','background.jpg')),(WIDTH,HEIGHT))

def draw_win(fst,scnd,fst_bullets,scnd_bullets,fst_health,scnd_health):
    WIN.blit(SPACE,(0,0))
    pygame.draw.rect(WIN,BLACK,BORDER)

    fst_health_text = HEALTH_FONT.render("HEALTH :"+ str(fst_health),1,WHITE) 
    scnd_health_text = HEALTH_FONT.render("HEALTH :"+ str(scnd_health),1,WHITE)
    WIN.blit(fst_health_text,(10,10))
    WIN.blit(scnd_health_text,(WIDTH - scnd_health_text.get_width() - 10,10)) 

    WIN.blit(SPACESHIP1,(fst.x,fst.y))
    WIN.blit(SPACESHIP2,(scnd.x,scnd.y))
    for bullet in fst_bullets:
        pygame.draw.rect(WIN,RED,bullet)
    for bullet in scnd_bullets:
        pygame.draw.rect(WIN,YELLOW,bullet)

    pygame.display.update()

def fst_spaceship_mov(keys_pressed,fst):
    if keys_pressed[pygame.K_a] and fst.x - VEL > 0: #LEFT
            fst.x -= VEL
    if keys_pressed[pygame.K_d] and fst.x + VEL + 60 < BORDER.x: #RIGHT
        fst.x += VEL
    if keys_pressed[pygame.K_w] and fst.y - VEL > 0: #UP
        fst.y -= VEL
    if keys_pressed[pygame.K_s] and fst.y + VEL + 60 < HEIGHT: #DOWN
        fst.y += VEL

def scnd_spaceship_mov(keys_pressed,scnd):
    if keys_pressed[pygame.K_LEFT] and scnd.x - VEL > BORDER.x + BORDER.width: #LEFT
            scnd.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and scnd.x + VEL + 60 < WIDTH: #RIGHT
        scnd.x += VEL
    if keys_pressed[pygame.K_UP] and scnd.y - VEL > 0: #UP
        scnd.y -= VEL
    if keys_pressed[pygame.K_DOWN] and scnd.y + VEL + 60 < HEIGHT: #DOWN
        scnd.y += VEL

def handle_bullets(fst_bullets,scnd_bullets,fst,scnd):
    for bullet in fst_bullets:
        bullet.x += BULLET_VEL
        if scnd.colliderect(bullet):
            pygame.event.post(pygame.event.Event(SCND_HIT))
            fst_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            fst_bullets.remove(bullet)
            

    for bullet in scnd_bullets:
        bullet.x -= BULLET_VEL
        if fst.colliderect(bullet):
            pygame.event.post(pygame.event.Event(FST_HIT))
            scnd_bullets.remove(bullet)
        elif bullet.x < 0:
            scnd_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text,1,WHITE)
    WIN.blit(draw_text,(WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    fst = pygame.Rect(100,300, 60,60) #WIDTH & HEIGHT oF Spaceship = 60
    scnd = pygame.Rect(700,300,60,60)

    fst_bullets = []
    scnd_bullets = []

    fst_health = 10
    scnd_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(fst_bullets)<MAX_BULLETS:
                    bullet = pygame.Rect(fst.x + fst.width,fst.y + fst.height//2 - 2, 8,4)
                    fst_bullets.append(bullet)

                if event.key == pygame.K_RCTRL and len(scnd_bullets)<MAX_BULLETS:
                    bullet = pygame.Rect(scnd.x,scnd.y + scnd.height//2 - 2, 8,4)
                    scnd_bullets.append(bullet)

            if event.type == SCND_HIT:
                scnd_health -= 1

            if event.type == FST_HIT:
                fst_health -= 1

        winner_text = ""
        if scnd_health <= 0:
            winner_text = "FIRST WINS"

        if fst_health <= 0:
            winner_text = "SECOND WINS"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        fst_spaceship_mov(keys_pressed,fst)
        scnd_spaceship_mov(keys_pressed,scnd)

        handle_bullets(fst_bullets,scnd_bullets,fst,scnd)

        draw_win(fst,scnd,fst_bullets,scnd_bullets,fst_health,scnd_health)

    main()

if __name__ == "__main__":
    main()