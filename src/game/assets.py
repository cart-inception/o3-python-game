import pygame

def load_image(file_path):
    try:
        image = pygame.image.load(file_path)
        # Convert the image for faster blitting
        image = image.convert_alpha()
        return image
    except Exception as e:
        print(f"Error loading image {file_path}: {e}")
        return None

def load_sound(file_path):
    try:
        sound = pygame.mixer.Sound(file_path)
        return sound
    except Exception as e:
        print(f"Error loading sound {file_path}: {e}")
        return None

def load_assets():
    # Update the file paths as needed to point to your high quality assets.
    assets = {
        "background": load_image("assets/high_quality_background.png"),
        "player": load_image("assets/high_quality_player.png"),
        "farm": load_image("assets/high_quality_farm.png"),
        "click_sound": load_sound("assets/high_quality_click.wav"),
        "background_music": load_sound("assets/high_quality_background_music.mp3"),
    }
    return assets

assets = load_assets()