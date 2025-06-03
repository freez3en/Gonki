import pygame
import sys
from assets import load_image, load_sound
from ui import menu
from game_logic import game, level_up_screen, trophy_screen, game_over_screen

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 480, 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GAME")

font_big = pygame.font.SysFont("Arial", 48)
font_medium = pygame.font.SysFont("Arial", 28)

clock = pygame.time.Clock()

def main():
    while True:
        start_level = menu(screen, clock, font_big, font_medium)
        print(f"Выбран уровень: {start_level}")
        break

if __name__ == "__main__":
    main()