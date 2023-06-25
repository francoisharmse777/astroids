import pygame

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
        pass

    '''
    Draw the game window.    
    '''

    def _draw(self):
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()
