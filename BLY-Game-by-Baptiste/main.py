import pygame

from player import *

# INSPIRED OF https://coderslegacy.com/python/python-pygame-tutorial/

pygame.init()

# Taille de l'écran
screen_width = 1080
screen_height = 720

# Générer la fenêtre de notre jeu
pygame.display.set_caption("Luffy Bros")
screen = pygame.display.set_mode((screen_width, screen_height))

# Remplir la fenêtre
WHITE = (255,255,255)
screen.fill(WHITE)

# Fixer les FPS
FPS = pygame.time.Clock()
FPS.tick(60)

# Importer l'arrière plan de notre jeu
background = pygame.image.load("assets/bg.jpg")


# Variable pour le jeu
gravity = 1

# Créerr un objet de type Player
P1 = Player(screen_width, screen_height)

# Variable pour la boucle permettant l'affichage de la fenêtre
running = True

while running:
    # Afficher le background
    screen.blit(background, (0, -200))

    # Déplacement du joueur
    P1.update()
    # Mettre à jour l'affichage
    P1.draw(screen)

    # Mettre à jour l'écran
    pygame.display.flip()

    # Scan de tous les évènements
    for event in pygame.event.get():
        # QUIT
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            print("Fermeture du jeu")

