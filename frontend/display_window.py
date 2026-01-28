import pygame
import os
import sys
from .ui_manager import draw_main
from .settings import DEFAULT_SETTINGS

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from backend.game_engine import GameEngine

def run_game():
    pygame.init()
    
    info = pygame.display.Info()
    sw, sh = info.current_w, info.current_h
    screen = pygame.display.set_mode((sw, sh))
    pygame.display.set_caption("Fruit Slicer")
    pygame.mouse.set_visible(False)
    
    font = pygame.font.SysFont("Arial", 26, bold=True)
    clock = pygame.time.Clock()

    ASSETS_PATH = os.path.join(os.path.dirname(__file__), "..", "assets")
    
    assets = {
        'bg': pygame.image.load(os.path.join(ASSETS_PATH, "background.png")).convert(),
        'title_img': pygame.image.load(os.path.join(ASSETS_PATH, "title.png")).convert_alpha(),
        'menu_bg': pygame.transform.smoothscale(
            pygame.image.load(os.path.join(ASSETS_PATH, "menu.png")).convert_alpha(), (700, 700)
        )
    }
    
    assets['title_rect'] = assets['title_img'].get_rect(center=(sw // 2, sh // 2 - 110))
    
    saber_raw = pygame.image.load(os.path.join(ASSETS_PATH, "saber.png")).convert_alpha()
    assets['saber'] = pygame.transform.rotate(pygame.transform.smoothscale(saber_raw, (50, 50)), 45)

    game_settings = DEFAULT_SETTINGS.copy()
    state = "LOADING"
    progress = 0
    running = True
    buttons = {}
    
    engine = GameEngine(sw, sh, assets['bg'])

    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        if state == "LOADING":
            progress += 2
            if progress >= 100: 
                state = "MENU"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if state == "GAME":
                engine.handle_events(event)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    state = "MENU"
                    engine = GameEngine(sw, sh, assets['bg'])
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if state == "MENU":
                    if buttons.get('play') and buttons['play'].collidepoint(mouse_pos):
                        state = "GAME"
                        pygame.mouse.set_visible(False)
                    elif buttons.get('settings') and buttons['settings'].collidepoint(mouse_pos):
                        state = "SETTINGS"
                    elif buttons.get('quit') and buttons['quit'].collidepoint(mouse_pos):
                        running = False
                        
                elif state == "SETTINGS":
                    if buttons.get('sound') and buttons['sound'].collidepoint(mouse_pos):
                        game_settings['sound'] = not game_settings['sound']
                    elif buttons.get('diff') and buttons['diff'].collidepoint(mouse_pos):
                        game_settings['diff_idx'] = (game_settings['diff_idx'] + 1) % len(game_settings['diff_levels'])
                    elif buttons.get('lang') and buttons['lang'].collidepoint(mouse_pos):
                        game_settings['lang_idx'] = (game_settings['lang_idx'] + 1) % len(game_settings['langs'])
                    elif buttons.get('back') and buttons['back'].collidepoint(mouse_pos):
                        state = "MENU"

        if state == "GAME":
            engine.update()
            engine.draw(screen)
            
            if engine.return_to_menu:
                state = "MENU"
                engine = GameEngine(sw, sh, assets['bg'])
            
            pygame.display.flip()
        else:
            draw_main(screen, state, progress, mouse_pos, buttons, game_settings, assets, font)
            pygame.display.flip()
        
        clock.tick(60)

    pygame.quit()