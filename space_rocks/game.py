import pygame

from models import SpaceShip, Rock
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
        self.rocks = [Rock(self.screen, self.ship.position) for _ in range(6)]

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
        elif is_key_pressed[pygame.K_UP]:
            self.ship.accelerate()

    @property
    def game_objects(self):
        #  By using the star operator (*) inside of this list,
        #  it deconstructs the rock list, so the result returned here is a single
        #  list with all the rocks plus the ship.
        return [*self.rocks, self.ship]

    '''
    Run the game logic.
    The ._game_logic() method handles the motion of anything that has a velocity. 
    With the new .game_objects() property, this method can be simplified to iterate 
    over every object in the game and calling each object’s .move() method. Let me scroll down.
    '''

    def _game_logic(self):
        for obj in self.game_objects:
            obj.move(self.screen)

    '''
    Draw the game window.    
    '''

    def _draw(self):
        self.screen.blit(self.background, (0, 0))

        # And here’s that same .game_objects() property once again—this time,
        # used to draw each of the objects in the game.
        for obj in self.game_objects:
            obj.draw(self.screen)

        pygame.display.flip()

        self.clock.tick(30)
