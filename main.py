import pygame
pygame.init()
from game import Game


# Générer la fenêtre de notre jeu
pygame.display.set_caption("Luffy Bros")
screen = pygame.display.set_mode((1080, 720))


# Importer l'arrière plan de notre jeu
background = pygame.image.load("assets/bg.jpg")

# CHarger notre jeu
game = Game()

# Variable pour la fenêtre
running = True


# Boucle tant que cette condition est vrai
while running:

    # Appliquer arrère plan
    screen.blit(background, (0, -200))

    #Appliquer l'image de mon joueur
    screen.blit(game.player.image, game.player.rect) # Injecter l'image de mon choix

    # Vérifier si le joueur souhaite aller à gauche ou à droite
    if game.pressed.get(pygame.K_RIGHT) and game.player.rect.x + game.player.rect.width < screen.get_width():
        game.player.move_right()
    elif game.pressed.get(pygame.K_LEFT) and game.player.rect.x > 0:
        game.player.move_left()


    #Mettre à jour l'écran
    pygame.display.flip()

    # Si le joueur ferme cette fenêtre
    for event in pygame.event.get():
        # Que l'évènement est fermeture de fenêtre
        if event.type == pygame.QUIT:
            running =False
            pygame.quit()
            print("Fermeture du jeu")
        # Détecter si un joueur lache une touce du clavier
        elif event.type == pygame.KEYDOWN:
           game.pressed[event.key] = True
        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False