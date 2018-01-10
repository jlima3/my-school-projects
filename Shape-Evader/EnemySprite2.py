import pygame
from random import randint


class Laser(pygame.sprite.Sprite):
    """Class for sprite creation

    Attributes:
        image (image): Image for sprite
        rect (rect): Rectangle obtained from image
        rect.x (int): Desired x coordinate
        rect.y (int): Desired y coordinate

    """
    def __init__(self, xpos):
        """__init__ method for Sprite

        Args:
            xpos (int): Given x coordinate, will change based on player location.

        """
        super().__init__()

        self.image = pygame.image.load("gameassets/DurrrSpaceShip.png").convert_alpha()

        self.rect = self.image.get_rect()

        self.rect.x = xpos
        self.rect.y = randint(-20, -15)

    def update(self, speedup=1):
        """Update method to make sprite move a certain way

        Args:
            speedup (int): Default is 1, will change based on boost in-game, to a bigger number to be multiplied to
                current rect.x and rect.y value

        """
        self.rect.y += 5 * speedup

    def reset_pos(self):
        self.rect.x = randint(10, 800)
        self.rect.y = randint(-20, -15)
