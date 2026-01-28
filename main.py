import sys
import os

# Ajout des dossiers au chemin de recherche de Python
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, "frontend"))
sys.path.append(os.path.join(BASE_DIR, "backend"))

# Importation de la fonction principale après avoir configuré les chemins
from frontend.display_window import run_game

def start():
    run_game()

if __name__ == "__main__":
    start()