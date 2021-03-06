import pygame
import random
from os import path

WIDTH = 420
HEIGHT = 690
FPS = 60

#define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
ORANGE =(244, 118, 0) 

#steup img folder
img_dir = path.join(path.dirname(__file__), "img")

class Player(pygame.sprite.Sprite):
    #sprite for the player
    def __init__(self): #initalizes the sprite
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = (WIDTH/2)
        self.rect.bottom = (HEIGHT-20)

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        self.rect.x+=self.speedx
        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH
        if self.rect.left <= 0:
            self.rect.left = 0
           
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
            
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = mob_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 10)
        self.speedx = random.randrange(-2, 2)
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT +10 or self.rect.left > WIDTH -10 or self.rect.right < 0 :
            self.rect.x = random.randrange (WIDTH - self.rect.width)
            self.rect.y = random.randrange (-100, -40)
            self.speedy = random.randrange (1, 10)
            self.speedx = random.randrange (-2, 2)

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK) 
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y +=self.speedy
        if self.rect.bottom < 0:
            self.kill()
            
            

#initalize pygame and create our window
pygame.init()
pygame.mixer.init()#allows game to have sound
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

#load images
player_img = pygame.image.load(path.join(img_dir, "Ship.png")).convert()
mob_img = pygame.image.load(path.join(img_dir, "Enemy.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir, "Lazer.png")).convert()

all_sprites = pygame.sprite.Group() 
player = Player()
all_sprites.add(player)
mobs=pygame.sprite.Group()
for i in range (10) :
    m = Mob()
    all_sprites.add(m) 
    mobs.add(m)
bullets = pygame.sprite.Group()


#Game loop
running = True
while running:
    #keep your loop running at the right speed
    clock.tick(FPS)

    #process input:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    #updates
    all_sprites.update()
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
    hits = pygame.sprite.spritecollide(player, mobs, False)
    if hits:
        running = False
    
    #render
    screen.fill(BLACK)
    all_sprites.draw(screen)
    #after drawing everything, flip the display
    pygame.display.flip()
pygame.quit()
