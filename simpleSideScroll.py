import pygame
pygame.font.init()
pygame.mixer.init()
pygame.init()

#SIMPLE SIDE SCROLLER

print ("Hello world")

#generate the surface
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game!")

#rgb colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

#game floor
FLOOR = pygame.Rect(0, HEIGHT//1.3, WIDTH, 5)

#sound assets
BULLET_HIT_SOUND = pygame.mixer.Sound('Grenade+1.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound('Gun+Silencer.mp3')

#text fonts
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

#fps
FPS = 60

#velocity
VEL = 5
BULLET_VEL = 7

#Max bullets per ship
MAX_BULLETS = 3

#collision events and action variables

REAPER_HIT = pygame.USEREVENT + 1
ENEMY_HIT = pygame.USEREVENT + 2

#Sprite dimensions
REAPER_WIDTH, REAPER_HEIGHT = 125, 115
WARRIOR_WIDTH, WARRIOR_HEIGHT = 105, 105

#assets
#REAPER = pygame.image.load('reaper.png')
#REAPER = pygame.transform.scale_by(REAPER, .5)


#ENEMY_SPACESHIP = pygame.transform.flip(pygame.image.load('warrior.png'), True, False)
#ENEMY_SPACESHIP = pygame.transform.scale_by(ENEMY_SPACESHIP, .5)


BACKGROUND = pygame.transform.scale(pygame.image.load('pinkNeonPygameBackground.png'), (WIDTH, HEIGHT))

#character class
class Character(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type
        self.speed = speed
        self.direction = 1
        self.flip = False
        img = pygame.image.load(f'{self.char_type}.png')
        self.image = pygame.transform.scale_by((pygame.transform.flip(img, True, False)), scale)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)


    def move(self, moving_left, moving_right):
        #reset movement variables
        dx = 0
        dy = 0
        
        #assign movement variables if moving left or right
        if moving_left: # LEFT
            dx = -self.speed
            self.flip = False
            self.direction = -1
        if moving_right: # RIGHT
            dx = self.speed
            self.flip = True
            self.direction = 1

        #update rect position
        self.rect.x += dx
        self.rect.y += dy

    def draw(self):
        WIN.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


def draw_window(enemy, reaper, enemy_bullets, reaper_bullets, enemy_health, reaper_health):
        WIN.blit(BACKGROUND, (0, 0))
        pygame.draw.rect(WIN, BLACK, FLOOR)

        #enemy_health_text = HEALTH_FONT.render("Health: " + str(enemy_health), 1, WHITE)
        reaper_health_text = HEALTH_FONT.render("Health: " + str(reaper_health), 1, WHITE)
        #WIN.blit(enemy_health_text, (WIDTH - enemy_health_text.get_width() - 10, 10))
        WIN.blit(reaper_health_text, (10, 10))

        #WIN.blit(REAPER, (reaper.x, reaper.y))
        #WIN.blit(ENEMY_SPACESHIP, (enemy.x, enemy.y))
        enemy.draw()
        reaper.draw()

        for bullet in enemy_bullets:
            pygame.draw.rect(WIN, RED, bullet)

        for bullet in reaper_bullets:
            pygame.draw.rect(WIN, YELLOW, bullet)

        pygame.display.update()

def handle_bullets(reaper_bullets, enemy_bullets, reaper, enemy):
    for bullet in reaper_bullets:
        bullet.x += BULLET_VEL
        if enemy.colliderect(bullet):
            pygame.event.post(pygame.event.Event(ENEMY_HIT))
            reaper_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            reaper_bullets.remove(bullet)

    for bullet in enemy_bullets:
        bullet.x -= BULLET_VEL
        if reaper.colliderect(bullet):
            pygame.event.post(pygame.event.Event(REAPER_HIT))
            enemy_bullets.remove(bullet)
        elif bullet.x < 0:
            enemy_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    
    reaper = Character('reaper',200, 327, .5, VEL)
    enemy = Character('warrior',700, 340, .5, VEL)

    moving_left = False
    moving_right = False

    enemy_bullets = []
    reaper_bullets = []

    enemy_health = 10
    reaper_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)

        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                #left/right
                if event.key == pygame.K_a:
                    moving_left = True
                if event.key == pygame.K_d:
                    moving_right = True

                #jump...


                #bullet fire
                #if event.key == pygame.K_LCTRL and len(reaper_bullets) < MAX_BULLETS:
                    #bullet = pygame.Rect(reaper.x + reaper.width, reaper.y + reaper.height//2 -2, 10, 5)
                    #reaper_bullets.append(bullet)
                    #BULLET_FIRE_SOUND.play()

                #if event.key == pygame.K_RCTRL and len(enemy_bullets) < MAX_BULLETS:
                    #bullet = pygame.Rect(enemy.x, enemy.y + enemy.height//2 -2, 10, 5)
                    #enemy_bullets.append(bullet)
                    #BULLET_FIRE_SOUND.play()

                #escape
                if event.key == pygame.K_ESCAPE:
                    break

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    moving_left = False
                if event.key == pygame.K_d:
                    moving_right = False

            
            if event.type == ENEMY_HIT:
                enemy_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == REAPER_HIT:
                reaper_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if enemy_health <= 0:
            winner_text = "Reaper Wins!"
        if reaper_health <= 0:
            winner_text = "Enemy Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break


        #keys_pressed = pygame.key.get_pressed()
        #reaper_handle_movement(keys_pressed, reaper)
        #enemy_handle_movement(keys_pressed, enemy)
        reaper.move(moving_left, moving_right)
        
        handle_bullets(reaper_bullets, enemy_bullets, reaper, enemy)

        draw_window(enemy, reaper, enemy_bullets, reaper_bullets, enemy_health, reaper_health)
        

    main()


if __name__ == "__main__":
    main()