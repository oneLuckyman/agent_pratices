import turtle
import pygame
import os 
import sys 
import time
import random

os.chdir(sys.path[0])

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
BG_COLOR = pygame.Color(0, 0, 0)
TEXT_COLOR = pygame.Color(255, 0, 0)
TANK_SPEED = 10

class MainGame():
    ENEMYTANK_NUMS = 5

    def __init__(self):
        self.move_keys = 0
        self.enemy_tank_list = []

    def start_game(self):
        pygame.display.init()
        self.window = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        self.my_tank = Tank(350, 250)
        self.create_enemy_tank()
        pygame.display.set_caption('Tank Game')
        while True:
            time.sleep(0.02)
            self.window.fill(BG_COLOR)
            self.get_event()
            self.window.blit(self.Get_Text_Surface('Number of remaining enemies: %d' %6), (10, 10))
            if not self.my_tank.stop:    
                self.my_tank.move()
            self.my_tank.display_tank(self.window)
            self.blit_all_enemy_tank()
            pygame.display.update()

    def end_game(self):
        print('Good Bye!')
        exit()

    def Get_Text_Surface(self, text):
        pygame.font.init()
        font = pygame.font.SysFont('timesnewroman', 18)
        textsurface = font.render(text, True, TEXT_COLOR)
        return textsurface

    def get_event(self):
        self.event_list = pygame.event.get()
        for event in self.event_list:
            if event.type == pygame.QUIT:
                self.end_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.move_keys += 1
                    self.my_tank.direction = 'L'
                    # self.my_tank.move()
                    self.my_tank.stop = False
                    print('Turn Left!')
                elif event.key == pygame.K_RIGHT:
                    self.move_keys += 1
                    self.my_tank.direction = 'R'
                    # self.my_tank.move()
                    self.my_tank.stop = False
                    print('Turn Right!')
                elif event.key == pygame.K_UP:
                    self.move_keys += 1
                    self.my_tank.direction = 'U'
                    # self.my_tank.move()
                    self.my_tank.stop = False
                    print('Turn Up!')
                elif event.key == pygame.K_DOWN:
                    self.move_keys += 1
                    self.my_tank.direction = 'D'
                    # self.my_tank.move()
                    self.my_tank.stop = False
                    print('Turn Down')
                elif event.key == pygame.K_SPACE:
                    print('Fire!')
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    self.move_keys -= 1
                if not self.move_keys:    
                    self.my_tank.stop = True
    
    def create_enemy_tank(self):
        top = 100
        for i in range(self.ENEMYTANK_NUMS):
            left = random.randint(0, 600)
            speed = random.randint(1, 4)
            self.enemy_tank_list.append(EnemyTank(left, top, speed))
    
    def blit_all_enemy_tank(self):
        for enemy_tank in self.enemy_tank_list:
            enemy_tank.display_tank(self.window)

class Tank():
    def __init__(self, left, top) -> None:
        self.images={
            'U':pygame.image.load('img/pltankU.png'),
            'D':pygame.image.load('img/pltankD.png'),
            'L':pygame.image.load('img/pltankL.png'),
            'R':pygame.image.load('img/pltankR.png')
        }

        self.direction = 'U'
        self.height = 56
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect()
        self.rect.left = left 
        self.rect.top = top
        self.speed = TANK_SPEED
        self.stop = True


    def move(self):
        if self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
        elif self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
        elif self.direction == 'R':
            if self.rect.left < SCREEN_WIDTH - self.height:
                self.rect.left += self.speed
        elif self.direction == 'D':
            if self.rect.top < SCREEN_HEIGHT - self.height:
                self.rect.top += self.speed

    def shot(self):
        pass

    def display_tank(self, window):
        self.image = self.images[self.direction]
        window.blit(self.image, self.rect)

class MyTank(Tank):
    def __init__(self) -> None:
        pass

class EnemyTank(Tank):
    def __init__(self, left, top, speed) -> None:
        self.images = {
            'U':pygame.image.load('img/enemy1_U.png'),
            'D':pygame.image.load('img/enemy1_D.png'),
            'L':pygame.image.load('img/enemy1_L.png'),
            'R':pygame.image.load('img/enemy1_R.png')
        }

        self.direction = self.random_direction()
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect()
        self.rect.left = left 
        self.rect.top = top 
        self.speed = speed 
        self.stop = True
    
    def random_direction(self):
        num = random.randint(1,4)
        if num == 1:
            return 'U'
        elif num == 2:
            return 'D'
        elif num == 3:
            return 'R'
        elif num == 4:
            return 'L'


class Bullet():
    def __init__(self) -> None:
        pass

    def move(self):
        pass

    def display_bullet(self):
        pass

class Wall():
    def __init__(self) -> None:
        pass

    def display_wall(self):
        pass

class Explode():
    def __init__(self):
        pass

    def display_explode(self):
        pass

class Music():
    def __init__(self) -> None:
        pass

    def play(self):
        pass

if __name__ == '__main__':
    MainGame().start_game()