import pygame
import sys

PEACH_BEIGE = (255, 218, 185)
DARK_GREEN = (10, 50, 10)
BLACK = (0, 0, 0)

class Button:
    def __init__(self, rect, text, font):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.base_color = BLACK
        self.hover_color = (30, 30, 30)
        self.active_color = (60, 60, 60)
        self.color = self.base_color
        self.font = font
        self.text_surf = self.font.render(text, True, PEACH_BEIGE)
        self.pressed = False

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_rect = self.text_surf.get_rect(center=self.rect.center)
        surface.blit(self.text_surf, text_rect)

    def update(self, mouse_pos, mouse_pressed):
        if self.rect.collidepoint(mouse_pos):
            if mouse_pressed[0]:
                self.color = self.active_color
                self.pressed = True
            else:
                if self.pressed:
                    self.pressed = False
                self.color = self.hover_color
        else:
            self.color = self.base_color
            self.pressed = False

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def menu(screen, clock, font_big, font_medium):
    easy_button = Button((240 - 100, 320 - 90, 200, 50), "Легкий", font_medium)
    medium_button = Button((240 - 100, 320 - 20, 200, 50), "Средний", font_medium)
    hard_button = Button((240 - 100, 320 + 50, 200, 50), "Сложный", font_medium)
    quit_button = Button((240 - 100, 320 + 120, 200, 50), "Выход", font_medium)

    while True:
        screen.fill(DARK_GREEN)
        title_surf = font_big.render("GAME", True, PEACH_BEIGE)
        screen.blit(title_surf, title_surf.get_rect(center=(240, 640 // 3 - 50)))

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        for button in [easy_button, medium_button, hard_button, quit_button]:
            button.update(mouse_pos, mouse_pressed)
            button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if easy_button.is_clicked(pos):
                    return 1
                elif medium_button.is_clicked(pos):
                    return 2
                elif hard_button.is_clicked(pos):
                    return 3
                elif quit_button.is_clicked(pos):
                    pygame.quit()
                    sys.exit()
                    
        pygame.display.flip()
        clock.tick(60)
        
def skin_selection(screen, clock, font_big, img_truck, img_car_game):
    truck_button = Button((240 - 220, 320 + 50, 200, 50), "Грузовик", pygame.font.SysFont("Arial", 28))
    car_button = Button((240 + 20, 320 + 50, 200, 50), "Автомобиль", pygame.font.SysFont("Arial", 28))

    while True:
        screen.fill((DARK_GREEN))
        title_surf = font_big.render("Выберите скин", True, (PEACH_BEIGE))
        screen.blit(title_surf, title_surf.get_rect(center=(240, 150)))

        truck_img_rect = img_truck.get_rect(center=(240 - 120, 320))
        car_img_rect = img_car_game.get_rect(center=(240 + 120, 320))
        screen.blit(img_truck, truck_img_rect)
        screen.blit(img_car_game, car_img_rect)

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        for button in [truck_button, car_button]:
            button.update(mouse_pos, mouse_pressed)
            button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if truck_button.is_clicked(pos):
                    return img_truck
                elif car_button.is_clicked(pos):
                    return img_car_game
                
        pygame.display.flip()
        clock.tick(60)

def level_up_screen(screen, clock, font_big, level, sound_level_up):
    if sound_level_up:
        sound_level_up.play()
    wait_time = 3
    start_time = pygame.time.get_ticks()

    while pygame.time.get_ticks() - start_time < wait_time * 1000:
        screen.fill(DARK_GREEN)
        text = font_big.render(f"Уровень {level}!", True, PEACH_BEIGE)
        screen.blit(text, text.get_rect(center=(240, 320)))
        pygame.display.flip()
        clock.tick(60)

def game_over_screen(screen, clock, font_big, time_survived, record, level):
    font_medium = pygame.font.SysFont("Arial", 28)
    retry_button = Button((140, 370, 200, 50), "Повторить", font_medium)
    menu_button = Button((140, 440, 200, 50), "В меню", font_medium)

    while True:
        screen.fill(DARK_GREEN)

        over_surf = font_big.render("Игра окончена", True, PEACH_BEIGE)
        time_surf = font_medium.render(f"Время: {time_survived:.2f} с", True, PEACH_BEIGE)
        record_surf = font_medium.render(f"Рекорд: {record:.2f} с", True, PEACH_BEIGE)
        level_surf = font_medium.render(f"Уровень: {level}", True, PEACH_BEIGE)

        screen.blit(over_surf, over_surf.get_rect(center=(240, 150)))
        screen.blit(time_surf, time_surf.get_rect(center=(240, 220)))
        screen.blit(record_surf, record_surf.get_rect(center=(240, 260)))
        screen.blit(level_surf, level_surf.get_rect(center=(240, 300)))

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        retry_button.update(mouse_pos, mouse_pressed)
        menu_button.update(mouse_pos, mouse_pressed)

        retry_button.draw(screen)
        menu_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if retry_button.is_clicked(event.pos):
                    return "retry"
                if menu_button.is_clicked(event.pos):
                    return "menu"

        pygame.display.flip()
        clock.tick(60)
