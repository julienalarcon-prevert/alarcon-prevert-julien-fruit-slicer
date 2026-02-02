import pygame
from .ui_utils import UIUtils
from .settings import TRANSLATIONS

class UIManager:
    def __init__(self, assets, font):
        self.assets = assets
        self.font = font
        self.utils = UIUtils()
        self.header_font = pygame.font.SysFont("Arial", 32, bold=True)
        self.accent_color = (140, 100, 40)

    def draw(self, screen, state, progress, mouse_pos, buttons_dict, game_settings, high_score):
        screen.blit(self.assets['bg'], (0, 0))
        lang = game_settings['langs'][game_settings['lang_idx']]
        t = TRANSLATIONS[lang]
        sw, sh = screen.get_size()

        if state == "LOADING":
            self._draw_loading(screen, progress, sw, sh)
        elif state == "MENU":
            self._draw_menu(screen, t, sw, sh, mouse_pos, buttons_dict, high_score)
        elif state == "SETTINGS" or state == "PAUSE":
            self._draw_overlay_menu(screen, state, t, sw, sh, mouse_pos, buttons_dict, game_settings)

        screen.blit(self.assets['saber'], self.assets['saber'].get_rect(center=mouse_pos))

    def _draw_loading(self, screen, progress, sw, sh):
        bar_w, bar_h = 400, 30
        x, y = (sw // 2) - (bar_w // 2), sh - 100
        pygame.draw.rect(screen, (100, 100, 100), (x, y, bar_w, bar_h), 2)
        fill_w = int(bar_w * (progress / 100))
        pygame.draw.rect(screen, self.accent_color, (x, y, fill_w, bar_h))
        screen.blit(self.assets['title_img'], self.assets['title_rect'])

    def _draw_menu(self, screen, t, sw, sh, mouse_pos, buttons_dict, high_score):
        menu_rect = self.assets['menu_bg'].get_rect(center=(sw // 2, sh // 2))
        screen.blit(self.assets['menu_bg'], menu_rect)
        cx = menu_rect.centerx - 140
        
        buttons_dict['play'] = self.utils.draw_button(screen, t['play'], cx, menu_rect.top + 180, 280, 75, self.font, mouse_pos)
        buttons_dict['settings'] = self.utils.draw_button(screen, t['settings'], cx, menu_rect.top + 310, 280, 75, self.font, mouse_pos)
        buttons_dict['quit'] = self.utils.draw_button(screen, t['quit'], cx, menu_rect.top + 440, 280, 75, self.font, mouse_pos)
        
        hs_text = self.font.render(f"BEST: {high_score}", True, (255, 215, 0))
        screen.blit(hs_text, (sw // 2 - hs_text.get_width() // 2, menu_rect.top + 120))

    def _draw_overlay_menu(self, screen, state, t, sw, sh, mouse_pos, buttons_dict, game_settings):
        set_w, set_h = 500, 550
        set_rect = pygame.Rect(0, 0, set_w, set_h)
        set_rect.center = (sw // 2, sh // 2)
        pygame.draw.rect(screen, (255, 255, 255), set_rect, border_radius=30)
        
        header_rect = pygame.Rect(set_rect.x, set_rect.y, set_w, 80)
        pygame.draw.rect(screen, (240, 240, 240), header_rect, border_top_left_radius=30, border_top_right_radius=30)
        
        title_text = t['config_title'] if state == "SETTINGS" else "PAUSE"
        title_surf = self.header_font.render(title_text, True, (80, 80, 80))
        screen.blit(title_surf, (set_rect.centerx - title_surf.get_width()//2, set_rect.top + 25))
        
        if state == "SETTINGS":
            row_h, start_y = 70, set_rect.top + 80
            lang = game_settings['langs'][game_settings['lang_idx']]
            sound_val = t['on'] if game_settings['sound'] else t['off']
            diff_val = t[game_settings['diff_levels'][game_settings['diff_idx']].lower()]
            
            buttons_dict['sound'] = self.utils.draw_settings_item(screen, t['sound_label'], sound_val, set_rect.x, start_y, set_w, row_h, self.font, mouse_pos)
            buttons_dict['diff'] = self.utils.draw_settings_item(screen, t['diff_label'], diff_val, set_rect.x, start_y + row_h, set_w, row_h, self.font, mouse_pos)
            buttons_dict['lang'] = self.utils.draw_settings_item(screen, t['lang_label'], lang, set_rect.x, start_y + row_h*2, set_w, row_h, self.font, mouse_pos)
            buttons_dict['back'] = self.utils.draw_button(screen, t['save_back'], set_rect.centerx - 125, set_rect.bottom - 90, 250, 60, self.font, mouse_pos, self.accent_color)