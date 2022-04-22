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
        self.image = pygame.image.load('assets/meteorGrey_med1.png').convert()
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
        if self.rect.top > HEIGHT + 10 or self.rect.left < - 25 or self.rect.right > WIDTH + 25:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(100 - 40)
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
        
        meteor = Meteoro()
        all_sprites.add(meteor)
        meteor_list.add(meteor)

    #colisiones - jugador + meteoro

    hits = pygame.sprite.spritecollide(player,meteor_list,True)
    if hits:
        running = False


    screen.blit(background, [0,0])
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()

