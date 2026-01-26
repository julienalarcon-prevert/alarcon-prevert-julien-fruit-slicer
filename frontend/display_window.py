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
    
    # Texte de gauche (Option)
    lbl_surf = font.render(label, True, (60, 60, 60))
    screen.blit(lbl_surf, (x + 20, y + (h - lbl_surf.get_height()) // 2))
    
    # Texte de droite (Valeur)
    val_surf = font.render(value, True, (0, 150, 255))
    screen.blit(val_surf, (x + w - val_surf.get_width() - 20, y + (h - val_surf.get_height()) // 2))
    
    # Séparateur (ligne fine en bas)
    pygame.draw.line(screen, (230, 230, 230), (x + 15, y + h), (x + w - 15, y + h), 1)
    return item_rect

def draw_screen(screen, background, entities, saber_img, saber_rect, state, progress, font, mouse_pos):
    screen.blit(background, (0, 0))
    buttons = {}

    if state == "LOADING":
        bar_w, bar_h = 400, 30
        x, y = (sw // 2) - (bar_w // 2), sh - 100
        pygame.draw.rect(screen, (100, 100, 100), (x, y, bar_w, bar_h), 2)
        fill_w = int(bar_w * (progress / 100))
        pygame.draw.rect(screen, (0, 255, 0), (x, y, fill_w, bar_h))
        
    elif state == "MENU":
        menu_w, menu_h = 550, 450
        menu_rect = pygame.Rect(0, 0, menu_w, menu_h)
        menu_rect.center = (sw // 2, sh // 2)
        pygame.draw.rect(screen, (34, 139, 34), menu_rect, border_radius=25)
        
        b_w, b_h = 280, 65
        cx = menu_rect.centerx - b_w // 2
        buttons['play'] = draw_button(screen, "PLAY", cx, menu_rect.top + 70, b_w, b_h, font, mouse_pos)
        buttons['settings'] = draw_button(screen, "SETTINGS", cx, menu_rect.top + 170, b_w, b_h, font, mouse_pos)
        buttons['quit'] = draw_button(screen, "QUIT", cx, menu_rect.top + 270, b_w, b_h, font, mouse_pos)

    elif state == "SETTINGS":
        # Conteneur principal style "Card"
        set_w, set_h = 500, 550
        set_rect = pygame.Rect(0, 0, set_w, set_h)
        set_rect.center = (sw // 2, sh // 2)
        pygame.draw.rect(screen, (255, 255, 255), set_rect, border_radius=30)
        
        # Header gris foncé en haut de la carte
        header_rect = pygame.Rect(set_rect.x, set_rect.y, set_w, 80)
        pygame.draw.rect(screen, (240, 240, 240), header_rect, border_top_left_radius=30, border_top_right_radius=30)
        
        header_font = pygame.font.SysFont("Arial", 32, bold=True)
        title_surf = header_font.render("CONFIGURATION", True, (80, 80, 80))
        screen.blit(title_surf, (set_rect.centerx - title_surf.get_width()//2, set_rect.top + 25))
        
        # Items de réglages
        row_h = 70
        start_y = set_rect.top + 80
        buttons['music'] = draw_settings_item(screen, "Sound Effects", "ENABLED", set_rect.x, start_y, set_w, row_h, font, mouse_pos)
        buttons['lang'] = draw_settings_item(screen, "Dictionary", "ENGLISH", set_rect.x, start_y + row_h, set_w, row_h, font, mouse_pos)
        buttons['diff'] = draw_settings_item(screen, "Difficulty", "NORMAL", set_rect.x, start_y + (row_h*2), set_w, row_h, font, mouse_pos)
        
        # Bouton Save / Back tout en bas
        buttons['back'] = draw_button(screen, "SAVE & BACK", set_rect.centerx - 125, set_rect.bottom - 90, 250, 60, font, mouse_pos, (50, 120, 200))

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
                if buttons.get('back') and buttons['back'].collidepoint(mouse_pos): state = "MENU"

    entities = [(title_img, title_rect)] if state == "LOADING" else []
    buttons = draw_screen(screen, bg, entities, saber_final, saber_rect, state, progress, font, mouse_pos)
    clock.tick(60)

pygame.quit()