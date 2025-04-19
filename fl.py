import pygame
import random
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
ANCHO = 400
ALTO = 600
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Flappy Bird")

# Colores
BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
NEGRO = (0, 0, 0)

# Configuración del juego
GRAVEDAD = 0.25
VELOCIDAD_SALTO = -6
VELOCIDAD_TUBOS = 3
ESPACIO_TUBOS = 150  # Espacio vertical entre tubos
FRECUENCIA_TUBOS = 1500  # Milisegundos entre tubos

# Clase para el pájaro
class Pajaro(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(AZUL)
        self.rect = self.image.get_rect(center=(100, ALTO//2))
        self.velocidad = 0
        
    def saltar(self):
        self.velocidad = VELOCIDAD_SALTO
        
    def update(self):
        self.velocidad += GRAVEDAD
        self.rect.y += self.velocidad

# Clase para los tubos
class Tubo(pygame.sprite.Sprite):
    def __init__(self, invertido, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 400))
        self.image.fill(VERDE)
        self.rect = self.image.get_rect()
        if invertido:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = (x, y - ESPACIO_TUBOS//2)
        else:
            self.rect.topleft = (x, y + ESPACIO_TUBOS//2)

# Sistema de puntos
puntos = 0
fuente = pygame.font.Font(None, 36)

def mostrar_puntos():
    texto = fuente.render(f"Puntos: {puntos}", True, NEGRO)
    ventana.blit(texto, (10, 10))

# Grupos de sprites
sprites = pygame.sprite.Group()
tubos = pygame.sprite.Group()

pajaro = Pajaro()
sprites.add(pajaro)

# Temporizador para crear tubos
USEREVENT = pygame.USEREVENT
pygame.time.set_timer(USEREVENT, FRECUENCIA_TUBOS)

# Bucle principal
reloj = pygame.time.Clock()
ejecutando = True

while ejecutando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ejecutando = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pajaro.saltar()
        if event.type == USEREVENT:
            y = random.randint(200, ALTO - 200)
            tubo_superior = Tubo(True, ANCHO, y)
            tubo_inferior = Tubo(False, ANCHO, y)
            sprites.add(tubo_superior, tubo_inferior)
            tubos.add(tubo_superior, tubo_inferior)
    
    # Actualizar sprites
    sprites.update()
    
    # Mover tubos
    for tubo in tubos:
        tubo.rect.x -= VELOCIDAD_TUBOS
        if tubo.rect.right < 0:
            tubo.kill()
    
    # Detectar colisiones
    if pygame.sprite.spritecollide(pajaro, tubos, False) or pajaro.rect.top < 0 or pajaro.rect.bottom > ALTO:
        ejecutando = False
    
    # Sistema de puntos
    for tubo in tubos:
        if tubo.rect.centerx == pajaro.rect.centerx:
            puntos += 0.5  # Suma 0.5 por cada tubo (1 punto por par)
    
    # Dibujar
    ventana.fill(BLANCO)
    sprites.draw(ventana)
    mostrar_puntos()
    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
sys.exit()