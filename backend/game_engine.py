import pygame
import random
import string
import math

class Target:
    def __init__(self, sw, sh):
        self.sw = sw
        self.sh = sh
        self.char = random.choice(string.ascii_uppercase)
        self.radius = 30
        self.x = random.randint(100, sw - 100)
        self.y = sh + self.radius
        self.gravity = 0.5
        
        min_height = sh // 2
        max_height = 100
        target_height = random.randint(max_height, min_height)
        dist_to_travel = self.y - target_height
        
        self.vy = -math.sqrt(2 * self.gravity * dist_to_travel)
        self.vx = random.uniform(-3, 3)
        self.active = True

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        if self.y > self.sh + 100:
            self.active = False

    def draw(self, screen, font):
        pygame.draw.circle(screen, (200, 50, 50), (int(self.x), int(self.y)), self.radius)
        text_surf = font.render(self.char, True, (255, 255, 255))
        screen.blit(text_surf, (self.x - text_surf.get_width()//2, self.y - self.radius - 35))

class GameEngine:
    def __init__(self, sw, sh, bg_image):
        self.sw = sw
        self.sh = sh
        self.bg_image = bg_image
        self.targets = []
        self.font = pygame.font.SysFont("Arial", 30, bold=True)
        self.spawn_timer = 0
        self.score = 0
        self.base_spawn_delay = 60 

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            key_name = pygame.key.name(event.key).upper()
            for target in self.targets:
                if target.char == key_name:
                    target.active = False
                    self.score += 1
                    break

    def update(self):
        level = self.score // 30
        current_spawn_delay = max(15, self.base_spawn_delay - (level * 10))

        self.spawn_timer += 1
        if self.spawn_timer >= current_spawn_delay:
            self.targets.append(Target(self.sw, self.sh))
            self.spawn_timer = 0

        for target in self.targets:
            target.update()
        
        self.targets = [t for t in self.targets if t.active]

    def draw(self, screen):
        screen.blit(self.bg_image, (0, 0))
        for target in self.targets:
            target.draw(screen, self.font)
        
        level = (self.score // 30) + 1
        score_surf = self.font.render(f"Score: {self.score}  |  Level: {level}", True, (255, 255, 255))
        screen.blit(score_surf, (20, 20))