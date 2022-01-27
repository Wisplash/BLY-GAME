import pygame
from pygame.locals import *

class Player(pygame.sprite.Sprite):
    screen_width = 0
    screen_height = 0

    def __init__(self, screen_width, screen_height):
        super().__init__()

        self.image = pygame.image.load("assets/Player1.png")
        self.image = pygame.transform.scale(self.image, (100, 143))

        self.rect = self.image.get_rect()
        self.rect.center = (100, screen_height - 125)

        self.screen_width = screen_width
        self.screen_height = screen_height


    def update(self):
        pressed_keys = pygame.key.get_pressed()
        # if pressed_keys[K_UP]:                # NOT USED
        #     self.rect.move_ip(0, -5)
        # if pressed_keys[K_DOWN]:
        #     self.rect.move_ip(0,5)

        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < self.screen_width:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

    def draw(self, screen):
        screen.blit(self.image, self.rect)