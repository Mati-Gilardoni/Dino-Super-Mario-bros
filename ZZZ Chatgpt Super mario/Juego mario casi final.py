import pygame
import os
import random

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
ANCHO, ALTO = 800, 400
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("SUPER MARIO BROS")

# Ícono
icono = pygame.image.load(os.path.join("ZZZ Chatgpt Super mario/assets", "logo.png"))
pygame.display.set_icon(icono)

# Fuente para el marcador
fuente = pygame.font.SysFont("Broadway", 22)
puntos = 0

# Cargar imágenes
IMAGEN_SUELO = pygame.image.load(os.path.join("ZZZ Chatgpt Super mario/assets", "ground.png"))
sprite_sheet = pygame.image.load(os.path.join("ZZZ Chatgpt Super mario", "mario_bros.png")).convert_alpha()
IMAGEN_NUBE = pygame.image.load(os.path.join("ZZZ Chatgpt Super mario/assets", "Nube.png"))
IMAGEN_ARBUSTO = pygame.image.load(os.path.join("ZZZ Chatgpt Super mario/assets", "arbusto.png"))
IMAGEN_NUBE = pygame.transform.scale(IMAGEN_NUBE, (120, 60))

# Obstáculo normal (animado)
IMAGEN_OBSTACULO_1 = pygame.image.load(os.path.join("ZZZ Chatgpt Super mario", "enemigo1.png"))
IMAGEN_OBSTACULO_2 = pygame.image.load(os.path.join("ZZZ Chatgpt Super mario", "enemigo2.png"))
IMAGEN_OBSTACULO_1 = pygame.transform.scale(IMAGEN_OBSTACULO_1, (60, 65))
IMAGEN_OBSTACULO_2 = pygame.transform.scale(IMAGEN_OBSTACULO_2, (60, 65))

# Obstáculo alto (estático)
IMAGEN_OBSTACULO_ALTO1 = pygame.image.load(os.path.join("ZZZ Chatgpt Super mario", "enemigo_alto1.png"))
IMAGEN_OBSTACULO_ALTO2 = pygame.image.load(os.path.join("ZZZ Chatgpt Super mario", "enemigo_alto2.png"))
IMAGEN_OBSTACULO_ALTO1 = pygame.transform.scale(IMAGEN_OBSTACULO_ALTO1, (110, 120))  # Doble altura
IMAGEN_OBSTACULO_ALTO2 = pygame.transform.scale(IMAGEN_OBSTACULO_ALTO2, (110, 120))  # Doble altura
# Sprite sheet del jugador
ANCHO_FRAME = 16
ALTO_FRAME = 16
COLUMNAS = 3
FILA = 2
frames_mario = []
for i in range(COLUMNAS):
    x = i * ANCHO_FRAME
    y = FILA * ALTO_FRAME
    frame = sprite_sheet.subsurface(pygame.Rect(x, y, ANCHO_FRAME, ALTO_FRAME))
    frames_mario.append(pygame.transform.scale(frame, (80, 96)))

class Jugador:
    def __init__(self):
        self.frames = frames_mario
        self.frame_index = 0
        self.imagen = self.frames[self.frame_index]
        self.rect = self.imagen.get_rect()
        self.rect.x = 80
        self.rect.y = ALTO - self.rect.height - 60
        self.velocidad_salto = 0
        self.saltando = False
        self.saltos_restantes = 2
        self.contador_animacion = 0

    def actualizar_animacion(self):
        self.contador_animacion += 1
        if self.contador_animacion >= 5:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.imagen = self.frames[self.frame_index]
            self.contador_animacion = 0

    def saltar(self):
        if self.saltos_restantes > 0:
            self.velocidad_salto = -17
            self.saltando = True
            self.saltos_restantes -= 1

    def actualizar(self):
        if self.saltando:
            self.velocidad_salto += 1
            self.rect.y += self.velocidad_salto
            if self.rect.y >= ALTO - self.rect.height - 60:
                self.rect.y = ALTO - self.rect.height - 60
                self.saltando = False
                self.saltos_restantes = 2
        self.actualizar_animacion()

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)

# Clase para objetos móviles
class ObjetoMovil:
    def __init__(self, imagenes, y, velocidad, animado=False):
        self.animado = animado
        if self.animado:
            self.frames = imagenes
            self.frame_index = 0
            self.contador_animacion = 0
            self.imagen = self.frames[self.frame_index]
        else:
            self.imagen = imagenes

        self.rect = self.imagen.get_rect()
        self.rect.x = ANCHO + random.randint(0, 300)
        self.rect.y = y
        self.velocidad = velocidad

    def actualizar(self):
        self.rect.x -= self.velocidad

        # Animación si es necesario
        if self.animado:
            self.contador_animacion += 1
            if self.contador_animacion >= 10:
                self.frame_index = (self.frame_index + 1) % len(self.frames)
                self.imagen = self.frames[self.frame_index]
                self.contador_animacion = 0

    def dibujar(self, ventana):
        ventana.blit(self.imagen, self.rect)

def crear_obstaculo():
    tipo = random.choice(["normal", "alto"])
    if tipo == "normal":
        return ObjetoMovil(
            [IMAGEN_OBSTACULO_1, IMAGEN_OBSTACULO_2],
            y=ALTO - IMAGEN_OBSTACULO_1.get_height() - 60,
            velocidad=10,
            animado=True
        )
    else:
        return ObjetoMovil(
            [IMAGEN_OBSTACULO_ALTO1, IMAGEN_OBSTACULO_ALTO2],
            y=ALTO - IMAGEN_OBSTACULO_ALTO1.get_height() - 60,
            velocidad=10,
            animado=True
        )


# Inicialización
jugador = Jugador()
suelo_y = ALTO - 60
nubes = [ObjetoMovil(IMAGEN_NUBE, y=random.randint(50, 150), velocidad=1.5) for _ in range(2)]
arbustos = [ObjetoMovil(IMAGEN_ARBUSTO, y=ALTO - 200, velocidad=6.5)]
obstaculos = [crear_obstaculo()]

# Bucle principal
FPS = 60
clock = pygame.time.Clock()
run = True

while run:
    clock.tick(FPS)
    puntos += 1

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            jugador.saltar()

    jugador.actualizar()

    for nube in nubes: nube.actualizar()
    for arbusto in arbustos: arbusto.actualizar()
    
    for i, obstaculo in enumerate(obstaculos):
        obstaculo.actualizar()

        # Si el obstáculo salió de la pantalla, lo reemplazamos por otro nuevo random
        if obstaculo.rect.right < 0:
            obstaculos[i] = crear_obstaculo()

    # Dibujar todo
    VENTANA.fill((135, 206, 235))
    for nube in nubes: nube.dibujar(VENTANA)
    for arbusto in arbustos: arbusto.dibujar(VENTANA)
    VENTANA.blit(IMAGEN_SUELO, (0, suelo_y))
    jugador.dibujar(VENTANA)
    for obstaculo in obstaculos: obstaculo.dibujar(VENTANA)

    texto_puntos = fuente.render(f"Puntos: {puntos}", True, (0, 0, 0))
    VENTANA.blit(texto_puntos, (ANCHO - 150, 10))

    pygame.display.update()

    # Colisiones
    for obstaculo in obstaculos:
        if jugador.rect.colliderect(obstaculo.rect):
            print("¡Game Over!")
            pygame.time.delay(1000)
            run = False
            break

pygame.quit()
