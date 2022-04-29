import pygame, random, sys, os
from constantes import *

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('GalaxyCody')
clock = pygame.time.Clock()

#texto

def draw_text(surface,text,size,color,x,y):

    font = pygame.font.SysFont('serif', size, bold=True)
    text_surface = font.render(text,True,color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surface.blit(text_surface,text_rect)

#shield en pantalla
def draw_shield_bar(surface,x,y,percentage):
    BAR_LENGHT = 100
    BAR_HEIGHT = 10
    fill = (percentage / 100 ) * BAR_LENGHT
    border = pygame.Rect(x,y,BAR_LENGHT,BAR_HEIGHT)
    fill = pygame.Rect(x,y,fill,BAR_HEIGHT)
    pygame.draw.rect(surface,GREEN,fill)
    pygame.draw.rect(surface,WHITE,border,2)

# menu screen
def show_menu():
    screen.blit(menu,(0,0))
    draw_text(screen, 'Puntaje a superar: ', 27,WHITE,WIDTH // 2, HEIGHT // 2)
    draw_text (screen, 'Presiona la tecla s para comenzar', 20,BLACK,WIDTH // 2, HEIGHT * 3/4)
    pygame.display.flip()
    wait()

#game over screen
def show_game_over():
    screen.blit(background,(0,0))
    draw_text(screen, 'GAME OVER', 45,WHITE,WIDTH // 2, HEIGHT // 3)
    draw_text(screen, 'Tu puntaje fue: '+ str(score), 30,WHITE,WIDTH // 2, HEIGHT // 2)
    draw_text (screen, 'Presiona la tecla s para comenzar', 20,BLACK,WIDTH // 2, HEIGHT * 3/4)
    pygame.display.flip()
    wait()

def wait():    
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_s:
                    waiting = False

def get_high_score():
    with open('highscore.txt', 'r') as f:
        return f.read()


class Player (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load(os.path.join('assets/player2.png'))
        
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed = 0

        #barra de vida
        self.shield = 100

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
        laser_sound.play()

class Meteoro (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('assets/meteorGrey_big4.png')
        self.image.set_colorkey(BLACK)  #quita lo negro de la img
        self.rect = self.image.get_rect()

        #donde aparecen los meteoritos
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(100 - 40)
        self.speed_y = random.randrange(1,10)
        self.speed_x = random.randrange(-5,2)


    def update (self):
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        if self.rect.top > HEIGHT + 10 or self.rect.left < - 40 or self.rect.right > WIDTH + 25:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(140 - 100)
            self.speed_y = random.randrange(1,5)

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
menu =  pygame.image.load('assets/menu.png').convert()

#sonidos

laser_sound = pygame.mixer.Sound('assets/laser5.ogg')

#pantalla game over

game_over = True
running = True

####high score

try:
    highest_score = int(get_high_score())

    
except:
    highest_score = 0

#eventos
while running:

    #para pantalla game over
    if game_over:
        show_menu()
        game_over = False

        #grupos
        all_sprites = pygame.sprite.Group()
        meteor_list = pygame.sprite.Group()
        bullets = pygame.sprite.Group()

        player = Player()
        all_sprites.add(player)


        #cantidad de meteoritos
        for i in range(5):
            meteor = Meteoro()
            all_sprites.add(meteor)
            meteor_list.add(meteor)

        score = 0


    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            

        #disparos        
        elif event.type == pygame.KEYUP:
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
    #mas shield
    hits = pygame.sprite.spritecollide(player,meteor_list,True)
    for hit in hits:
        player.shield -= 25
        
        #agregar meteoro desp de ser golpeado
        meteor = Meteoro()
        all_sprites.add(meteor)
        meteor_list.add(meteor)

        #termina el juego cuando la vida es 0
        if player.shield <= 0:
            game_over = True
            show_game_over()


    screen.blit(background, [0,0])
    all_sprites.draw(screen)
    
    #score en pantalla
    draw_text(screen,'Score: ' + str(score),22,WHITE,48,15)

    #escudo en pantalla
    draw_shield_bar(screen,8,5,player.shield)
    
    ##checking high score

    if (highest_score < score):
        highest_score = score   

    
    with open('highscore.txt', 'w') as f:
        f.write(str(highest_score))

    draw_text (screen, 'Highscore: '+ str(highest_score),22,WHITE,76,38)



    pygame.display.flip()

pygame.quit()
sys.exit()