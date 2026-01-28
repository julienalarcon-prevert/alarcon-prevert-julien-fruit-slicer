import pygame
import os
import sys
from ui_utils import draw_button, draw_settings_item
from settings import TRANSLATIONS, DEFAULT_SETTINGS

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from backend.game_engine import GameEngine

pygame.init()
info = pygame.display.Info()
sw, sh = info.current_w, info.current_h
screen = pygame.display.set_mode((sw, sh))
pygame.mouse.set_visible(False)
font = pygame.font.SysFont("Arial", 26, bold=True)

ASSETS_PATH = os.path.join(os.path.dirname(__file__), "..", "assets")

bg = pygame.image.load(os.path.join(ASSETS_PATH, "background.png")).convert()
title_img = pygame.image.load(os.path.join(ASSETS_PATH, "title.png")).convert_alpha()
saber_raw = pygame.image.load(os.path.join(ASSETS_PATH, "saber.png")).convert_alpha()
saber_final = pygame.transform.rotate(pygame.transform.smoothscale(saber_raw, (50, 50)), 45)

menu_bg_raw = pygame.image.load(os.path.join(ASSETS_PATH, "menu.png")).convert_alpha()
menu_bg_final = pygame.transform.smoothscale(menu_bg_raw, (1200, 700))

title_rect = title_img.get_rect(center=(sw // 2, sh // 2 - 110))

game_settings = DEFAULT_SETTINGS
state, progress, running = "LOADING", 0, True
clock = pygame.time.Clock()
buttons = {}

engine = GameEngine(sw, sh, bg)

def draw_main(screen, state, progress, mouse_pos, buttons_dict):
    screen.blit(bg, (0, 0))
    lang = game_settings['langs'][game_settings['lang_idx']]
    t = TRANSLATIONS[lang]

    if state == "LOADING":
        bar_w, bar_h = 400, 30
        x, y = (sw // 2) - (bar_w // 2), sh - 100
        pygame.draw.rect(screen, (100, 100, 100), (x, y, bar_w, bar_h), 2)
        fill_w = int(bar_w * (progress / 100))
        pygame.draw.rect(screen, (0, 255, 0), (x, y, fill_w, bar_h))
        screen.blit(title_img, title_rect)
        
    elif state == "MENU":
        menu_rect = menu_bg_final.get_rect(center=(sw // 2, sh // 2))
        screen.blit(menu_bg_final, menu_rect)
        
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

    screen.blit(saber_final, saber_final.get_rect(center=mouse_pos))
    pygame.display.flip()

while running:
    mouse_pos = pygame.mouse.get_pos()
    
    if state == "LOADING":
        progress += 2
        if progress >= 100: state = "MENU"

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if state == "GAME":
            engine.handle_events(event)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                state = "MENU"
                engine = GameEngine(sw, sh, bg)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if state == "MENU":
                if buttons.get('play') and buttons['play'].collidepoint(mouse_pos): state = "GAME"
                if buttons.get('settings') and buttons['settings'].collidepoint(mouse_pos): state = "SETTINGS"
                if buttons.get('quit') and buttons['quit'].collidepoint(mouse_pos): running = False
            elif state == "SETTINGS":
                if buttons.get('sound') and buttons['sound'].collidepoint(mouse_pos):
                    game_settings['sound'] = not game_settings['sound']
                if buttons.get('diff') and buttons['diff'].collidepoint(mouse_pos):
                    game_settings['diff_idx'] = (game_settings['diff_idx'] + 1) % len(game_settings['diff_levels'])
                if buttons.get('lang') and buttons['lang'].collidepoint(mouse_pos):
                    game_settings['lang_idx'] = (game_settings['lang_idx'] + 1) % len(game_settings['langs'])
                if buttons.get('back') and buttons['back'].collidepoint(mouse_pos):
                    state = "MENU"

    if state == "GAME":
        engine.update()
        engine.draw(screen)
        
        if engine.return_to_menu:
            state = "MENU"
            engine = GameEngine(sw, sh, bg)
        pygame.display.flip()
    else:
        draw_main(screen, state, progress, mouse_pos, buttons)
    
    clock.tick(60)

pygame.quit()