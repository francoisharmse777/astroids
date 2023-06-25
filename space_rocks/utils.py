# this is helper file to run helper methods for the code
# load sprites (this is using external graphics and sounds files)

from pathlib import Path

from pygame.image import load
from pygame.math import Vector2

'''
This method is used to load sprite from the assets folder
:param name: name of the sprite
:param with_alpha: boolean value to check if the sprite has alpha channel or not
:return: sprite object
:rtype: pygame.Surface
'''


def load_sprite(name, with_alpha=True):
    filename = Path(__file__).parent / Path(f"assets/sprites/{name}.png")
    sprite = load(filename.resolve())

    if with_alpha:
        return sprite.convert_alpha()

    return sprite.convert()


def wrap_position(position, surface):
    x, y = position
    w, h = surface.get_size()
    return Vector2(x % w, y % h)
