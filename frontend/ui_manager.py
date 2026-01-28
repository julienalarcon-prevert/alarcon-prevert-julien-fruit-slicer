import pygame
from ui_utils import draw_button, draw_settings_item
from settings import TRANSLATIONS

def draw_main(screen, state, progress, mouse_pos, buttons_dict, game_settings, assets, font):
    screen.blit(assets['bg'], (0, 0))
    lang = game_settings['langs'][game_settings['lang_idx']]
    t = TRANSLATIONS[lang]
    sw, sh = screen.get_size()

    if state == "LOADING":
        bar_w, bar_h = 400, 30
        x, y = (sw // 2) - (bar_w // 2), sh - 100
        pygame.draw.rect(screen, (100, 100, 100), (x, y, bar_w, bar_h), 2)
        fill_w = int(bar_w * (progress / 100))
        pygame.draw.rect(screen, (0, 255, 0), (x, y, fill_w, bar_h))
        screen.blit(assets['title_img'], assets['title_rect'])
        
    elif state == "MENU":
        menu_rect = assets['menu_bg'].get_rect(center=(sw // 2, sh // 2))
        screen.blit(assets['menu_bg'], menu_rect)
        cx = menu_rect.centerx - 140
        buttons_dict['play'] = draw_button(screen, t['play'], cx, menu_rect.top + 180, 280, 75, font, mouse_pos)
        buttons_dict['settings'] = draw_button(screen, t['settings'], cx, menu_rect.top + 310, 280, 75, font, mouse_pos)
        buttons_dict['quit'] = draw_button(screen, t['quit'], cx, menu_rect.top + 440, 280, 75, font, mouse_pos)

    elif state == "SETTINGS":
        set_w, set_h = 500, 550
        set_rect = pygame.Rect(0, 0, set_w, set_h)
        set_rect.center = (sw // 2, sh // 2)
        pygame.draw.rect(screen, (255, 255, 255), set_rect, border_radius=30)
        
        header_rect = pygame.Rect(set_rect.x, set_rect.y, set_w, 80)
        pygame.draw.rect(screen, (240, 240, 240), header_rect, border_top_left_radius=30, border_top_right_radius=30)
        h_font = pygame.font.SysFont("Arial", 32, bold=True)
        title_surf = h_font.render(t['config_title'], True, (80, 80, 80))
        screen.blit(title_surf, (set_rect.centerx - title_surf.get_width()//2, set_rect.top + 25))
        
        row_h, start_y = 70, set_rect.top + 80
        sound_val = t['on'] if game_settings['sound'] else t['off']
        diff_val = t[game_settings['diff_levels'][game_settings['diff_idx']].lower()]
        
        buttons_dict['sound'] = draw_settings_item(screen, t['sound_label'], sound_val, set_rect.x, start_y, set_w, row_h, font, mouse_pos)
        buttons_dict['diff'] = draw_settings_item(screen, t['diff_label'], diff_val, set_rect.x, start_y + row_h, set_w, row_h, font, mouse_pos)
        buttons_dict['lang'] = draw_settings_item(screen, t['lang_label'], lang, set_rect.x, start_y + row_h*2, set_w, row_h, font, mouse_pos)
        buttons_dict['back'] = draw_button(screen, t['save_back'], set_rect.centerx - 125, set_rect.bottom - 90, 250, 60, font, mouse_pos, (50, 120, 200))

    screen.blit(assets['saber'], assets['saber'].get_rect(center=mouse_pos))