import pygame
import random

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
        
def draw_road(surface):
    surface.fill((70, 70, 70))
    for i in range(1, 4):
        x = LANE_WIDTH * i
        dash_length = 20
        gap = 15
        y = 0
        while y < HEIGHT:
            pygame.draw.line(surface, (255, 255, 255), (x, y), (x, y + dash_length), 4)
            y += dash_length + gap

def game(level, player_image, img_car, img_obstacle, sound_collision, sound_nitro, sound_level_up):
    player = Player(player_image)
    player.speed = BASE_SPEED

    obstacles = []
    spawn_timer = 0
    spawn_interval = 1000 
    running = True

    clock = pygame.time.Clock()
    screen = pygame.display.get_surface()

    while running:
        dt = clock.tick(60)
        draw_road(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.move_left()
                elif event.key == pygame.K_RIGHT:
                    player.move_right()

        spawn_timer += dt
        if spawn_timer > spawn_interval:
            spawn_timer = 0
            lane = random.randint(0, 3)
            kind = random.choice([0, 1])
            speed = player.speed
            obstacles.append(Obstacle(lane, speed, kind, img_obstacle, img_car))

        player.update()

        for obs in obstacles[:]:
            obs.update()
            if obs.y > HEIGHT + obs.height:
                obstacles.remove(obs)

        player.draw(screen)
        for obs in obstacles:
            obs.draw(screen)

        pygame.display.flip()

    return True

def level_up_screen(*args, **kwargs):
    pass

def trophy_screen(*args, **kwargs):
    pass

def game_over_screen(*args, **kwargs):
    return "menu"
