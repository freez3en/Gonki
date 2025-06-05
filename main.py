import pygame
import sys
from assets import load_image, load_sound
from ui import menu, skin_selection
from game_logic import game, level_up_screen, trophy_screen, game_over_screen

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 480, 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GAME")

img_car = load_image("Car.png", 80, 90).convert_alpha()
img_obstacle = load_image("obstacle.png", 80, 90).convert_alpha()
sound_collision = load_sound("collision.wav")
sound_nitro = load_sound("nitro.wav")
sound_level_up = load_sound("level_up.wav")
img_truck = load_image("truck.png", 80, 90).convert_alpha()
img_car_game = load_image("Car_Game.png", 80, 90).convert_alpha()

font_big = pygame.font.SysFont("Arial", 48)
font_medium = pygame.font.SysFont("Arial", 28)

clock = pygame.time.Clock()

def main():
    while True:
        start_level = menu(screen, clock, font_big, font_medium)
        player_image = skin_selection(screen, clock, font_big, img_truck, img_car_game)
        game(start_level, player_image, img_car, img_obstacle, sound_collision, sound_nitro, sound_level_up)
        break

if __name__ == "__main__":
    main()