import pygame
import math
from random import randint


class Laser(pygame.sprite.Sprite):
    """Class for sprite creation

    Attributes:
        image (image): Image for sprite
        rect (rect): Rectangle obtained from image
        rect.x (int): Desired x coordinate
        rect.y (int): Desired y coordinate
        step (int): Starting step at 0 for later update use

    """
    def __init__(self, xpos):
        """__init__ method for Sprite

        Args:
            xpos (int): Given x coordinate, will change based on player location.

        """
        super().__init__()

        self.image = pygame.image.load('gameassets/circulo-cromatico.png').convert_alpha()
        # self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = randint(860, 880)
        self.step = 0

    def update(self, speedup=1):
        """Update method to make sprite move a certain way

        Args:
            speedup (int): Default is 1, will change based on boost in-game, to a bigger number to be multiplied to
                current rect.x and rect.y value

        """
        self.rect.x += -1 * math.sin(self.step) * speedup
        self.rect.y -= 5 * speedup
        self.step += 0.008
        self.step %= 2 * math.pi

    def reset_pos(self):
        """Used when sprite goes off to reset position

        Changes the x and y values of the sprite to move to starting position.

        """
        self.rect.x = randint(10, 800)
        self.rect.y = randint(860, 880)
