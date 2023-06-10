import pygame
import pygame.freetype
import time
import random

FPS = 144
WIDTH = 1000
HEIGHT = 600

class StartScreen:
    def __init__(self, game):
        self.game = game
        self.startscreen_running = True
        self.screen = self.game.screen
        self.mid_width = WIDTH / 2
        self.mid_height = HEIGHT / 2

        self.clock = self.game.clock

        self.fontsize = 30
        self.font = pygame.freetype.Font("assets/fonts/Diphylleia-Regular.ttf", self.fontsize)

        self.run()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.startscreen_running = False
                self.game.running = False
                pygame.quit()
                quit()

    def run(self):
        while self.startscreen_running:
            self.check_events()

            text(self, "press any key to continue", self.font, (255, 255, 255), self.mid_width, self.mid_height)

            keys = pygame.key.get_pressed()
            mouse = pygame.mouse.get_pressed()

            if keys.count(1) > 0 or mouse.count(1) > 0:
                self.startscreen_running = False
                print ("Starting game...")
                self.game.main_loop()
                       
            pygame.display.update()

class Snake:
    def __init__(self, game):
        self.game = game
        self.screen = self.game.screen
        self.mid_width = WIDTH / 2
        self.mid_height = HEIGHT / 2
        
        self.color = (220,20,60)

        self.length = 1
        self.size = 20
        self.x = self.mid_width
        self.y = self.mid_height

        self.speed = 2
        
        self.direction = "RIGHT"

        self.appear()
        self.move()
    
    def appear(self):
        pygame.draw.rect(self.screen, self.color, (self.x - (self.size / 2), self.y - (self.size / 2), self.size, self.size))
    
    def move(self):
        if self.direction == "RIGHT":
            self.x += self.speed
        elif self.direction == "LEFT":
            self.x -= self.speed
        elif self.direction == "UP":
            self.y -= self.speed
        elif self.direction == "DOWN":
            self.y += self.speed
    
class Food:
    def __init__(self, game):
        self.game = game
        self.screen = self.game.screen

        self.color = (0, 255, 0)

        self.size = 10
        self.x = random.randint(self.game.frame_size + self.size, WIDTH - self.game.frame_size - self.size)
        self.y = random.randint(self.game.frame_size + self.size, HEIGHT - self.game.frame_size - self.size)

        self.appear()

    def appear(self):
        pygame.draw.rect(self.screen, self.color, (self.x - (self.size / 2), self.y - (self.size / 2), self.size, self.size))


class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.running = False

        self.mid_width = WIDTH / 2
        self.mid_height = HEIGHT / 2   

        self.frame_size = 20
        self.frame_color = (0, 0, 255)

        self.score = 1
        self.fontsize = 25
        self.font = pygame.freetype.Font("assets/fonts/Diphylleia-Regular.ttf", self.fontsize)

        self.start_screen = StartScreen(self)
    
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                quit()

    def draw_frame(self):
        pygame.draw.rect(self.screen, self.frame_color, (0, 0, WIDTH, HEIGHT), self.frame_size)
    
    def check_collision(self, Snake):
        if Snake.x <= self.frame_size + (Snake.size / 2)  or Snake.x >= WIDTH - self.frame_size - (Snake.size / 2) or Snake.y <= self.frame_size + (Snake.size / 2) or Snake.y >= HEIGHT - self.frame_size - (Snake.size / 2):
            print ("Game over!")
            self.running = False
            pygame.quit()
            quit()
    
    def check_keys(self, Snake):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and Snake.direction != "RIGHT":
            Snake.direction = "LEFT"
        elif keys[pygame.K_RIGHT] and Snake.direction != "LEFT":
            Snake.direction = "RIGHT"
        elif keys[pygame.K_UP] and Snake.direction != "DOWN":
            Snake.direction = "UP"
        elif keys[pygame.K_DOWN] and Snake.direction != "UP":
            Snake.direction = "DOWN"

    def draw_snake(self, Snake):
        Snake.appear()
        Snake.move()
    
    def draw_food(self, Food):
        Food.appear()
    
    def check_food_collision(self, Snake, Food):
        if Snake.x - (Snake.size / 2) <= Food.x <= Snake.x + (Snake.size / 2) and Snake.y - (Snake.size / 2) <= Food.y <= Snake.y + (Snake.size / 2):
            print ("Food eaten!")
            Snake.length += 1
            Food.x = random.randint(self.frame_size + (Food.size / 2), WIDTH - self.frame_size - (Food.size / 2))
            Food.y = random.randint(self.frame_size + (Food.size / 2), HEIGHT - self.frame_size - (Food.size / 2))
    
    def draw_score(self, Snake):
        text(self, "score: " + str(Snake.length - 1), self.font, (255, 255, 255), self.frame_size + self.fontsize * 2, self.frame_size + self.fontsize - 10)

    
    def main_loop(self):
        self.running = True
        food = Food(self)
        snake = Snake(self)

        while self.running:
            self.screen.fill((0, 0, 0))
            self.check_events()
            self.draw_frame()
            self.check_collision(snake)
            self.check_keys(snake)
            self.draw_food(food)
            self.draw_snake(snake)
            self.check_food_collision(snake, food)
            self.draw_score(snake)
            pygame.display.update()
            self.clock.tick(FPS)

def text(self, text, font, color, x, y):
    text_surface, rect = font.render(text, color)
    self.screen.blit(text_surface, (x - rect.width / 2, y - rect.height / 2))


    

