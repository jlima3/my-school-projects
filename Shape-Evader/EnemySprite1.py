import pygame
from random import randint


class Laser(pygame.sprite.Sprite):
    """Class for sprite creation

    Attributes:
        image (image): Image for sprite
        rect (rect): Rectangle obtained from image
        rect.x (int): Desired x coordinate
        rect.y (int): Desired y coordinate
        randomy (int): Random integer for use in update method
        randomx (int): Random integer for use in update method

    """
    def __init__(self, ypos):
        """__init__ method for Sprite

        Args:
            ypos (int): Given y coordinate, will change based on player location.

        """
        super().__init__()

        self.image = pygame.image.load('gameassets/asteroid.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = randint(800, 880)
        self.rect.y = ypos
        self.randomy = randint(-5, 5)
        self.randomx = randint(5, 20)

    def update(self, speedup=1):
        """Update method to make sprite move a certain way

        Args:
            speedup (int): Default is 1, will change based on boost in-game, to a bigger number to be multiplied to
                current rect.x and rect.y value

        """
        self.rect.x -= self.randomx * speedup
        self.rect.y += self.randomy * speedup

    def reset_pos(self):
        """Used when sprite goes off to reset position

        Changes the x and y values of the sprite to move to starting position.

        """
        self.rect.x = 850
        self.rect.y = randint(0, 800)
