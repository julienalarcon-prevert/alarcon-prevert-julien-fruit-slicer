import pygame

class UIUtils:
    def __init__(self):
        self.white = (255, 255, 255)
        self.gray_hover = (245, 245, 245)
        self.text_dark = (60, 60, 60)
        self.border_color = (230, 230, 230)
        self.danger_color = (255, 50, 50)
        self.default_accent = (140, 100, 40)
        
        self.negatives = ["OFF", "HARD", "IMPOSSIBLE", "NON", "DIFÍCIL", "DIFFICILE"]

    def draw_button(self, screen, text, x, y, w, h, font, mouse_pos, color=None):
        if color is None:
            color = self.default_accent
            
        button_rect = pygame.Rect(x, y, w, h)
        is_hovered = button_rect.collidepoint(mouse_pos)
        
        bg_color = (min(color[0]+30, 255), min(color[1]+30, 255), min(color[2]+30, 255)) if is_hovered else color
        
        pygame.draw.rect(screen, bg_color, button_rect, border_radius=12)
        
        text_surf = font.render(text, True, self.white)
        text_rect = text_surf.get_rect(center=button_rect.center)
        screen.blit(text_surf, text_rect)
        
        return button_rect

    def draw_settings_item(self, screen, label, value, x, y, w, h, font, mouse_pos):
        item_rect = pygame.Rect(x, y, w, h)
        is_hovered = item_rect.collidepoint(mouse_pos)
        
        bg_color = self.gray_hover if is_hovered else self.white
        pygame.draw.rect(screen, bg_color, item_rect)
        
        lbl_surf = font.render(label, True, self.text_dark)
        screen.blit(lbl_surf, (x + 20, y + (h - lbl_surf.get_height()) // 2))
        
        val_str = str(value).upper()
        val_color = self.danger_color if val_str in self.negatives else self.default_accent
        
        val_surf = font.render(str(value), True, val_color)
        screen.blit(val_surf, (x + w - val_surf.get_width() - 20, y + (h - val_surf.get_height()) // 2))
        
        pygame.draw.line(screen, self.border_color, (x + 15, y + h), (x + w - 15, y + h), 1)
        
        return item_rect