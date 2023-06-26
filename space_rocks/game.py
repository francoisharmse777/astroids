import pygame

from models import SpaceShip, Rock
from utils import load_sprite, load_sound, print_text

'''
This class is responsible for creating the game window and running the main loop.
It is also responsible for handling user input.
'''

bullets = []
rocks = []


class SpaceRocks:
    def __init__(self):
        # Initialize pygame and set the title
        pygame.init()
        pygame.display.set_caption("Space Rocks")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 64)
        self.message = ""

        self.screen = pygame.display.set_mode((800, 600))
        self.background = load_sprite("space", False)

        self.ship = SpaceShip((400, 300))

        global rocks
        rocks = [Rock.create_random(self.screen, self.ship.position)
                 for _ in range(6)
                 ]

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
            if event.type == pygame.KEYDOWN and self.ship:
                if event.key == pygame.K_SPACE:
                    self.ship.shoot()

        is_key_pressed = pygame.key.get_pressed()

        if self.ship is None:
            return

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
        global bullets, rocks
        #  By using the star operator (*) inside of this list,
        #  it deconstructs the rock list, so the result returned here is a single
        #  list with all the rocks plus the ship.
        return [*rocks, *bullets, self.ship]

    '''
    Run the game logic.
    The ._game_logic() method handles the motion of anything that has a velocity. 
    With the new .game_objects() property, this method can be simplified to iterate 
    over every object in the game and calling each object’s .move() method. Let me scroll down.
    '''

    def _game_logic(self):

        self.kaboom = load_sound("kaboom")

        global bullets, rocks

        if self.ship:
            for obj in self.game_objects:
                obj.move(self.screen)

        #  As the desired result of the bullet being off the screen is to remove it,
        #  you’re going to need to iterate and remove at the same time.
        #  There are two ways to handle this in code:
        #  Either create a temporary list of objects to remove and remove all of them after
        #  you’re done iterating, or what I’m doing here, which is using a copy of the list.
        #
        # The [:] notation here is using list slicing, but saying,
        # “Give me a slice that is the whole list.”
        # This gives you a copy of the list. Line 55 is actually iterating through that
        # copy of the bullet container.
        rect = self.screen.get_rect()
        for bullet in bullets[:]:
            if not rect.collidepoint(bullet.position):
                bullets.remove(bullet)

        for bullet in bullets[:]:
            for rock in rocks[:]:
                if rock.collides_with(bullet):
                    rocks.remove(rock)
                    rock.split()
                    bullets.remove(bullet)
                    break

        if self.ship:
            for rock in rocks[:]:
                if rock.collides_with(self.ship):
                    self.ship = None
                    self.message = "Game Over!"
                    self.kaboom.play()
                    break

        if not rocks and self.ship:
            self.message = "You Won!!!"

    '''
    Draw the game window.    
    '''

    def _draw(self):
        self.screen.blit(self.background, (0, 0))

        # And here’s that same .game_objects() property once again—this time,
        # used to draw each of the objects in the game.
        if self.ship:
            for obj in self.game_objects:
                obj.draw(self.screen)

        if self.message:
            print_text(self.screen, self.message, self.font)

        pygame.display.flip()

        self.clock.tick(30)
