import pygame

from models import GameObject
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

        self.screen = pygame.display.set_mode((800, 600))
        self.background = load_sprite("space", False)

        sprite = load_sprite("spaceship")
        self.ship = GameObject((400, 300), sprite, (0, 0))

        sprite = load_sprite("asteroid")
        self.rock = GameObject((50, 300), sprite, (1, 0))

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

    '''
    Run the game logic.
    '''

    def _game_logic(self):
        self.ship.move()
        self.rock.move()

    '''
    Draw the game window.    
    '''

    def _draw(self):
        self.screen.blit(self.background, (0, 0))
        self.ship.draw(self.screen)
        self.rock.draw(self.screen)
        pygame.display.flip()

        if self.ship.collides_with(self.rock):
            self.collision_count += 1
            print(f"Collision #{self.collision_count}")
