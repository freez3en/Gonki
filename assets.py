import pygame
import os

IMAGE_DIR = "images"
SOUND_DIR = "sounds"

def load_image(name, width=None, height=None):
    path = os.path.join(IMAGE_DIR, name)
    image = pygame.image.load(path)
    if width and height:
        image = pygame.transform.smoothscale(image, (width, height))
    return image

def load_sound(name):
    path = os.path.join(SOUND_DIR, name)
    return pygame.mixer.Sound(path)
