from pygame.math import Vector2

'''
This class is used to represent a game object.
It has a position, a size, a sprite, and a velocity.
It can be drawn to a surface, moved, and checked for collisions.
'''


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
