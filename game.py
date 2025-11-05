import os
import sys
import math
import random
import pygame
import json

from scripts.utils import load_image, load_images, Animation
from scripts.entities import PhysicsEntity, Player, Enemy
from scripts.tilemap import Tilemap
from scripts.particle import Particle
from scripts.spark import Spark
from scripts.tutorial import TutorialSystem
from scripts.system_logs import SistemaLogsVisual


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

            print("✅ Assets cargados")
        except Exception as e:
            print(f"⚠️ Error cargando assets: {e}")
        
        return assets
    
    def load_backgrounds(self):
        backgrounds = {}
        for i in range(3):
            try:
                bg = pygame.image.load(f'data/images/backgrounds/background_{i}.png').convert()
                backgrounds[i] = pygame.transform.scale(bg, (DISPLAY_WIDTH, DISPLAY_HEIGHT))
            except:
                surf = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
                colors = [(20, 40, 60), (30, 30, 50), (10, 10, 20)]
                surf.fill(colors[i])
                backgrounds[i] = surf
        
        self.current_background = backgrounds[0]
        self.prev_background = self.current_background
        self.background_alpha = 255
        return backgrounds
    
    def load_menu_assets(self):
        menu_assets = {}
        menu_images = {
            'background': ('data/images/menu_backgrounds/primero.png', (SCREEN_WIDTH, SCREEN_HEIGHT)),
            'titulo': ('data/images/menu_backgrounds/titulo.png', (800, 500)),
            'boton_jugar': ('data/images/menu_backgrounds/jugar.png', (200, 100)),
            'boton_tienda': ('data/images/menu_backgrounds/tienda.png', (200, 100)),
            'boton_creditos': ('data/images/menu_backgrounds/creditos.png', (200, 100)),
            'boton_salir': ('data/images/menu_backgrounds/salir.png', (180, 100)),
            'icono_config': ('data/images/menu_backgrounds/configuracion.png', (120, 100)),
            'game_over': ('data/images/menu_backgrounds/gameover1.png', (800, 600))
        }
        
        for key, (path, size) in menu_images.items():
            try:
                img = pygame.image.load(path)
                menu_assets[key] = pygame.transform.scale(img, size) if size else img
            except:
                menu_assets[key] = pygame.Surface(size if size else (200, 100))
                menu_assets[key].fill((100, 100, 150))
        
        return menu_assets
    
    def save_game_data(self):
        try:
            os.makedirs('saves', exist_ok=True)
            with open('saves/save_data.json', 'w') as f:
                json.dump({
                    'level': self.level,
                    'skin': self.selected_skin,
                    'volume': self.volume
                }, f)
        except:
            pass
    
    def load_game_data(self):
        try:
            with open('saves/save_data.json', 'r') as f:
                data = json.load(f)
                self.level = data.get('level', 0)
                self.selected_skin = data.get('skin', 'player')
                self.volume = data.get('volume', 0.5)
        except:
            pass
    
    def load_level(self, map_id):
        try:
            self.tilemap.load(f'data/maps/{map_id}.json')
        except:
            print(f"Mapa {map_id} no encontrado")
            self.create_emergency_map()

        self.enemies = []
        enemy_spawners = [s for s in self.tilemap.extract([('spawners', 1)])]
        
        if self.level == 2:
            enemy_spawners = enemy_spawners[:15] if len(enemy_spawners) > 15 else enemy_spawners
            enemy_type = 'enemy2'
        elif self.level == 1:
            enemy_spawners = enemy_spawners[:12] if len(enemy_spawners) > 12 else enemy_spawners
            enemy_type = 'enemy1'
        else:
            enemy_spawners = enemy_spawners[:8] if len(enemy_spawners) > 8 else enemy_spawners
            enemy_type = 'enemy'
        
        for spawner in enemy_spawners:
            self.enemies.append(Enemy(self, spawner['pos'], (8, 15), e_type=enemy_type))
        
        for spawner in self.tilemap.extract([('spawners', 0)]):
            self.player.pos = spawner['pos']

        self.projectiles = []
        self.particles = []
        self.sparks = []
        self.scroll = [0, 0]
        self.dead = 0
        self.transition = -30

        self.prev_background = self.current_background
        self.current_background = self.backgrounds.get(self.level, self.current_background)
        self.background_alpha = 0
        
        niveles = {0: "PERÍMETRO DOMÉSTICO", 1: "RED CORPORATIVA", 2: "NÚCLEO DEL SISTEMA"}
        self.sistema_logs.agregar_log(f">>> {niveles.get(self.level, 'DESCONOCIDO')}", "INFO")
        self.sistema_logs.agregar_log(f"Hostiles: {len(self.enemies)} detectados", "ALERT")
    
    def create_emergency_map(self):
        self.tilemap.tilemap = {}
        for x in range(5, 15):
            for y in range(13, 15):
                self.tilemap.tilemap[f"{x};{y}"] = {'type': 'grass', 'variant': 1, 'pos': [x, y]}
        self.tilemap.offgrid_tiles = [
            {'type': 'spawners', 'variant': 0, 'pos': [96, 192]},
            {'type': 'spawners', 'variant': 1, 'pos': [176, 192]}
        ]
    
    def main_menu(self):
        """Menú principal simplificado"""
        play_button = Button(540, 580, 200, 60)
        quit_button = Button(540, 660, 200, 60)
        
        while True:
            self.screen.blit(self.menu_assets['background'], (0, 0))
            self.screen.blit(self.menu_assets['titulo'], (240, 50))
            
            pygame.draw.rect(self.screen, (50, 100, 200), play_button.rect)
            pygame.draw.rect(self.screen, (200, 50, 50), quit_button.rect)
            
            play_text = self.font.render('JUGAR', True, (255, 255, 255))
            quit_text = self.font.render('SALIR', True, (255, 255, 255))
            
            self.screen.blit(play_text, (play_button.rect.centerx - play_text.get_width()//2, 
                                         play_button.rect.centery - play_text.get_height()//2))
            self.screen.blit(quit_text, (quit_button.rect.centerx - quit_text.get_width()//2,
                                         quit_button.rect.centery - quit_text.get_height()//2))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if play_button.is_clicked(event):
                    if self.sonido_boton:
                        self.sonido_boton.play()
                    self.reset_game()
                    self.run()
                    return
                if quit_button.is_clicked(event):
                    pygame.quit()
                    sys.exit()
            
            pygame.display.update()
            self.clock.tick(60)
    
    def reset_game(self):
        self.level = 0
        self.load_level(self.level)
        self.player.vidas = 3
        self.player.air_time = 0
        self.player.jumps = 1
        self.player.dashing = 0
        self.dead = 0
        self.transition = 0
        self.scroll = [0, 0]
        self.movement = [False, False]
    
    def run(self):
        """Loop principal del juego"""
        tutorial_triggered = False
        
        while True:
            if self.player.vidas <= 0:
                self.main_menu()
                return
            
            # Render fondo
            self.display.blit(self.prev_background, (0, 0))
            if self.background_alpha < 255:
                bg_copy = self.current_background.copy()
                bg_copy.set_alpha(self.background_alpha)
                self.display.blit(bg_copy, (0, 0))
                self.background_alpha = min(255, self.background_alpha + 5)
            else:
                self.display.blit(self.current_background, (0, 0))

            self.screenshake = max(0, self.screenshake - 1)

            # Transición de nivel
            if not len(self.enemies):
                self.transition += 1
                if self.transition > 30:
                    if self.level == 2:
                        self.main_menu()
                        return
                    else:
                        self.level += 1
                        self.load_level(self.level)
            
            if self.transition < 0:
                self.transition += 1

            if self.dead:
                self.dead += 1
                if self.dead > 40:
                    self.player.vidas = 0
                    continue

            # Cámara
            self.scroll[0] += (self.player.rect().centerx - DISPLAY_WIDTH / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - DISPLAY_HEIGHT / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            # Render mapa
            self.tilemap.render(self.display, offset=render_scroll)

            # Enemigos
            for enemy in self.enemies.copy():
                kill = enemy.update(self.tilemap, (0, 0))
                enemy.render(self.display, offset=render_scroll)
                if kill:
                    self.enemies.remove(enemy)
                    self.enemigos_derrotados += 1
                    self.sistema_logs.agregar_log("Amenaza neutralizada", "INFO")
            
            # Jugador
            if not self.dead:
                # Tutorial nivel 1
                if self.level == 0 and not tutorial_triggered:
                    if self.movement[0] or self.movement[1]:
                        self.tutorial.trigger_tutorial('movement', 
                            (self.player.pos[0], self.player.pos[1] - 30))
                        tutorial_triggered = True
                
                self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
                self.player.render(self.display, offset=render_scroll)
                
                # UI
                for i in range(self.player.vidas):
                    self.display.blit(self.heart_img, (5 + i * 25, 5))
                
                self.display.blit(self.enemy_icon, (5, 35))
                enemy_text = self.pixel_font.render(f'x {len(self.enemies)}', True, (255, 255, 255))
                self.display.blit(enemy_text, (30, 35))
            
            # Proyectiles
            for projectile in self.projectiles.copy():
                projectile[0][0] += projectile[1]
                projectile[2] += 1
                img = self.assets['projectile']
                self.display.blit(img, (projectile[0][0] - img.get_width() / 2 - render_scroll[0], 
                                       projectile[0][1] - img.get_height() / 2 - render_scroll[1]))
                
                if self.tilemap.solid_check(projectile[0]):
                    self.projectiles.remove(projectile)
                elif projectile[2] > 360:
                    self.projectiles.remove(projectile)
                elif abs(self.player.dashing) < 50:
                    if self.player.rect().collidepoint(projectile[0]):
                        self.projectiles.remove(projectile)
                        self.player.take_damage()
                        self.sistema_logs.agregar_log("¡Integridad comprometida!", "ALERT")
                        self.screenshake = max(16, self.screenshake)
            
            # Sparks
            for spark in self.sparks.copy():
                kill = spark.update()
                spark.render(self.display, offset=render_scroll)
                if kill:
                    self.sparks.remove(spark)

            # Partículas
            for particle in self.particles.copy():
                kill = particle.update()
                particle.render(self.display, offset=render_scroll)
                if kill:
                    self.particles.remove(particle)

            # Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        if self.player.jump():
                            pass
                    if event.key == pygame.K_x:
                        self.player.dash()
                        self.sistema_logs.agregar_log("Firewall activado", "INFO")
                        
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
            
            # Actualizar sistemas
            self.tutorial.update()
            self.sistema_logs.update()
            self.tutorial.render(self.display, offset=render_scroll)
            self.sistema_logs.render(self.display)
            
            # Transición
            if self.transition:
                transition_surf = pygame.Surface(self.display.get_size())
                pygame.draw.circle(transition_surf, (255, 255, 255), 
                                 (DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2), 
                                 (30 - abs(self.transition)) * 8)
                transition_surf.set_colorkey((255, 255, 255))
                self.display.blit(transition_surf, (0, 0))

            # Screenshake y render final
            screenshake_offset = (random.random() * self.screenshake - self.screenshake / 2, 
                                random.random() * self.screenshake - self.screenshake / 2)
            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), 
                           (int(screenshake_offset[0]), int(screenshake_offset[1])))
            
            pygame.display.update()
            self.clock.tick(60)

if __name__ == '__main__':
    game = Game()
    game.main_menu()
