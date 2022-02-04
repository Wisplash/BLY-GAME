import pygame
from pygame.locals import *
from pygame import mixer

# Import des classes crées
from button import *
from player import *
from world import *
from traps import *
from stalagmite import *
from end_lvl import *

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

level = 0
max_levels = 2
world_lvl = []
world_list = []

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

win_img = pygame.image.load('assets/win.png')


# Chargement des sons
pygame.mixer.music.load('assets/adhesivewombat-8-bit-adventure.wav')         #Charger la musique de fond
pygame.mixer.music.play(-1)                                     # Lancer la musique de fond (Boucler à l'infini)
pygame.mixer.music.set_volume(0.5)                                # Régler le volume du son de fond

jump_fx1 = pygame.mixer.Sound('assets/jump1.wav')                              # Charger le son du jump 1
jump_fx1.set_volume(0.5)                                         # Régler le volume du son de jump 1
jump_fx2 = pygame.mixer.Sound('assets/jump2.wav')                              # Charger le son du jump 2
jump_fx2.set_volume(0.5)                                         # Régler le volume du son de jump 2
jump_fx3 = pygame.mixer.Sound('assets/jump3.wav')                              # Charger le son du jump 3
jump_fx3.set_volume(0.5)                                         # Régler le volume du son de jump 3

game_over_fx = pygame.mixer.Sound('assets/oof.wav')                          # Charger le son de mort
game_over_fx.set_volume(1)                                      # Régler le volume du son de mort (Mettre à 0 pour désactiver)


# Fonction pour reset les levels
def reset_level(color, world_lvl):
    player.reset(100, screen_height - 130, color)
    myTraps_group.empty()
    stalagmite_group.empty()
    end_group.empty()

    world = World(world_lvl, tile_size, Traps, myTraps_group, Stalagmite, stalagmite_group, End_lvl, end_group)

    return world


# Représentation des niveaux
lvl1 = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 1],
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
world_lvl.append(lvl1)


lvl2 = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 2, 2, 0, 0, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1],
    [1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
world_lvl.append(lvl2)

lvl3 = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1],
    [1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
world_lvl.append(lvl3)

# Création de l'objet Player
player = Player(100, screen_height - 130, "blue")

# Création des objets intéractifs
myTraps_group = pygame.sprite.Group()
stalagmite_group = pygame.sprite.Group()
end_group = pygame.sprite.Group()

# Création des mondes
for i in range(len(world_lvl)):
    temp =  World(world_lvl[i], tile_size, Traps, myTraps_group, Stalagmite, stalagmite_group, End_lvl, end_group)
    world_list.append(temp)

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


        world_list[0].draw(screen)              # Afficher le monde 0

        if game_over == 0:                      # Tant que l'on est pas mort, faire bouger les pièges
            myTraps_group.update()

        myTraps_group.draw(screen)              # Afficher les piéges à l'écran
        stalagmite_group.draw(screen)           # Afficher les pièges qui bouge à l'écran
        end_group.draw(screen)                 # Afficher la porte finale

        game_over = player.update(screen, game_over, world_list[0], myTraps_group, stalagmite_group, game_over_fx, end_group, jump_fx1, jump_fx2, jump_fx3)    # Récupérer en boucle si le joueur est mort

        # Si le joueur est mort
        if game_over == -1:
            screen.blit(game_over_img, (screen_width / 2 - (game_over_img.get_width() /2), screen_height /2.5 - (game_over_img.get_height() /2)))
            if restart_button.draw(screen):                     # Afficher le bouton restart
                world_data = []
                world_list[0] = reset_level("blue", world_lvl[0])   # Afficher le monde 0 + reset de tout
                game_over = 0

        # if player has completed the level
        if game_over == 1:
            # reset game and go to next level
            level += 1

            if level == 1:                                              # Level 1
                # reset level
                world_data = []
                world_list[0] = reset_level("red", world_lvl[level])
                game_over = 0
            if level == 2:                                              # Level 2
                # reset level
                world_data = []
                world_list[0] = reset_level("green", world_lvl[level])
                game_over = 0

            else:
                screen.blit(win_img, (screen_width / 2 - (win_img.get_width() / 2), screen_height / 3 - (win_img.get_height() / 2)))
                if restart_button.draw(screen):
                    level = 1
                    # reset level
                    world_data = []
                    world_list[0] = reset_level("blue", world_lvl[0])
                    game_over = 0

        pygame.display.update()                 # Update l'affichage

    for event in pygame.event.get():            # Check si l'user quitte la fenêtre
        if event.type == pygame.QUIT:
            run = False

pygame.quit()