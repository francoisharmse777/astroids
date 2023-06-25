from pygame.math import Vector2
from pygame.transform import rotozoom

from utils import load_sprite

'''
This class is used to represent a game object.
It has a position, a size, a sprite, and a velocity.
It can be drawn to a surface, moved, and checked for collisions.
'''

DIRECTION_UP = Vector2(0, -1)


class GameObject:
    def __init__(self, position, sprite, velocity):
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = self.sprite.get_width() / 2
        self.velocity = Vector2(velocity)

    '''
    Draws the game object to the screen.
    The position of the object is subtracted from the position of the screen
    to get the correct position.    
    '''

    def draw(self, surface):
        position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, position)

    '''
    Moves the game object.
    The velocity is added to the position.
    '''

    def move(self):
        self.position = self.position + self.velocity

    '''
    Checks if the game object collides with another game object.
    The distance between the two objects is calculated.
    If the distance is less than the sum of the two objects' radii,
    then the objects collide.
    Returns True if the objects collide, False otherwise.
    '''

    def collides_with(self, other):
        distance = self.position.distance_to(other.position)
        return distance < self.radius + other.radius


class SpaceShip(GameObject):
    ROTATION_SPEED = 3

    def __init__(self, position):
        self.direction = Vector2(DIRECTION_UP)
        super().__init__(position, load_sprite("spaceship"), Vector2(0))

    def rotate(self, clock_wise=True):
        sign = 1 if clock_wise else -1
        angle = self.ROTATION_SPEED * sign
        self.direction.rotate_ip(angle)

    def draw(self, surface):
        angle = self.direction.angle_to(DIRECTION_UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())

        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)
