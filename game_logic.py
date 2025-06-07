import pygame
import random
import time

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

def collision_effect(sound_collision):
    flash_time = 0.5
    end_time = time.time() + flash_time
    screen = pygame.display.get_surface()
    clock = pygame.time.Clock()
    while time.time() < end_time:
        screen.fill((255, 0, 0))
        pygame.display.flip()
        clock.tick(60)
    if sound_collision:
        sound_collision.play()
        
def load_record(level): 
    try:
        with open(f"record_level_{level}.txt", "r") as f:
            return float(f.read())
    except:
        return 0.0

def save_record(record, level): 
    try:
        with open(f"record_level_{level}.txt", "w") as f:
            f.write(str(record))
    except:
        pass

def game(level, player_image, img_car, img_obstacle, sound_collision, sound_nitro, sound_level_up):
    player = Player(player_image)
    player.speed = BASE_SPEED

    obstacles = []
    spawn_timer = 0
    spawn_interval = 1000 
    running = True
    start_time = time.time()
    record = load_record(level)

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
        
        player_rect = pygame.Rect(player.x - player.width//2, player.y - player.height//2, player.width, player.height)
        collision = False
        for obs in obstacles:
            obs_rect = pygame.Rect(obs.x - obs.width//2, obs.y - obs.height//2, obs.width, obs.height)
            if player_rect.colliderect(obs_rect):
                collision = True
                break
            
        if collision:
            collision_effect(sound_collision)
            running = False

        player.draw(screen)
        for obs in obstacles:
            obs.draw(screen)
        
        survived = time.time() - start_time 
        if survived > record:
            record = survived

        font_small = pygame.font.SysFont("Arial", 20)
        time_surf = font_small.render(f"Время: {survived:.2f} с", True, (255, 218, 185))
        record_surf = font_small.render(f"Рекорд: {record:.2f} с", True, (255, 218, 185))
        screen.blit(time_surf, (10, 10))
        screen.blit(record_surf, (10, 35)) 

        pygame.display.flip()
    
    save_record(record, level)

    action = game_over_screen(screen, clock, pygame.font.SysFont("Arial", 48), survived, record, level) 
    return action == "retry"

def level_up_screen(*args, **kwargs):
    pass

def trophy_screen(*args, **kwargs):
    pass

def game_over_screen(*args, **kwargs):
    return "menu"
