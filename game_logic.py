import pygame
import random
import time
from ui import game_over_screen

WIDTH, HEIGHT = 480, 640
LANE_WIDTH = WIDTH // 4
LANES_X = [LANE_WIDTH * i + LANE_WIDTH // 2 for i in range(4)]

BASE_SPEED = 5
NITRO_SPEED = 15
NITRO_DURATION = 3
NITRO_COOLDOWN = 5

class Player:
    def __init__(self, image):
        self.lane = 1
        self.x = LANES_X[self.lane]
        self.y = HEIGHT - 100
        self.width = 50
        self.height = 90
        self.speed = BASE_SPEED
        self.nitro_active = False
        self.nitro_start_time = 0
        self.nitro_last_used = -NITRO_COOLDOWN
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
        
        if self.nitro_active and time.time() - self.nitro_start_time > NITRO_DURATION:
            self.nitro_active = False
            self.speed = BASE_SPEED

    def draw(self, surface):
        rect = self.image.get_rect(center=(self.x, self.y))
        surface.blit(self.image, rect)
        if self.nitro_active:
            radius = max(self.width, self.height)
            glow = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
            pygame.draw.circle(glow, (0, 150, 255, 100), (radius, radius), radius)
            glow_rect = glow.get_rect(center=(self.x, self.y))
            surface.blit(glow, glow_rect)
    
    def use_nitro(self, sound_nitro):
        now = time.time()
        if now - self.nitro_last_used >= NITRO_COOLDOWN:
            self.nitro_active = True
            self.nitro_start_time = now
            self.nitro_last_used = now
            self.speed = NITRO_SPEED
            if sound_nitro:
                sound_nitro.play()
            return True
        return False
    
    def nitro_status(self):
        now = time.time()
        if self.nitro_active:
            remaining = max(0, NITRO_DURATION - (now - self.nitro_start_time))
            return ("active", remaining)
        else:
            cooldown_left = max(0, NITRO_COOLDOWN - (now - self.nitro_last_used))
            if cooldown_left > 0:
                return ("cooldown", cooldown_left)
            else:
                return ("ready", 0)

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
                elif event.key == pygame.K_SPACE:
                    player.use_nitro(sound_nitro)

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
        
        status, time_left = player.nitro_status()
        if status == "active":
            text = f"Нитро: Активно ({time_left:.1f}s)"
            color = (0, 200, 255)
        elif status == "cooldown":
            text = f"Нитро: Перезарядка ({time_left:.1f}s)"
            color = (200, 100, 0)
        else:
            text = "Нитро: Готово"
            color = (0, 255, 0)
        
        nitro_surf = font_small.render(text, True, color)
        nitro_rect = nitro_surf.get_rect(topright=(WIDTH - 10, 10))
        screen.blit(nitro_surf, nitro_rect) 

        pygame.display.flip()
    
    save_record(record, level)

    action = game_over_screen(screen, clock, pygame.font.SysFont("Arial", 48), survived, record, level) 
    return action == "retry"
