import pygame
from random import randint


class Boost(pygame.sprite.Sprite):
    """Class for the Boost sprite that will give player boost replenishment

    Attributes:
        oldimage (image): original boost sprite
        image (image): rescaled boost sprite
        rect (rect): Bounding rectangle
        rect.x (int): Random int between 300 and 800 for x position
        rect.y (int): Random int between 25 and 775 for y position
    """
    def __init__(self):
        super().__init__()
        self.integrityup = 0
        self.boostup = 100
        self.oldimage = pygame.image.load("gameassets/boostup.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.oldimage, (20, 40))
        self.rect = self.image.get_rect()
        self.rect.x = randint(300, 800)
        self.rect.y = randint(25, 775)

