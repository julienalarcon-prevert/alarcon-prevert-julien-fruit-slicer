import pygame
import random
import os
from .target import Target, Monster, Glacon, Bombe, Salmon

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
        self.base_spawn_delay = 45 
        self.game_over = False
        self.return_to_menu = False
        self.is_frozen = False
        self.freeze_timer = 0
        self.available_keys = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

        
        assets_path = os.path.join(os.path.dirname(__file__), "..", "assets")
        self.slice_sound = pygame.mixer.Sound(os.path.join(assets_path, "slice.wav"))
        
        self.images = {}
        monsters = ["Owlet_Monster.png", "Dude_Monster.png", "Pink_Monster.png"]
        
        self.monsters_images = [pygame.transform.smoothscale(pygame.image.load(os.path.join(assets_path, random.choice(monsters))).convert_alpha(), (80, 80)) for f in monsters]
        self.images["GLACON"] = pygame.transform.smoothscale(pygame.image.load(os.path.join(assets_path, "glacon.png")).convert_alpha(), (80, 80))
        self.images["BOMBE"] = pygame.transform.smoothscale(pygame.image.load(os.path.join(assets_path, "bombe.png")).convert_alpha(), (80, 80))
        self.images["SALMON"] = pygame.transform.smoothscale(pygame.image.load(os.path.join(assets_path, "salmon.png")).convert_alpha(), (400, 400))
        
        self.heart_img = pygame.transform.smoothscale(pygame.image.load(os.path.join(assets_path, "heart.png")).convert_alpha(), (40, 40))

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
                    target.apply_effect(self)
                    self.slice_sound.play()
                    if isinstance(target, Glacon):
                        self.activate_freeze
                    break

    def update(self):
        if self.lives <= 0:
            self.game_over = True
            return
        
        if self.is_frozen:
            self.freeze_timer -= 1
            if self.freeze_timer <= 0:
                self.is_frozen = False

        level = self.score // 30
        delay = max(10, self.base_spawn_delay - (level * 15))

        self.spawn_timer += 1
        
        if self.spawn_timer >= delay and self.is_frozen == False and self.available_keys:
            prob = random.random()
            
            if prob < 0.1:
                new_target = Bombe(self.sw, self.sh, self.images["BOMBE"])
            elif prob < 0.05:
                new_target = Salmon(self.sw, self.sh, self.images["SALMON"])
            elif prob < 0.2:
                new_target = Glacon(self.sw, self.sh, self.images["GLACON"])
            else : 
                new_target = Monster(self.sw, self.sh, random.choice(self.monsters_images))
            
            # 🔑 Attribuer une touche unique
            new_target.char = random.choice(self.available_keys)
            self.available_keys.remove(new_target.char)

            self.targets.append(new_target)
            self.spawn_timer = 0


        for target in self.targets:
            if not self.is_frozen:
                target.update()
            
            if target.missed:
                if isinstance(target, Monster):
                    self.lives -= 1
                if target.char not in self.available_keys:
                    self.available_keys.append(target.char)
                target.active = False
                       
        
        self.targets = [t for t in self.targets if t.active]

    def activate_freeze(self):
        self.is_frozen = True
        self.freeze_timer = 180
        
        
    def draw(self, screen):
        screen.blit(self.bg_image, (0, 0))
        for t in self.targets: 
            t.draw(screen, self.font)
            
        for i in range(self.lives): 
            screen.blit(self.heart_img, (self.sw - 60 - (i * 50), 20))
        
        score_surf = self.font.render(f"Score: {self.score}  |  Lvl: {(self.score//30)+1}", True, (255, 255, 255))
        screen.blit(score_surf, (20, 20))

        if self.game_over:
            overlay = pygame.Surface((self.sw, self.sh), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0,0))
            
            over_font = pygame.font.SysFont("Arial", 80, True)
            info_font = pygame.font.SysFont("Arial", 40, False)
            
            txt = over_font.render("GAME OVER", True, (255, 50, 50))
            score_txt = info_font.render(f"Score Final: {self.score}", True, (255, 255, 255))
            retry_txt = info_font.render("Appuyez sur ENTRER", True, (200, 200, 200))
            
            screen.blit(txt, (self.sw//2 - txt.get_width()//2, self.sh//2 - 100))
            screen.blit(score_txt, (self.sw//2 - score_txt.get_width()//2, self.sh//2))
            screen.blit(retry_txt, (self.sw//2 - retry_txt.get_width()//2, self.sh//2 + 80))