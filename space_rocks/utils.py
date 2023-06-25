# this is helper file to run helper methods for the code
# load sprites (this is using external graphics and sounds files)

from pathlib import Path

from pygame import Color
from pygame.image import load
from pygame.math import Vector2
from pygame.mixer import Sound

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


def load_sound(name):
    filename = Path(__file__).parent / Path(f"assets/sounds/{name}.wav")
    return Sound(filename)


def print_text(surface, text, font, color=Color("tomato")):
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect()
    rect.center = Vector2(surface.get_size()) / 2
    surface.blit(text_surface, rect)
