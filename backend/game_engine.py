import pygame
import random
import string
import math
import os

class Target:
    def __init__(self, sw, sh, images):
        self.sw = sw
        self.sh = sh
        self.char = random.choice(string.ascii_uppercase)
        self.original_image = random.choice(images)
        self.image = self.original_image
        self.rect = self.image.get_rect()
        
        self.x = random.randint(100, sw - 100)
        self.y = sh + 50
        self.gravity = 0.5
        
        min_height = sh // 2
        max_height = 100
        target_height = random.randint(max_height, min_height)
        dist_to_travel = self.y - target_height
        
        self.vy = -math.sqrt(2 * self.gravity * dist_to_travel)
        self.vx = random.uniform(-3, 3)
        
        self.angle = 0
        self.rot_speed = random.uniform(-5, 5)
        
        self.active = True
        self.missed = False

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        
        self.angle += self.rot_speed
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=(int(self.x), int(self.y)))
        
        if self.y > self.sh + 100:
            self.active = False
            self.missed = True

    def draw(self, screen, font):
        screen.blit(self.image, self.rect)
        text_surf = font.render(self.char, True, (255, 255, 255))
        screen.blit(text_surf, (self.x - text_surf.get_width()//2, self.y - 70))

class GameEngine:
    def __init__(self, sw, sh, bg_image):
        self.sw = sw
        self.sh = sh
        self.bg_image = bg_image
        self.targets = []
        self.font = pygame.font.SysFont("Arial", 30, bold=True)
        self.spawn_timer = 0
        self.score = 0
        self.lives = 3
        self.base_spawn_delay = 60 
        self.game_over = False
        self.return_to_menu = False
        
        assets_path = os.path.join(os.path.dirname(__file__), "..", "assets")
        
        self.monster_images = []
        names = ["Owlet_Monster.png", "Pink_Monster.png", "Dude_Monster.png"]
        for name in names:
            img = pygame.image.load(os.path.join(assets_path, name)).convert_alpha()
            self.monster_images.append(pygame.transform.smoothscale(img, (80, 80)))
            
        heart_raw = pygame.image.load(os.path.join(assets_path, "heart.png")).convert_alpha()
        self.heart_img = pygame.transform.smoothscale(heart_raw, (40, 40))

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if self.game_over:
                if event.key == pygame.K_RETURN:
                    self.return_to_menu = True
                return

            key_name = pygame.key.name(event.key).upper()
            for target in self.targets:
                if target.char == key_name:
                    target.active = False
                    self.score += 1
                    break

    def update(self):
        if self.lives <= 0:
            self.game_over = True
            return

        level = self.score // 30
        current_spawn_delay = max(15, self.base_spawn_delay - (level * 10))

        self.spawn_timer += 1
        if self.spawn_timer >= current_spawn_delay:
            self.targets.append(Target(self.sw, self.sh, self.monster_images))
            self.spawn_timer = 0

        for target in self.targets:
            target.update()
            if target.missed:
                self.lives -= 1
        
        self.targets = [t for t in self.targets if t.active]

    def draw(self, screen):
        screen.blit(self.bg_image, (0, 0))
        
        for target in self.targets:
            target.draw(screen, self.font)
        
        for i in range(self.lives):
            screen.blit(self.heart_img, (self.sw - 60 - (i * 50), 20))
        
        level = (self.score // 30) + 1
        score_surf = self.font.render(f"Score: {self.score}  |  Level: {level}", True, (255, 255, 255))
        screen.blit(score_surf, (20, 20))

        if self.game_over:
            overlay = pygame.Surface((self.sw, self.sh), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0,0))
            over_font = pygame.font.SysFont("Arial", 80, bold=True)
            info_font = pygame.font.SysFont("Arial", 40, bold=False)
            over_surf = over_font.render("GAME OVER", True, (255, 50, 50))
            score_final_surf = info_font.render(f"Score Final: {self.score}", True, (255, 255, 255))
            hint_surf = info_font.render("Appuyez sur ENTRER pour le Menu", True, (200, 200, 200))
            screen.blit(over_surf, (self.sw//2 - over_surf.get_width()//2, self.sh//2 - 100))
            screen.blit(score_final_surf, (self.sw//2 - score_final_surf.get_width()//2, self.sh//2))
            screen.blit(hint_surf, (self.sw//2 - hint_surf.get_width()//2, self.sh//2 + 80))