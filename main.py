import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("almost square box")

FPS = 60
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)
HEALTH_FONT = pygame.font.SysFont('timesnewroman', 15)
WIN_FONT = pygame.font.SysFont('timesnewroman', 50)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

WHITE = (255, 255, 255)
BLACK = (10, 10, 40)
RED = (40, 10, 10)
ORANGE = (200, 200, 0)
VEL = 5
BULLET_VEL = 10
MAX_BULLETS = 10
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
SHIP_WIDTH, SHIP_HEIGHT = 50, 40

YELLOW_SHIP_ORG = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SHIP_ORG, (SHIP_WIDTH, SHIP_HEIGHT)), 90)

RED_SHIP_ORG = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SHIP = pygame.transform.rotate(pygame.transform.scale(RED_SHIP_ORG, (SHIP_WIDTH, SHIP_HEIGHT)), 270)

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.fill(BLACK)
    pygame.draw.rect(WIN, RED, BORDER)
    red_health_text = HEALTH_FONT.render(str(red_health) + ' HEALTH', 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(str(yellow_health) + ' HEALTH', 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 15))
    WIN.blit(yellow_health_text, (10, 15))
    WIN.blit(YELLOW_SHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, ORANGE, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, ORANGE, bullet)

    pygame.display.update()

def draw_winner(text):
    win_screen = WIN_FONT.render(text, 1, WHITE)
    WIN.blit(win_screen, (WIDTH // 2 - win_screen.get_width() // 2, HEIGHT // 2))
    pygame.display.update()
    pygame.time.delay(5000)

def yellow_move_keys(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL < 405:
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL < 450:
        yellow.y += VEL

def red_move_keys(keys_pressed, red, red_x_vel, red_y_vel):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > 455:
        red_x_vel -= 5
        red.x += red_x_vel
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL < 860:
        red_x_vel += 5
        red.x += red_x_vel
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:
        red_y_vel -= 5
        red.y += red_y_vel
    if keys_pressed[pygame.K_DOWN] and red.y + VEL < 450:
        red_y_vel += 5
        red.y += red_y_vel

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def main():

    red = pygame.Rect(700, 210, SHIP_WIDTH, SHIP_HEIGHT)
    yellow = pygame.Rect(100, 210, SHIP_WIDTH, SHIP_HEIGHT)
    red_x_vel = 5
    red_y_vel = 5

    red_health = 10
    yellow_health = 10

    red_bullets = []
    yellow_bullets = []

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + 20, yellow.y + 20, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x - 20, red.y + 20, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        #print(red_x_vel)

        keys_pressed = pygame.key.get_pressed()
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        yellow_move_keys(keys_pressed, yellow)
        red_move_keys(keys_pressed, red, red_x_vel, red_y_vel)
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

        winner_text = ''
        if red_health <= 0:
            winner_text = "YELLOW WINS"
        if yellow_health <= 0:
            winner_text = "RED WINS"
        if winner_text != '':
            draw_winner(winner_text)
            break

    main()

if __name__ == "__main__":
   main()