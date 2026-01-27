import pygame

def draw_button(screen, text, x, y, w, h, font, mouse_pos, color=(140, 100, 40)):
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