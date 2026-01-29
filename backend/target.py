import pygame
import random
import string
import math

class Target:
    def __init__(self, sw, sh, image):
        self.sw , self.sh = sw, sh
        self.char = random.choice(string.ascii_uppercase)
        self.original_image = image
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.time_scale = 0.8
        
        self.x = random.randint(100, sw - 100)
        self.y = sh + 50
        self.gravity = 0.3
        
        target_height = random.randint(100, sh // 2)
        dist = self.y - target_height
        self.vy = -math.sqrt(2 * self.gravity * dist)
        self.vx = random.uniform(-2, 2)
        
        self.angle = 0
        self.rot_speed = random.uniform(-5, 5)
        self.active = True
        self.missed = False
        
    def update(self):
        self.x += self.vx * self.time_scale
        self.y += self.vy * self.time_scale
        self.vy += self.gravity * self.time_scale
        self.angle += self.rot_speed
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))
        
        if self.y > self.sh + 100:
            self.active = False
            self.missed = True
            
    def draw(self, screen, font, color=(255, 255, 255)):
        screen.blit(self.image, self.rect)
        text_surf = font.render(self.char, True, color)
        screen.blit(text_surf, (self.x - text_surf.get_width()//2, self.y - 75))
        
class Monster(Target):
    def apply_effect(self, engine):
        engine.score += 1

class Glacon(Target):
    def apply_effect(self, screen, font):
        super().draw(screen, font, color=(100, 200 , 255))
    
    def apply_effect(self, engine):
        engine.activate_freeze()

class Bombe(Target):
    def draw(self, screen, font):
        super().draw(screen, font, color=(255, 50, 50))
    
    def apply_effect(self, engine):
        engine.lives -= 3
        
class Salmon(Target):
    def draw(self, screen, font, color=(255, 255, 255)):
        super().draw(screen, font, color)
    
    def apply_effect(self, engine):
        engine.activate_freeze()
        engine.lives += 1