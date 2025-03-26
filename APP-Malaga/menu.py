# ------ 1. IMPORTACIONES Y CONFIGURACIÓN ------
import pygame
import random
import os

# Configuración
WIDTH, HEIGHT = 800, 600
BLACK, WHITE, RED = (0, 0, 0), (255, 255, 255), (255, 0, 0)
LIVES = 3  # Vidas iniciales

# Inicialización
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('GALAGA')
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 30)

# ------ 2. CLASES ------
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10  # Velocidad hacia arriba

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:  # Elimina si sale de pantalla
            self.kill()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join('assets', 'player.png')).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed_x = 0
        self.lives = LIVES
        self.invulnerable = False
        self.invulnerable_time = 0

    def update(self):
        # Movimiento
        keystate = pygame.key.get_pressed()
        self.speed_x = 0
        if keystate[pygame.K_LEFT]: self.speed_x = -5
        if keystate[pygame.K_RIGHT]: self.speed_x = 5
        self.rect.x += self.speed_x
        # Límites de pantalla
        if self.rect.right > WIDTH: self.rect.right = WIDTH
        if self.rect.left < 0: self.rect.left = 0
        # Invulnerabilidad
        if self.invulnerable and pygame.time.get_ticks() - self.invulnerable_time > 1000:
            self.invulnerable = False

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join('assets', 'meteorGrey_big1.png')).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 10)
        self.speedx = random.randrange(-5, 5)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 25:
            self.reset()

    def reset(self):
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 10)

# ------ 3. INICIALIZACIÓN ------
all_sprites = pygame.sprite.Group()
meteors = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

for i in range(8):
    m = Meteor()
    all_sprites.add(m)
    meteors.add(m)

# ------ 4. BUCLE PRINCIPAL ------
running = True
game_over = False

while running:
    clock.tick(60)
    
    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                player.shoot()
            if event.key == pygame.K_r and game_over:
                # Reiniciar juego
                game_over = False
                player.lives = LIVES
                player.rect.centerx = WIDTH // 2
                for bullet in bullets: bullet.kill()
    
    # Actualizaciones
    if not game_over:
        all_sprites.update()
        
        # Colisiones balas-meteoritos (¡ESTA ES LA PARTE CLAVE!)
        hits = pygame.sprite.groupcollide(meteors, bullets, True, True)
        for hit in hits:
            m = Meteor()
            all_sprites.add(m)
            meteors.add(m)
        
        # Colisiones jugador-meteoritos
        hits = pygame.sprite.spritecollide(player, meteors, True)
        for hit in hits:
            if not player.invulnerable:
                player.lives -= 1
                player.invulnerable = True
                player.invulnerable_time = pygame.time.get_ticks()
                m = Meteor()
                all_sprites.add(m)
                meteors.add(m)
                if player.lives <= 0:
                    game_over = True
    
    # Dibujado
    screen.fill(BLACK)
    all_sprites.draw(screen)
    screen.blit(font.render(f"Lives: {player.lives}", True, WHITE), (WIDTH-150, 10))
    if game_over:
        screen.blit(font.render("GAME OVER - Press R", True, RED), (WIDTH//2-100, HEIGHT//2))
    
    pygame.display.flip()

pygame.quit()