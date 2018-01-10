"""Module for craft

This module contains all the methods for the moving craft.

"""
import pygame


class Craft(pygame.sprite.Sprite):
    """ Class used to create a sprite of the desired ship

    Attributes:
        image (image): Sprite Image
        integrity (int): The current integrity of the sprite.
        boost (int): The current boost of the sprite.
        rect (rect): The rectangle obtained from the sprite image.
        rect.y (int): Desired y coordinate for the rectangle.
        rect.x (int): Desired x coordinate for the rectangle.
        change_x (int): Used for later methods, current change of x value.
        change_y (int): Used for later methods, current change of y value.
        walls : Used for later methods, for the walls bounding craft to screen.

    """
    def __init__(self, x, y):
        """Initializing Method
        

        Args:
            x (int): Desired x coordinate
            y (int): Desired y coordinate

        """
        super().__init__()
        self.image = pygame.image.load("gameassets/ship_1.png").convert_alpha()
        self.integrity = 100
        self.boost = 100
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        # Set speed vector
        self.change_x = 0
        self.change_y = 0
        self.walls = None
    
    def changespeed(self, x, y):
        """ Change the speed of the player.

        Args:
            x (int): Supplied change of x value
            y (int): Supplied change of y value
        """
        self.change_x += x
        self.change_y += y

    def update(self):
        """ Update the player position. Taking into account the walls created.

        """
        # Move left/right
        self.rect.x += self.change_x

        # Did this update cause us to hit a wall?
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            # If we are moving right, set our right side to the left side of
            # the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom
