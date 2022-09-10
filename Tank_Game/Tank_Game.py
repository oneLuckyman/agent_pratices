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

class BaseItem(pygame.sprite.Sprite):
    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self)

class MainGame():
    ENEMYTANK_NUMS = 5
    explode_list = []

    def __init__(self):
        self.move_keys = 0
        self.enemy_tank_list = []
        self.my_bullet_list = []
        self.enemy_bullet_list = []

    def start_game(self):
        pygame.display.init()
        self.window = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        self.my_tank = Tank(350, 250)
        self.create_enemy_tank()
        pygame.display.set_caption('Tank Game')
        while True:
            time.sleep(0.02)
            self.window.fill(BG_COLOR)
            self.window.blit(self.Get_Text_Surface('Number of remaining enemies: %d' %len(self.enemy_tank_list)), (10, 10))
            if self.my_tank.alive:
                self.my_tank.display_tank(self.window)
            else:
                break
            self.get_event()
            if not self.my_tank.stop:    
                self.my_tank.move()
            self.blit_all_enemy_tank()
            self.blit_my_bullet()
            self.blit_enemy_bullet()
            self.blit_explode()
            pygame.display.update()
        
        print('Game Over!!!')

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
                    if len(self.my_bullet_list) <= 3:
                        my_bullet = Bullet(self.my_tank)
                        self.my_bullet_list.append(my_bullet)
                        print('Fire!')
                    else:
                        print('Too many bullets!')
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
            if enemy_tank.alive:
                enemy_tank.display_tank(self.window)
                enemy_tank.random_move()
                enemy_bullet = enemy_tank.shot()
                if enemy_bullet:
                    self.enemy_bullet_list.append(enemy_bullet)
            else:
                self.enemy_tank_list.remove(enemy_tank)
    
    def blit_my_bullet(self):
        for my_bullet in self.my_bullet_list:
            if my_bullet.alive:
                my_bullet.display_bullet(self.window)
                my_bullet.move()
                my_bullet.hit_enemy_tank(self.enemy_tank_list, self.window)
            else:
                self.my_bullet_list.remove(my_bullet)
    
    def blit_enemy_bullet(self):
        for enemy_bullet in self.enemy_bullet_list:
            if enemy_bullet.alive:
                enemy_bullet.display_bullet(self.window)
                enemy_bullet.move()
                enemy_bullet.hit_my_tank(self.my_tank, self.window)
            else:
                self.enemy_bullet_list.remove(enemy_bullet)
    
    def blit_explode(self):
        for explode in self.explode_list:
            if explode.alive:
                explode.display_explode()
            else:
                self.explode_list.remove(explode)

class Tank(BaseItem):
    def __init__(self, left, top) -> None:
        self.images={
            'U':pygame.image.load('img/pltankU.png'),
            'D':pygame.image.load('img/pltankD.png'),
            'L':pygame.image.load('img/pltankL.png'),
            'R':pygame.image.load('img/pltankR.png')
        }

        self.alive = True
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
                if (self.rect.left - self.speed) < 0:
                    self.rect.left = 0
                else:
                    self.rect.left -= self.speed
        elif self.direction == 'U':
            if self.rect.top > 0:
                if (self.rect.top - self.speed) < 0:
                    self.rect.top = 0
                else:
                    self.rect.top -= self.speed
        elif self.direction == 'R':
            if self.rect.left < SCREEN_WIDTH - self.height:
                if (self.rect.left + self.speed) > (SCREEN_WIDTH - self.height):
                    self.rect.left = (SCREEN_WIDTH - self.height)
                else:
                    self.rect.left += self.speed
        elif self.direction == 'D':
            if self.rect.top < SCREEN_HEIGHT - self.height:
                if (self.rect.top + self.speed) > (SCREEN_HEIGHT - self.height):
                    self.rect.top = (SCREEN_HEIGHT - self.height)
                else:
                    self.rect.top += self.speed

    def shot(self):
        num = random.randint(1, 100)
        if num < 50:
            return Bullet(self)

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

        self.alive = True
        self.direction = self.random_direction()
        self.image = self.images[self.direction]
        self.height = 56
        self.rect = self.image.get_rect()
        self.rect.left = left 
        self.rect.top = top 
        self.speed = speed 
        self.stop = True
        self.init_steps = 60
        self.steps = self.init_steps
    
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
    
    def random_move(self):
        if self.steps <= 0:
            self.direction = self.random_direction()
            self.steps = self.init_steps
        else:
            self.move()
            self.steps -= self.speed


class Bullet(BaseItem):
    def __init__(self, tank: Tank) -> None:
        self.images = {
            'U':pygame.image.load('img/Bullet/bullet_up.png'),
            'D':pygame.image.load('img/Bullet/bullet_down.png'),
            'L':pygame.image.load('img/Bullet/bullet_left.png'),
            'R':pygame.image.load('img/Bullet/bullet_right.png')
        }

        self.direction = tank.direction
        self.height = 12
        self.speed = 5
        self.alive = True

        if self.direction == 'U':
            self.image = self.images[self.direction]
            self.rect = self.image.get_rect()
            self.rect.left = tank.rect.left + ((tank.height - self.height) / 2) + 1
            self.rect.top = tank.rect.top - self.height
        elif self.direction == 'D':
            self.image = self.images[self.direction]
            self.rect = self.image.get_rect()
            self.rect.left = tank.rect.left + ((tank.height - self.height) / 2) + 1
            self.rect.top = tank.rect.top + tank.height
        elif self.direction == 'R':
            self.image = self.images[self.direction]
            self.rect = self.image.get_rect()
            self.rect.left = tank.rect.left + tank.height
            self.rect.top = tank.rect.top + ((tank.height - self.height) / 2) + 1
        elif self.direction == 'L':
            self.image = self.images[self.direction]
            self.rect = self.image.get_rect()
            self.rect.left = tank.rect.left - self.height
            self.rect.top = tank.rect.top + ((tank.height - self.height) / 2) + 1
            

    def move(self):
        if self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
            else:
                self.alive = False
        if self.direction == 'D':
            if self.rect.top < (SCREEN_HEIGHT - self.height):
                self.rect.top += self.speed
            else:
                self.alive = False
        if self.direction == 'R':
            if self.rect.left < (SCREEN_WIDTH - self.height):
                self.rect.left += self.speed
            else:
                self.alive = False
        if self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
            else:
                self.alive = False

    def display_bullet(self, window):
        window.blit(self.image, self.rect)
    
    def hit_enemy_tank(self, enemy_tank_list, window):
        for enemy_tank in enemy_tank_list:
            if pygame.sprite.collide_rect(self, enemy_tank):
                enemy_tank.alive = False
                self.alive = False
                MainGame.explode_list.append(Explode(enemy_tank, window))
    
    def hit_my_tank(self, my_tank, window):
        if pygame.sprite.collide_rect(self, my_tank):
            if pygame.sprite.collide_rect(self, my_tank):
                my_tank.alive = False
                self.alive = False
                MainGame.explode_list.append(Explode(my_tank, window))


class Wall():
    def __init__(self) -> None:
        pass

    def display_wall(self):
        pass

class Explode():
    def __init__(self, tank, window):
        self.window = window
        self.rect = tank.rect
        self.rect.left += 4 # (56 - 48)/2 
        self.rect.top += 4
        self.step = 0
        self.images = [
            pygame.image.load('img/boom_static.png'),
            pygame.image.load('img/boom_static.png')
        ]
        self.alive = True 

    def display_explode(self):
        if self.step < len(self.images):
            self.image = self.images[self.step]
            self.step += 1
            self.window.blit(self.image, self.rect)
        else:
            self.alive = False 
            self.step = 0


class Music():
    def __init__(self) -> None:
        pass

    def play(self):
        pass

if __name__ == '__main__':
    MainGame().start_game()