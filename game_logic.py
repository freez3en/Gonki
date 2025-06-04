import pygame

WIDTH, HEIGHT = 480, 640
LANE_WIDTH = WIDTH // 4
LANES_X = [LANE_WIDTH * i + LANE_WIDTH // 2 for i in range(4)]

BASE_SPEED = 5

class Player:
    def __init__(self, image):
        self.lane = 1
        self.x = LANES_X[self.lane]
        self.y = HEIGHT - 100
        self.width = 50
        self.height = 90
        self.speed = BASE_SPEED
        self.image = image

    def move_left(self):
        if self.lane > 0:
            self.lane -= 1

    def move_right(self):
        if self.lane < 3:
            self.lane += 1

    def update(self):
        target_x = LANES_X[self.lane]
        if abs(self.x - target_x) < 5:
            self.x = target_x
        elif self.x < target_x:
            self.x += 10
        else:
            self.x -= 10

    def draw(self, surface):
        rect = self.image.get_rect(center=(self.x, self.y))
        surface.blit(self.image, rect)

class Obstacle:
    def __init__(self, lane, speed, kind, img_obstacle, img_car):
        self.lane = lane
        self.x = LANES_X[lane]
        self.y = -100
        self.speed = speed
        self.kind = kind
        self.width = 50
        self.height = 90
        self.image = img_obstacle if kind == 0 else img_car

    def update(self):
        self.y += self.speed

    def draw(self, surface):
        rect = self.image.get_rect(center=(self.x, self.y))
        surface.blit(self.image, rect)
        
def game(*args, **kwargs):
    print("Игра пока не готова")
    return True

def level_up_screen(*args, **kwargs):
    pass

def trophy_screen(*args, **kwargs):
    pass

def game_over_screen(*args, **kwargs):
    return "menu"
