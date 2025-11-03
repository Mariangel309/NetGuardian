import os
import sys
import math
import random
import pygame

from scripts.entities import PhysicsEntity, Player, Enemy
from scripts.tilemap import Tilemap
from scripts.tutorial import TutorialSystem
from scripts.system_logs import SistemaLogsVisual
from scripts.particle import Particle
from scripts.utils import load_image, load_images, Animation



DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 360
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

class Button:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
    
    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False
    

class Game:
    def __init__(self):
        pygame.init()

        self.enemigos_derrotados = 0
        self.total_enemigos = 0

        try:
            self.pixel_font = pygame.font.Font('data/fonts/pixel_font.ttf', 12)
        except:
            self.pixel_font = pygame.font.Font(None, 12)
        
        try:
            self.font = pygame.font.Font('data/fonts/static/Oswald-Medium.ttf', 40)
        except:
            self.font = pygame.font.Font(None, 40)

        # Audio
        self.volume = 0.5
        pygame.mixer.init()
        pygame.mixer.music.set_volume(self.volume)

        try:
            self.sonido_boton = pygame.mixer.Sound('data/sfx/boton.mp3') #buscar sonido de boton
            self.sonido_boton.set_volume(0.5)
        except:
            self.sonido_boton = None

        #pantalla
        pygame.display.set_caption('NetGuardian')
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #tamaño de la ventana a confirmar
        self.display = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT)) #pantalla del juego a confirmar

        self.clock = pygame.time.Clock()

        self.movement = [False, False]

        #animaciones e imagenes

        self.assets = self.load_all_assets()
        self.backgrounds = self.load_backgrounds()
        self.menu_assets = self.load_menu_assets()

        self.vida_img = self.load_ui('data/images/souls/corazon.png', (24, 24)) #buscar asset de icono de vida
        self.enemy_icon = self.load_ui('data/images/ui/enemy_icon.png', (24, 24)) #buscar asset de icono de enemigo

        # Jugador
        self.selected_skin = "player"
        self.player = Player(self, (50, 50), (8, 15), skin=self.selected_skin)
        
        # Mapa
        self.tilemap = Tilemap(self, tile_size=16)
        self.level = 0
        self.load_level(self.level)
        
        # Efectos
        self.screenshake = 0

                # Sistemas nuevos
        self.tutorial = TutorialSystem(self)
        self.sistema_logs = SistemaLogsVisual(self)
    
    def load_ui(self, path, size):
        try:
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(img, size)
        except:
            surf = pygame.Surface(size)
            surf.fill((255, 0, 255))
            return surf
    
    def load_all_assets(self):
        assets = {}
        try:
            assets['decor'] = load_images('tiles/decor')
            assets['grass'] = load_images('tiles/grass')
            assets['large_decor'] = load_images('tiles/large_decor')
            assets['stone'] = load_images('tiles/stone')
            
            assets['player'] = load_image('entities/player.png')
            assets['player/idle'] = Animation(load_images('entities/player/idle'), img_dur=6)
            assets['player/run'] = Animation(load_images('entities/player/run'), img_dur=4)
            assets['player/jump'] = Animation(load_images('entities/player/jump'))
            assets['player/slide'] = Animation(load_images('entities/player/slide'))
            assets['player/wall_slide'] = Animation(load_images('entities/player/wall_slide'))
            
            assets['skin1/idle'] = Animation(load_images('entities/skin/skin1/idle'), img_dur=6)
            assets['skin1/run'] = Animation(load_images('entities/skin/skin1/run'), img_dur=4)
            assets['skin1/jump'] = Animation(load_images('entities/skin/skin1/jump'))
            assets['skin1/slide'] = Animation(load_images('entities/skin/skin1/slide'))
            assets['skin1/wall_slide'] = Animation(load_images('entities/skin/skin1/wall_slide'))
            
            assets['skin2/idle'] = Animation(load_images('entities/skin/skin2/idle'), img_dur=6)
            assets['skin2/run'] = Animation(load_images('entities/skin/skin2/run'), img_dur=4)
            assets['skin2/jump'] = Animation(load_images('entities/skin/skin2/jump'))
            assets['skin2/slide'] = Animation(load_images('entities/skin/skin2/slide'))
            assets['skin2/wall_slide'] = Animation(load_images('entities/skin/skin2/wall_slide'))
            
            assets['enemy/idle'] = Animation(load_images('entities/enemy/idle'), img_dur=6)
            assets['enemy/run'] = Animation(load_images('entities/enemy/run'), img_dur=4)
            assets['enemy/hurt'] = Animation(load_images('entities/enemy/hurt'), img_dur=4, loop=False)
            
            assets['enemy1/idle'] = Animation(load_images('entities/enemy1/idle'), img_dur=6)
            assets['enemy1/run'] = Animation(load_images('entities/enemy1/run'), img_dur=4)
            assets['enemy1/hurt'] = Animation(load_images('entities/enemy1/hurt'), img_dur=4, loop=False)
            
            assets['enemy2/idle'] = Animation(load_images('entities/enemy2/idle'), img_dur=6)
            assets['enemy2/run'] = Animation(load_images('entities/enemy2/run'), img_dur=4)
            assets['enemy2/hurt'] = Animation(load_images('entities/enemy2/hurt'), img_dur=4, loop=False)
            
            assets['particle/particle'] = Animation(load_images('particles/particle'), img_dur=6, loop=False)
            assets['gun'] = load_image('gun.png')
            assets['projectile'] = load_image('projectile.png')
        
    


