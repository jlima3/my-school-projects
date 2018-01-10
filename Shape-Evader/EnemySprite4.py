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
    def __init__(self):
        """__init__ method for Sprite

        """
        super().__init__()
        self.image = pygame.image.load('gameassets/fire-ball.png')
        self.rect = self.image.get_rect()
        self.rect.x = randint(600, 800)
        self.rect.y = randint(-10, 0)

    def update(self, speedup=1):
        """Update method to make sprite move a certain way

        Args:
            speedup (int): Default is 1, will change based on boost in-game, to a bigger number to be multiplied to
                current rect.x and rect.y value

        """
        self.rect.x -= 5 * speedup
        self.rect.y += 5 * speedup

    def reset_pos(self):
        self.rect.x = randint(600, 800)
        self.rect.y = randint(-20, 0)
