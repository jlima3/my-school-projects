import pygame

black = pygame.Color(0, 0, 0)

class Wall(pygame.sprite.Sprite):
    """Class for wall creation to keep player in bounds

    """
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(black)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
