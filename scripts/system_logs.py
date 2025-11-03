import pygame

class LogNode:
    """Nodo de lista enlazada para logs"""
    def __init__(self, mensaje, tipo="INFO"):
        self.mensaje = mensaje
        self.tipo = tipo
        self.siguiente = None
        self.timestamp = 0

class ListaEnlazadaLogs:
    """Lista enlazada para almacenar logs del sistema"""
    def __init__(self, max_size=5):
        self.cabeza = None
        self.tamano = 0
        self.max_size = max_size
        self.frame_actual = 0
    
    def agregar_log(self, mensaje, tipo="INFO"):
        nuevo_nodo = LogNode(mensaje, tipo)
        nuevo_nodo.timestamp = self.frame_actual
        
        if self.cabeza is None:
            self.cabeza = nuevo_nodo
        else:
            nuevo_nodo.siguiente = self.cabeza
            self.cabeza = nuevo_nodo
        
        self.tamano += 1
        
        if self.tamano > self.max_size:
            self._eliminar_ultimo()
    
    def _eliminar_ultimo(self):
        if self.cabeza is None:
            return
        
        if self.cabeza.siguiente is None:
            self.cabeza = None
            self.tamano = 0
            return
        
        actual = self.cabeza
        while actual.siguiente.siguiente is not None:
            actual = actual.siguiente
        
        actual.siguiente = None
        self.tamano -= 1
    
    def obtener_logs(self):
        logs = []
        actual = self.cabeza
        while actual is not None:
            logs.append({
                'mensaje': actual.mensaje,
                'tipo': actual.tipo,
                'edad': self.frame_actual - actual.timestamp
            })
            actual = actual.siguiente
        return logs
    
    def actualizar_frame(self):
        self.frame_actual += 1

class SistemaLogsVisual:
    """Sistema visual para logs en pantalla"""
    def __init__(self, game):
        self.game = game
        self.lista_logs = ListaEnlazadaLogs(max_size=5)
        try:
            self.font = pygame.font.Font('data/Fonts/pixel_font.ttf', 8)
        except:
            self.font = pygame.font.Font(None, 12)
        
        self.colores = {
            'INFO': (100, 200, 255),
            'WARNING': (255, 200, 100),
            'ALERT': (255, 100, 100)
        }
    
    def agregar_log(self, mensaje, tipo="INFO"):
        self.lista_logs.agregar_log(mensaje, tipo)
    
    def update(self):
        self.lista_logs.actualizar_frame()
    
    def render(self, surf):
        logs = self.lista_logs.obtener_logs()
        y_offset = surf.get_height() - 10
        
        for log in logs:
            alpha = 255
            if log['edad'] > 180:
                fade_frames = 60
                alpha = max(0, 255 - int(((log['edad'] - 180) / fade_frames) * 255))
            
            if alpha > 0:
                color = self.colores.get(log['tipo'], (255, 255, 255))
                text_surf = self.font.render(log['mensaje'], True, color)
                text_surf.set_alpha(alpha)
                
                bg_rect = text_surf.get_rect()
                bg_rect.inflate_ip(6, 4)
                bg_rect.bottomleft = (5, y_offset)
                
                bg_surf = pygame.Surface(bg_rect.size)
                bg_surf.set_alpha(150)
                bg_surf.fill((0, 0, 0))
                
                surf.blit(bg_surf, bg_rect)
                surf.blit(text_surf, (bg_rect.x + 3, bg_rect.y + 2))
                
                y_offset -= 12