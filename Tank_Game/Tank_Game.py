import pygame

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
BG_COLOR = pygame.Color(0, 0, 0)

class MainGame():
    def __init__(self):
        pass

    def start_game(self):
        pygame.display.init()
        self.window = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        pygame.display.set_caption('Tank Game')
        while True:
            self.window.fill(BG_COLOR)
            self.get_event()
            pygame.display.update()

    def end_game(self):
        print('Good Bye!')
        exit()

    def get_event(self):
        self.event_list = pygame.event.get()
        for event in self.event_list:
            if event.type == pygame.QUIT:
                self.end_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    print('Turn Left!')
                elif event.key == pygame.K_RIGHT:
                    print('Turn Right!')
                elif event.key == pygame.K_UP:
                    print('Turn Up!')
                elif event.key == pygame.K_DOWN:
                    print('Turn Down')

class Tank():
    def __init__(self) -> None:
        pass

    def move(self):
        pass

    def shot(self):
        pass

    def display_tank(self):
        pass

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