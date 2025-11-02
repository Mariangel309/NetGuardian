import os
import sys
import math
import random
import pygame



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

        self.pixel_font = pygame.font.Font('data/fonts/pixel_font.ttf', 12)

        #Cargar la música de la pantalla de inicio aquí
        self.sonido_boton = pygame.mixer.Sound() #ruta del archivo

        self.volume = 0.5
        pygame.mixer.init()
        pygame.mixer.music.set_volume(self.volume)

        #pantalla
        pygame.display.set_caption('NetGuardian')
        self.screen = pygame.display.set_mode((664, 480)) #tamaño de la ventana a confirmar
        self.display = pygame.Surface(()) #pantalla del juego a confirmar

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('data/fonts/static/Oswald-Medium.ttf', 40)

        self.movement = [False, False]

        #animaciones e imagenes
        self.assets = {
            
        }


