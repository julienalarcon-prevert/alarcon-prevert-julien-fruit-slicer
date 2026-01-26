import pygame

def draw_button(screen, text, x, y, w, h, font, mouse_pos, color=(40, 100, 40)):
    button_rect = pygame.Rect(x, y, w, h)
    is_hovered = button_rect.collidepoint(mouse_pos)
    bg_color = (color[0]+30, color[1]+30, color[2]+30) if is_hovered else color
    pygame.draw.rect(screen, bg_color, button_rect, border_radius=12)
    text_surf = font.render(text, True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=button_rect.center)
    screen.blit(text_surf, text_rect)
    return button_rect

def draw_settings_item(screen, label, value, x, y, w, h, font, mouse_pos):
    item_rect = pygame.Rect(x, y, w, h)
    is_hovered = item_rect.collidepoint(mouse_pos)
    color = (255, 255, 255) if not is_hovered else (245, 245, 245)
    pygame.draw.rect(screen, color, item_rect)
    lbl_surf = font.render(label, True, (60, 60, 60))
    screen.blit(lbl_surf, (x + 20, y + (h - lbl_surf.get_height()) // 2))
    val_color = (0, 150, 255) if value not in ["OFF", "HARD", "NON", "DIFÍCIL"] else (255, 50, 50)
    val_surf = font.render(str(value), True, val_color)
    screen.blit(val_surf, (x + w - val_surf.get_width() - 20, y + (h - val_surf.get_height()) // 2))
    pygame.draw.line(screen, (230, 230, 230), (x + 15, y + h), (x + w - 15, y + h), 1)
    return item_rect

def draw_screen(screen, background, entities, saber_img, saber_rect, state, progress, font, mouse_pos, settings, translations):
    screen.blit(background, (0, 0))
    buttons = {}
    lang = settings['langs'][settings['lang_idx']]
    t = translations[lang]

    if state == "LOADING":
        bar_w, bar_h = 400, 30
        x, y = (sw // 2) - (bar_w // 2), sh - 100
        pygame.draw.rect(screen, (100, 100, 100), (x, y, bar_w, bar_h), 2)
        fill_w = int(bar_w * (progress / 100))
        pygame.draw.rect(screen, (0, 255, 0), (x, y, fill_w, bar_h))
        
    elif state == "MENU":
        menu_w, menu_h = 550, 450
        menu_rect = pygame.Rect(0, 0, menu_w, menu_h).copy()
        menu_rect.center = (sw // 2, sh // 2)
        pygame.draw.rect(screen, (34, 139, 34), menu_rect, border_radius=25)
        cx = menu_rect.centerx - 140
        buttons['play'] = draw_button(screen, t['play'], cx, menu_rect.top + 70, 280, 65, font, mouse_pos)
        buttons['settings'] = draw_button(screen, t['settings'], cx, menu_rect.top + 170, 280, 65, font, mouse_pos)
        buttons['quit'] = draw_button(screen, t['quit'], cx, menu_rect.top + 270, 280, 65, font, mouse_pos)

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
        sound_val = t['on'] if settings['sound'] else t['off']
        diff_val = t[settings['diff_levels'][settings['diff_idx']].lower()]
        
        buttons['sound'] = draw_settings_item(screen, t['sound_label'], sound_val, set_rect.x, start_y, set_w, row_h, font, mouse_pos)
        buttons['diff'] = draw_settings_item(screen, t['diff_label'], diff_val, set_rect.x, start_y + row_h, set_w, row_h, font, mouse_pos)
        buttons['lang'] = draw_settings_item(screen, t['lang_label'], lang, set_rect.x, start_y + row_h*2, set_w, row_h, font, mouse_pos)
        buttons['back'] = draw_button(screen, t['save_back'], set_rect.centerx - 125, set_rect.bottom - 90, 250, 60, font, mouse_pos, (50, 120, 200))

    for image, rect in entities:
        screen.blit(image, rect)
    screen.blit(saber_img, saber_rect)
    pygame.display.flip()
    return buttons

pygame.init()
info = pygame.display.Info()
sw, sh = info.current_w, info.current_h
screen = pygame.display.set_mode((sw, sh))
pygame.mouse.set_visible(False)
font = pygame.font.SysFont("Arial", 26, bold=True)

bg = pygame.image.load("assets/background.png").convert()
title_img = pygame.image.load("assets/title.png").convert_alpha()
saber_raw = pygame.image.load("assets/saber.png").convert_alpha()
saber_final = pygame.transform.rotate(pygame.transform.smoothscale(saber_raw, (50, 50)), 45)

title_rect = title_img.get_rect(center=(sw // 2, sh // 2 - 280))

translations = {
    "ENGLISH": {
        "play": "PLAY", "settings": "SETTINGS", "quit": "QUIT", "config_title": "CONFIGURATION",
        "sound_label": "Sound Effects", "diff_label": "Difficulty", "lang_label": "Language",
        "save_back": "SAVE & BACK", "on": "ON", "off": "OFF", "easy": "EASY", "normal": "NORMAL", "hard": "HARD"
    },
    "FRENCH": {
        "play": "JOUER", "settings": "OPTIONS", "quit": "QUITTER", "config_title": "CONFIGURATION",
        "sound_label": "Effets Sonores", "diff_label": "Difficulté", "lang_label": "Langue",
        "save_back": "SAUVER & RETOUR", "on": "OUI", "off": "NON", "easy": "FACILE", "normal": "NORMAL", "hard": "DIFFICILE"
    },
    "SPANISH": {
        "play": "JUGAR", "settings": "AJUSTES", "quit": "SALIR", "config_title": "CONFIGURACIÓN",
        "sound_label": "Efectos de Sonido", "diff_label": "Dificultad", "lang_label": "Idioma",
        "save_back": "GUARDAR", "on": "SÍ", "off": "NO", "easy": "FÁCIL", "normal": "NORMAL", "hard": "DIFÍCIL"
    }
}

game_settings = {
    'sound': True,
    'diff_levels': ["EASY", "NORMAL", "HARD"],
    'diff_idx': 1,
    'langs': list(translations.keys()),
    'lang_idx': 0
}

state, progress, running = "LOADING", 0, True
clock = pygame.time.Clock()
buttons = {}

while running:
    mouse_pos = pygame.mouse.get_pos()
    saber_rect = saber_final.get_rect(center=mouse_pos)
    if state == "LOADING":
        progress += 2
        if progress >= 100: state = "MENU"

    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q: running = False
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

    entities = [(title_img, title_rect)] if state == "LOADING" else []
    buttons = draw_screen(screen, bg, entities, saber_final, saber_rect, state, progress, font, mouse_pos, game_settings, translations)
    clock.tick(60)

pygame.quit()