import pygame

# Créer une première classe qui va représenter notre joueur

class Player(pygame.sprite.Sprite):

    def __init__(self): # Initialiser la classe
        super().__init__() # Initialiser la super classe Sprite
        self.health = 100 # Vie du joueur
        self.max_health = 100 # Vie maximale du joueur
        self.attack = 10 # Points d'attaques du joueur
        self.velocity = 1 # Vitesse du joueur
        self.image = pygame.image.load("assets/LuffyRedHappymove2 (Personnalisé).png") # Charge l'image du joueur
        self.rect = self.image.get_rect() # Rectangle
        self.rect.x = 400
        self.rect.y = 500
        self.mass = 1


    def move_right(self):
        self.rect.x += self.velocity

    def move_left(self):
        self.rect.x -= self.velocity

    def jump_up(self):
        self.rect.h += self

