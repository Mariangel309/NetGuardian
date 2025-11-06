import pygame
import random
import math

class DataFragment:
    #Representa un fragmento de datos que cae al derrotar enemigos
    def __init__(self, pos, fragment_type, fragment_id):
        self.pos = list(pos)
        self.fragment_type = fragment_type  # 'password', 'firewall', 'masterkey'
        self.fragment_id = fragment_id
        self.velocity = [random.uniform(-2, 2), random.uniform(-4, -2)]
        self.lifetime = 0
        self.collected = False
        self.float_offset = random.random() * math.pi * 2
        
        # Colores según tipo
        self.colors = {
            'password': (100, 200, 255),    # Azul
            'firewall': (255, 150, 50),      # Naranja
            'masterkey': (255, 50, 150)      # Rosa
        }
        self.color = self.colors.get(fragment_type, (255, 255, 255))
        
    def update(self):
        """Actualiza física del fragmento"""
        self.lifetime += 1
        
        # Gravedad
        self.velocity[1] += 0.3
        self.velocity[1] = min(self.velocity[1], 5)
        
        # Fricción horizontal
        self.velocity[0] *= 0.95
        
        # Movimiento
        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]
        

        if self.lifetime > 60:
            self.pos[1] += math.sin(self.lifetime * 0.1 + self.float_offset) * 0.5
        
        return False
    
    def render(self, surf, offset=(0, 0)):
        """Renderiza el fragmento con efecto brillante"""
        x = int(self.pos[0] - offset[0])
        y = int(self.pos[1] - offset[1])
        
        # Efecto de pulso
        pulse = abs(math.sin(self.lifetime * 0.1)) * 2 + 2
        
        # Brillo exterior
        for i in range(3):
            alpha = 100 - i * 30
            size = 4 + pulse + i
            glow_surf = pygame.Surface((size * 2, size * 2))
            glow_surf.set_alpha(alpha)
            pygame.draw.circle(glow_surf, self.color, (size, size), size)
            surf.blit(glow_surf, (x - size, y - size))
        
        # Núcleo del fragmento
        pygame.draw.circle(surf, self.color, (x, y), 3)
        pygame.draw.circle(surf, (255, 255, 255), (x, y), 2)
        
        # Icono según tipo
        if self.lifetime % 60 < 30:
            icon_color = (255, 255, 255)
        else:
            icon_color = self.color
        
        pygame.draw.circle(surf, icon_color, (x, y), 1)


class DataCollectionSystem:
    #Sistema de recolección y gestión de fragmentos
    def __init__(self, game):
        self.game = game
        self.fragments = []
        self.collected_fragments = {
            'password': [],      # Nivel 0
            'firewall': [],      # Nivel 1
            'masterkey': []      # Nivel 2
        }
        self.total_required = {
            'password': 8,
            'firewall': 12,
            'masterkey': 15
        }
        
        try:
            self.font = pygame.font.Font('data/fonts/pixel_font.ttf', 10)
            self.big_font = pygame.font.Font('data/fonts/pixel_font.ttf', 14)
        except:
            self.font = pygame.font.Font(None, 12)
            self.big_font = pygame.font.Font(None, 16)
        
        # Contador de notificaciones
        self.notification = None
        self.notification_timer = 0
        
    def get_fragment_type_for_level(self, level):
        #Retorna el tipo de fragmento según el nivel
        types = {0: 'password', 1: 'firewall', 2: 'masterkey'}
        return types.get(level, 'password')
    
    def spawn_fragment(self, pos, fragment_type, fragment_id):
        #Genera un nuevo fragmento
        fragment = DataFragment(pos, fragment_type, fragment_id)
        self.fragments.append(fragment)
        
    def collect_fragment(self, fragment):
        #Recolecta un fragmento
        if fragment.fragment_id not in self.collected_fragments[fragment.fragment_type]:
            self.collected_fragments[fragment.fragment_type].append(fragment.fragment_id)
            self.fragments.remove(fragment)
            
            # Notificación
            current = len(self.collected_fragments[fragment.fragment_type])
            total = self.total_required[fragment.fragment_type]
            
            type_names = {
                'password': 'CONTRASEÑA',
                'firewall': 'FIREWALL',
                'masterkey': 'CLAVE MAESTRA'
            }
            
            self.notification = f"Fragmento {type_names[fragment.fragment_type]} {current}/{total}"
            self.notification_timer = 120
            
            # Log
            self.game.sistema_logs.agregar_log(f"Datos recuperados [{current}/{total}]", "INFO")
            
            # Check si completó el nivel
            if current >= total:
                return True  # Nivel completado
        
        return False
    
    def update(self):
        #Actualiza todos los fragmentos
        for fragment in self.fragments.copy():
            fragment.update()
            
            # Recolección por proximidad
            player_rect = self.game.player.rect()
            fragment_rect = pygame.Rect(fragment.pos[0] - 5, fragment.pos[1] - 5, 10, 10)
            
            if player_rect.colliderect(fragment_rect):
                if self.collect_fragment(fragment):
                    self.game.activate_puzzle()
        
        # Actualizar notificación
        if self.notification_timer > 0:
            self.notification_timer -= 1
    
    def render(self, surf, offset=(0, 0)):
        # Renderizar fragmentos en el mundo
        for fragment in self.fragments:
            fragment.render(surf, offset=offset)
        
        self.render_collection_ui(surf)
        
        # Notificación central
        if self.notification_timer > 0:
            self.render_notification(surf)
    
    def render_collection_ui(self, surf):
        fragment_type = self.get_fragment_type_for_level(self.game.level)
        collected = len(self.collected_fragments[fragment_type])
        total = self.total_required[fragment_type]
        
        # Posición
        x = surf.get_width() - 10
        y = 5
        
        colors = {
            'password': (100, 200, 255),
            'firewall': (255, 150, 50),
            'masterkey': (255, 50, 150)
        }
        color = colors[fragment_type]
        
        pygame.draw.circle(surf, color, (x - 25, y + 10), 4)
        pygame.draw.circle(surf, (255, 255, 255), (x - 25, y + 10), 2)
        
        text = f"{collected}/{total}"
        text_surf = self.font.render(text, True, (255, 255, 255))
        surf.blit(text_surf, (x - text_surf.get_width(), y + 5))
    
    def render_notification(self, surf):
        """Renderiza notificación de recolección"""
        if not self.notification:
            return
        

        if self.notification_timer > 100:
            alpha = 255
        elif self.notification_timer < 20:
            alpha = int((self.notification_timer / 20) * 255)
        else:
            alpha = 255
        
        text_surf = self.big_font.render(self.notification, True, (100, 255, 100))
        text_surf.set_alpha(alpha)
        

        bg_rect = text_surf.get_rect()
        bg_rect.inflate_ip(20, 10)
        bg_rect.center = (surf.get_width() // 2, 40)
        
        bg_surf = pygame.Surface(bg_rect.size)
        bg_surf.set_alpha(180)
        bg_surf.fill((0, 0, 0))
        
        surf.blit(bg_surf, bg_rect)
        surf.blit(text_surf, (bg_rect.x + 10, bg_rect.y + 5))
    
    def has_completed_level(self, level):
        fragment_type = self.get_fragment_type_for_level(level)
        collected = len(self.collected_fragments[fragment_type])
        required = self.total_required[fragment_type]
        return collected >= required
    
    def reset_level_collection(self, level):
        fragment_type = self.get_fragment_type_for_level(level)
        self.collected_fragments[fragment_type] = []
        self.fragments = []