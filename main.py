
import pygame, random

WIDTH = 800
HEIGHT = 600
BLACK = (0,0,0)
WHITE = (255,255,255)

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Cody Galáctico')
clock = pygame.time.Clock()

#texto

def draw_text(surface,text,size,x,y):

    font = pygame.font.SysFont('serif', size)
    text_surface = font.render(text,True,WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surface.blit(text_surface,text_rect)



class Player (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load('assets/player.png').convert()

        self.image.set_colorkey(BLACK)  #quita lo negro de la img


        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed = 0

    def update(self):
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -5
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 5
        self.rect.x += self.speed_x

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
    def shoot (self):
        bullet = Bullet(self.rect.centerx,self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Meteoro (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(meteor_images)
        self.image.set_colorkey(BLACK)  #quita lo negro de la img
        self.rect = self.image.get_rect()

        #donde aparecen los meteoritos
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(100 - 40)
        self.speed_y = random.randrange(1,10)
        self.speed_x = random.randrange(-5,5)


    def update (self):
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        if self.rect.top > HEIGHT + 10 or self.rect.left < - 40 or self.rect.right > WIDTH + 25:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(140 - 100)
            self.speed_y = random.randrange(1,10)

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load('assets/laser1.png')
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.centerx = x
        self.speed_y = -10


    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()


background = pygame.image.load('assets/background.png').convert()

#imagens de los meteoros
meteor_images = []
meteoros_list = ['assets/meteorGrey_big1.png','assets/meteorGrey_big2.png','assets/meteorGrey_big3.png','assets/meteorGrey_big4.png','assets/meteorGrey_med1.png','assets/meteorGrey_med2.png','assets/meteorGrey_small1.png','assets/meteorGrey_small2.png','assets/meteorGrey_tiny1.png','assets/meteorGrey_tiny2.png']

for img in meteoros_list:
    meteor_images.append(pygame.image.load(img).convert())


#grupos
all_sprites = pygame.sprite.Group()
meteor_list = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)


#cantidad de meteoritos
for i in range(8):
    meteor = Meteoro()
    all_sprites.add(meteor)
    meteor_list.add(meteor)

score = 0
running = True

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #disparos
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()


    all_sprites.update()

    #colisiones - meteoro + laser
    hits = pygame.sprite.groupcollide(meteor_list,bullets,True,True)
    for hit in hits:
        score += 10
        meteor = Meteoro()
        all_sprites.add(meteor)
        meteor_list.add(meteor)

    #colisiones - jugador + meteoro

    hits = pygame.sprite.spritecollide(player,meteor_list,True)
    if hits:
        running = False


    screen.blit(background, [0,0])
    all_sprites.draw(screen)
    
    #score
    draw_text(screen,str(score),25, WIDTH //2, 10)



    pygame.display.flip()

pygame.quit()

