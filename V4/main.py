import pygame
from pygame.locals import *
from pygame import mixer

# Import des classes crées
from button import *
from player import *
from world import *
from traps import *
from stalagmite import *

# Initialisation de l'audio pygame
mixer.init()
pygame.init()

# Initialisation des horloges
clock = pygame.time.Clock()
fps = 60

# Variables
screen_width = 1200
screen_height = 800

tile_size = 40
game_over = 0
main_menu = True

# Initialisation de la fenêtre
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('BLY Game - Platform game create by MERZOUGUI Lucas, MARCHAIS Baptiste, LECONTE Yoann - E3IN ESIEE-IT')


# Chargement des images
    # Gestion de l'image de fond
bg_img = pygame.image.load('assets/bg4.jpeg')
bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))

menu_bg_img = pygame.image.load('assets/menu_bg.png')
menu_bg_img = pygame.transform.scale(menu_bg_img, (screen_width, screen_height))

    # Images des boutons
restart_img = pygame.image.load('assets/restart_btn.png')
restart_btn_ratio = 3.59
restart_button_size = 200
restart_img = pygame.transform.scale(restart_img, (restart_button_size, restart_button_size/restart_btn_ratio))

start_img = pygame.image.load('assets/start_btn.png')
start_btn_ratio = 3
start_button_size = 180
start_img = pygame.transform.scale(start_img, (start_button_size, start_button_size/start_btn_ratio))

exit_img = pygame.image.load('assets/exit_btn.png')
exit_btn_ratio = 2.38
exit_button_size = 150
exit_img = pygame.transform.scale(exit_img, (exit_button_size, exit_button_size/exit_btn_ratio))

game_over_img = pygame.image.load('assets/game_over.png')



# Chargement des sons
pygame.mixer.music.load('assets/adhesivewombat-8-bit-adventure.wav')      #Charger la musique de fond
pygame.mixer.music.play(-1)                                         # Lancer la musique de fond (Boucler à l'infini)
pygame.mixer.music.set_volume(0.4)                                  # Régler le volume du son de fond
game_over_fx = pygame.mixer.Sound('assets/oof.wav')                       # Charger le son de mort
game_over_fx.set_volume(1)                                      # Régler le volume du son de mort (Mettre à 0 pour désactiver)


# Représentation du niveau
world_data = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 2, 2, 0, 0, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 2, 2, 2, 4, 4, 4, 4, 4, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1],
    [1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Création de l'objet Player
player = Player(100, screen_height - 130, "blue")

# Création des objets piége
myTraps_group = pygame.sprite.Group()
stalagmite_group = pygame.sprite.Group()

# Création du monde
world = World(world_data, tile_size, Traps, myTraps_group, Stalagmite, stalagmite_group)

# Création des objets bouton
restart_button = Button(screen_width / 2 - (restart_img.get_width() /2), screen_height / 1.8, restart_img)
start_button = Button(screen_width / 3.4, screen_height / 2, start_img)
exit_button = Button(screen_width / 1.8, screen_height / 2, exit_img)

# Boucle principale
run = True
while run:

    clock.tick(fps)             # Set les FPS

    screen.blit(bg_img, (0, 0))  # Set l'image de fond

    if main_menu == True:       # Afficher le menu principal
        screen.blit(menu_bg_img, (0, 0))        # Set l'image de fond du menu


        if exit_button.draw(screen):            # Si clique sur le bouton exit
            run = False
        if start_button.draw(screen):           # Si clique sur le bouton start
            main_menu = False
            screen.blit(bg_img, (0, 0))  # Set l'image de fond
        pygame.display.update()                 # Update constament pour prendre en compte les changements de background
    else:

        world.draw(screen)                      # Afficher le monde à l'écran

        if game_over == 0:                      # Tant que l'on est pas mort, faire bouger les pièges
            myTraps_group.update()

        myTraps_group.draw(screen)              # Afficher les piéges à l'écran
        stalagmite_group.draw(screen)           # Afficher les pièges qui bouge à l'écran

        game_over = player.update(screen, game_over, world, myTraps_group, stalagmite_group, game_over_fx)    # Récupérer en boucle si le joueur est mort

        # Si le joueur est mort
        if game_over == -1:
            screen.blit(game_over_img, (screen_width / 2 - (game_over_img.get_width() /2), screen_height /2.5 - (game_over_img.get_height() /2)))
            if restart_button.draw(screen):                     # Afficher le bouton restart
                player.reset(100, screen_height - 130, "blue")  # Reset le joueur
                game_over = 0                                   # Reset la variable game_over

        pygame.display.update()                 # Update l'affichage

    for event in pygame.event.get():            # Check si l'user quitte la fenêtre
        if event.type == pygame.QUIT:
            run = False

pygame.quit()