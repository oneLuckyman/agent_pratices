import pygame
import os 
import sys 

os.chdir(sys.path[0])

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
BG_COLOR = pygame.Color(0, 0, 0)
TEXT_COLOR = pygame.Color(255, 0, 0)

class MainGame():
    def __init__(self):
        pass

    def start_game(self):
        pygame.display.init()
        self.window = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        self.my_tank = Tank(350, 250)
        pygame.display.set_caption('Tank Game')
        while True:
            self.window.fill(BG_COLOR)
            self.get_event()
            self.window.blit(self.Get_Text_Surface('Number of remaining enemies: %d' %6), (10, 10))
            self.my_tank.display_tank(self.window)
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
                    self.my_tank.direction = 'L'
                    self.my_tank.move()
                    print('Turn Left!')
                elif event.key == pygame.K_RIGHT:
                    self.my_tank.direction = 'R'
                    self.my_tank.move()
                    print('Turn Right!')
                elif event.key == pygame.K_UP:
                    self.my_tank.direction = 'U'
                    self.my_tank.move()
                    print('Turn Up!')
                elif event.key == pygame.K_DOWN:
                    self.my_tank.direction = 'D'
                    self.my_tank.move()
                    print('Turn Down')

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
        self.speed = 10


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
    def __init__(self) -> None:
        pass

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