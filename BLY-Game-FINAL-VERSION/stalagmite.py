import pygame
from pygame.locals import *
from pygame import mixer

class Stalagmite(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_size):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('assets/stalactite.png')
        img = pygame.transform.flip(img, False, True)
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - (tile_size / 2)