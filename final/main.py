import pygame
from src.controller import Controller

def main():
    pygame.init()
    controller = Controller()
    controller.game_loop()

if __name__ == '__main__':
    main()
