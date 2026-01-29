import os

def get_save_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    return os.path.join(project_root, "high_score.txt")

def load_high_score():
    path = get_save_path()
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                content = f.read().strip()
                return int(content) if content else 0
        except:
            return 0
    return 0

def save_high_score(score):
    path = get_save_path()
    try:
        with open(path, "w") as f:
            f.write(str(score))
    except:
        pass