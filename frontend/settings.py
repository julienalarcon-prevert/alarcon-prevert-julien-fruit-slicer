TRANSLATIONS = {
    "ENGLISH": {
        "play": "PLAY", "settings": "SETTINGS", "quit": "QUIT", "config_title": "CONFIGURATION",
        "sound_label": "Sound Effects", "diff_label": "Difficulty", "lang_label": "Language",
        "save_back": "SAVE & BACK", "on": "ON", "off": "OFF", "easy": "EASY", "normal": "NORMAL", "hard": "HARD", "impossible" : "IMPOSSIBLE"
    },
    "FRENCH": {
        "play": "JOUER", "settings": "OPTIONS", "quit": "QUITTER", "config_title": "CONFIGURATION",
        "sound_label": "Effets Sonores", "diff_label": "Difficulté", "lang_label": "Langue",
        "save_back": "SAUVER & RETOUR", "on": "OUI", "off": "NON", "easy": "FACILE", "normal": "NORMAL", "hard": "DIFFICILE", "impossible" : "IMPOSSIBLE"
    },
    "SPANISH": {
        "play": "JUGAR", "settings": "AJUSTES", "quit": "SALIR", "config_title": "CONFIGURACIÓN",
        "sound_label": "Efectos de Sonido", "diff_label": "Dificultad", "lang_label": "Idioma",
        "save_back": "GUARDAR", "on": "SÍ", "off": "NO", "easy": "FÁCIL", "normal": "NORMAL", "hard": "DIFÍCIL", "impossible" : "IMPOSSIBLE"
    }
}

DEFAULT_SETTINGS = {
    'sound': True,
    'diff_levels': ["EASY", "NORMAL", "HARD", "IMPOSSIBLE"],
    'diff_idx': 1,
    'langs': list(TRANSLATIONS.keys()),
    'lang_idx': 0
}