import random

from pygame.math import Vector2
from pygame.transform import rotozoom

from utils import load_sprite, wrap_position, load_sound

'''
This class is used to represent a game object.
It has a position, a size, a sprite, and a velocity.
It can be drawn to a surface, moved, and checked for collisions.
'''

DIRECTION_UP = Vector2(0, -1)


class GameObject:
    def __init__(self, position, sprite, velocity, wraps=True):
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)
        self.wraps = wraps

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

    def move(self, surface):
        move_to = self.position + self.velocity

        if self.wraps:
            self.position = wrap_position(move_to, surface)
        else:
            self.position = move_to

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
    ACCELERATION = 0.25
    BULLET_SPEED = 10

    def __init__(self, position):
        self.direction = Vector2(DIRECTION_UP)
        self.pew_pew = load_sound("laser")
        super().__init__(position, load_sprite("spaceship"), Vector2(0))

    def rotate(self, clock_wise=True):
        sign = 1 if clock_wise else -1
        angle = self.ROTATION_SPEED * sign
        self.direction.rotate_ip(angle)

    def accelerate(self):
        self.velocity += self.direction * self.ACCELERATION
        print(f'Velocity {self.velocity} @ direction {self.direction}')

    def shoot(self):
        velocity = self.direction * self.BULLET_SPEED + self.velocity
        bullet = Bullet(self.position, velocity)

        from game import bullets
        bullets.append(bullet)
        self.pew_pew.play()

    def draw(self, surface):
        angle = self.direction.angle_to(DIRECTION_UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())

        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)


class Rock(GameObject):
    MIN_START_GAP = 250
    MIN_SPEED = 1
    MAX_SPEED = 3

    #  What I’ve decided to do here is create a factory method. A factory method is a class
    #  method that constructs and returns an object. This pattern is useful if there are a
    #  bunch of different ways of constructing something.
    #
    # Factory methods can sometimes make your code clearer.
    # Instead of having to read all the various parameters to interpret how a constructor is
    # going to be called, you can have a factory method called .create_random() whose name might
    # be considered clearer than having to use a use_random_position=True parameter.
    @classmethod
    def create_random(cls, surface, ship_position):
        while True:
            position = Vector2(
                random.randrange(surface.get_width()),
                random.randrange(surface.get_height()),
            )

            if position.distance_to(ship_position) > cls.MIN_START_GAP:
                break

        return Rock(position)

    def __init__(self, position, size=3):
        self.wam = load_sound("explode")
        self.size = size
        if size == 3:
            scale = 1.0
        elif size == 2:
            scale = 0.5
        else:
            scale = 0.25

        sprite = rotozoom(load_sprite("asteroid"), 0, scale)
        # Random velocity
        speed = random.randint(self.MIN_SPEED, self.MAX_SPEED)
        angle = random.randint(0, 360)
        velocity = Vector2(speed, 0).rotate(angle)

        super().__init__(position, sprite, velocity)

    def split(self):
        if self.size > 1:
            from game import rocks

            rocks.append(Rock(self.position, self.size - 1))
            rocks.append(Rock(self.position, self.size - 1))
            self.wam.play()


class Bullet(GameObject):
    def __init__(self, position, velocity):
        super().__init__(position, load_sprite("bullet"), velocity, False)
