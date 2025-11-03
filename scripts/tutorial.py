import pygame

class TutorialMessage:
    def __init__(self, text, pos, duration=180):
        self.text = text
        self.pos = list(pos)
        self.duration = duration
        self.timer = duration
        self.alpha = 255
        try:
            self.font = pygame.font.Font('data/Fonts/pixel_font.ttf', 10)
        except:
            self.font = pygame.font.Font(None, 12)
    
    def update(self):
        self.timer -= 1
        if self.timer < 30:
            self.alpha = int((self.timer / 30) * 255)
        return self.timer <= 0
    
    def render(self, surf, offset=(0, 0)):
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_surf.set_alpha(self.alpha)
        
        bg_rect = text_surf.get_rect()
        bg_rect.inflate_ip(10, 6)
        bg_rect.center = (self.pos[0] - offset[0], self.pos[1] - offset[1])
        
        bg_surf = pygame.Surface(bg_rect.size)
        bg_surf.set_alpha(180)
        bg_surf.fill((0, 0, 0))
        
        surf.blit(bg_surf, bg_rect)
        surf.blit(text_surf, (bg_rect.x + 5, bg_rect.y + 3))

class TutorialSystem:
    def __init__(self, game):
        self.game = game
        self.messages = []
        self.triggers = {
            'movement': False,
            'jump': False,
            'dash': False,
            'enemy': False,
        }
        
    def trigger_tutorial(self, trigger_name, pos):
        if self.triggers.get(trigger_name, False):
            return
        
        messages_data = {
            'movement': "Usa ← → para moverte",
            'jump': "Presiona ↑ para saltar",
            'dash': "Presiona X para activar Firewall (Dash)",
            'enemy': "¡Amenaza detectada! Usa Firewall para eliminarla",
        }
        
        if trigger_name in messages_data:
            self.messages.append(TutorialMessage(messages_data[trigger_name], pos))
            self.triggers[trigger_name] = True
    
    def update(self):
        for msg in self.messages.copy():
            if msg.update():
                self.messages.remove(msg)
    
    def render(self, surf, offset=(0, 0)):
        for msg in self.messages:
            msg.render(surf, offset=offset)