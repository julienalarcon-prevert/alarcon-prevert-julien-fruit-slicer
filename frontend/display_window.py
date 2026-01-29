import pygame
import os
import sys
from .ui_manager import draw_main
from .settings import DEFAULT_SETTINGS
from backend.persistance import load_high_score, save_high_score
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from backend.game_engine import GameEngine

class FruitSlicer:
    def __init__(self):
        pygame.init()
        
        info = pygame.display.Info()
        self.sw, self.sh = info.current_w, info.current_h
        self.screen = pygame.display.set_mode((self.sw, self.sh))
        pygame.mouse.set_visible(False)
        pygame.display.set_caption("Fruit Slicer")
        self.clock = pygame.time.Clock()
        
        self.font = pygame.font.SysFont("Arial", 26, bold=True)
        self.assets = self._load_assets()
        self.game_settings = DEFAULT_SETTINGS.copy()
        
        self.state = "LOADING"
        self.progress = 0
        self.running = True
        self.buttons = {}
        
        self.current_high_score = load_high_score()
        self.engine = GameEngine(self.sw, self.sh, self.assets['bg'], high_score=self.current_high_score)
        
    def _load_assets(self):
        assets_path = os.path.join(os.path.dirname(__file__), "..", "assets")
        
        assets = {
            'bg': pygame.image.load(os.path.join(assets_path, "background.png")).convert_alpha(),
            'title_img': pygame.image.load(os.path.join(assets_path, "title.png")).convert_alpha(),
            'menu_bg': pygame.transform.smoothscale(
                pygame.image.load(os.path.join(assets_path, "menu.png")).convert_alpha(),
                (700, 700)
            )
        }
        assets['title_rect'] = assets['title_img'].get_rect(center=(self.sw // 2, self.sh // 2 - 110))
        saber_raw = pygame.image.load(os.path.join(assets_path, "saber.png")).convert_alpha()
        assets['saber'] = pygame.transform.rotate(pygame.transform.smoothscale(saber_raw, (50, 50)), 45)
        
        return assets
        
    def _reset_engine(self):
        current_diff = self.game_settings['diff_levels'][self.game_settings['diff_idx']]
        self.engine = GameEngine(
            self.sw,
            self.sh,
            self.assets['bg'],
            difficulty = current_diff,
            high_score = self.current_high_score
        )
    
    def _handle_event(self):
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if self.state == "GAME":
                self.engine.handle_events(event)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.state = "MENU"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_menu_clicks(event, mouse_pos)
                
    def _handle_menu_clicks(self, event, mouse_pos):
        if self.state == "MENU":
            if self.buttons.get('play') and self.buttons['play'].collidepoint(mouse_pos):
                self._reset_engine()
                self.state = "GAME"
            elif self.buttons.get('settings') and self.buttons['settings'].collidepoint(mouse_pos):
                self.state = "SETTINGS"
            elif self.buttons.get('quit') and self.buttons['quit'].collidepoint(mouse_pos):
                self.running = False
               
        elif self.state == "SETTINGS":
            if self.buttons.get('sound') and self.buttons['sound'].collidepoint(mouse_pos):
                self.game_settings['sound'] = not self.game_settings['sound']
            elif self.buttons.get('diff') and self.buttons['diff'].collidepoint(mouse_pos):
                self.game_settings['diff_idx'] = (self.game_settings['diff_idx'] + 1) % len(self.game_settings['diff_levels'])
            elif self.buttons.get('lang') and self.buttons['lang'].collidepoint(mouse_pos):
                self.game_settings['lang_idx'] = (self.game_settings['lang_idx'] + 1) % len(self.game_settings['langs'])
            elif self.buttons.get('back') and self.buttons['back'].collidepoint(mouse_pos):
                self.state = "MENU"
                
    def _update(self):
        if self.state == "LOADING":
            self.progress += 1
            if self.progress >= 100:
                self.state = "MENU"
       
        if self.state == "GAME":
            self.engine.update()
           
            if self.engine.score > self.current_high_score:
                self.current_high_score = self.engine.score
            
            if self.engine.return_to_menu:
                self.state = "MENU"
                self._reset_engine()
                
    def _draw(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.state == "GAME":
            self.engine.draw(self.screen)
        else:
            draw_main(
                self.screen, self.state, self.progress, mouse_pos,
                self.buttons, self.game_settings, self.assets,
                self.font, self.current_high_score
            )
        pygame.display.flip()
        
    def run(self):
        while self.running:
            self._handle_event()
            self._update()
            self._draw()
            self.clock.tick(60)
        pygame.quit()

def run_game():
    app = FruitSlicer()
    app.run()        