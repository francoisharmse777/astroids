import pygame

from models import SpaceShip
from utils import load_sprite

'''
This class is responsible for creating the game window and running the main loop.
It is also responsible for handling user input.
'''


class SpaceRocks:
    def __init__(self):
        # Initialize pygame and set the title
        pygame.init()
        pygame.display.set_caption("Space Rocks")
        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((800, 600))
        self.background = load_sprite("space", False)

        self.ship = SpaceShip((400, 300))

        self.collision_count = 0

    '''
    Run the main loop.    
    '''

    def main_loop(self):
        while True:
            self._handle_input()
            self._game_logic()
            self._draw()

    '''
    Handle user input.
    '''

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        is_key_pressed = pygame.key.get_pressed()
        if is_key_pressed[pygame.K_ESCAPE] or is_key_pressed[pygame.K_q]:
            quit()
        elif is_key_pressed[pygame.K_RIGHT]:
            self.ship.rotate(clock_wise=True)
        elif is_key_pressed[pygame.K_LEFT]:
            self.ship.rotate(clock_wise=False)

    '''
    Run the game logic.
    '''

    def _game_logic(self):
        self.ship.move()

    '''
    Draw the game window.    
    '''

    def _draw(self):
        self.screen.blit(self.background, (0, 0))
        self.ship.draw(self.screen)
        pygame.display.flip()

        self.clock.tick(30)
