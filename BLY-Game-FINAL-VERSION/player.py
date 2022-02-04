import pygame
from pygame.locals import *
from pygame import mixer
from random import randint

class Player():
    death_wait = False

    last_game_ticks_jump = 0

    def __init__(self, x, y, color):
        self.reset(x, y, color)

    def update(self, screen, game_over, world, myTraps_group, stalagmite_group, game_over_fx, end_group, jump_fx1, jump_fx2, jump_fx3):
        dx = 0
        dy = 0
        walk_cooldown = 5

        if game_over == 0:
            # get keypresses
            key = pygame.key.get_pressed()
            # print("Current game_ticks ", pygame.time.get_ticks())
            # print("Jump ticks ", self.last_game_ticks_jump)
            if ((self.last_game_ticks_jump + 500) < pygame.time.get_ticks()):
                if key[pygame.K_SPACE] and self.jumped == False:
                        self.last_game_ticks_jump = pygame.time.get_ticks()

                        random_value = randint(1, 3)    # Jouer le son du saut aléatoirement
                        if (random_value == 1):
                            jump_fx1.play()
                        elif (random_value == 2):
                            jump_fx2.play()
                        elif (random_value == 3):
                            jump_fx3.play()

                        self.vel_y = -15
                        self.jumped = True
                        if self.direction == 1 or self.direction == 0:  # Si on avance ou au lancement du jeu (direction = 0)
                            self.image = self.img_right_jump
                        if self.direction == -1:  # Si on recule
                            self.image = self.img_left_jump
                if key[pygame.K_SPACE] == False:
                    self.jumped = False
                    self.image = self.images_right[self.index]
            if key[pygame.K_LEFT]:
                dx -= 5
                self.counter += 1
                self.direction = -1
            if key[pygame.K_RIGHT]:
                dx += 5
                self.counter += 1
                self.direction = 1
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False and key[pygame.K_SPACE] == False:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.img_right_normal  # Index = 0 -> Image par défaut direction droite (1)
                if self.direction == -1:
                    self.image = self.img_left_normal  # Index = 0 -> Image par défaut direction gauche (-1)

            # handle animation
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]
                if self.direction == 1:
                    self.dead_image = self.img_right_sad
                elif self.direction == -1:
                    self.dead_image = self.img_left_sad

            # add gravity
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            # check for collision
            for tile in world.tile_list:
                # check for collision in x direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                # check for collision in y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # check if below the ground i.e. jumping
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    # check if above the ground i.e. falling
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0

            # check for collision with enemies
            if pygame.sprite.spritecollide(self, myTraps_group, False):
                game_over = -1
                self.image = self.dead_image
                pygame.mixer.music.stop()
                game_over_fx.play()

            # check for collision with stalagmite
            if pygame.sprite.spritecollide(self, stalagmite_group, False):
                game_over = -1
                self.image = self.dead_image
                pygame.mixer.music.stop()
                game_over_fx.play()

            # check for collision with exit
            if pygame.sprite.spritecollide(self, end_group, False):
                game_over = 1

            # update player coordinates
            self.rect.x += dx
            self.rect.y += dy


        elif game_over == -1:
            if self.death_wait == False:
                self.image = self.dead_image
                pygame.time.delay(500)
                self.death_wait = True
            if self.rect.y > 200:
                self.rect.y += 15

        # draw player onto screen
        screen.blit(self.image, self.rect)
        # pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)       # Dessine la hitbox du joueur


        return game_over

    def reset(self, x, y, color):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0

        perso_height = 60
        perso_width = 35

        for num in range(1, 3):
            if color == "red":
                img_right = pygame.image.load(f'assets/LuffyRed{num}.png')
            elif color == "blue":
                img_right = pygame.image.load(f'assets/LuffyBlue{num}.png')
            else:
                img_right = pygame.image.load(f'assets/LuffyGreen{num}.png')

            img_right = pygame.transform.scale(img_right, (perso_width, perso_height))
            self.images_right.append(img_right)

            img_left = pygame.transform.flip(img_right, True, False)
            self.images_left.append(img_left)

        # Charger perso "Normal"
        if color == "red":
            self.img_right_normal = pygame.image.load('assets/LuffyRedNormal.png')
        elif color == "blue":
            self.img_right_normal = pygame.image.load('assets/LuffyBlueNormal.png')
        else:
            self.img_right_normal = pygame.image.load('assets/LuffyGreenNormal.png')

        self.img_right_normal = pygame.transform.scale(self.img_right_normal,
                                                       (perso_width, perso_height))  # Redimensionne right normal
        self.img_left_normal = pygame.transform.flip(self.img_right_normal, True, False)  # Mirroir right -> left

        # Charger perso "Jump"
        if color == "red":
            self.img_right_jump = pygame.image.load('assets/LuffyRedJump.png')
        elif color == "blue":
            self.img_right_jump = pygame.image.load('assets/LuffyBlueJump.png')
        else:
            self.img_right_jump = pygame.image.load('assets/LuffyGreenJump.png')

        self.img_right_jump = pygame.transform.scale(self.img_right_jump,
                                                     (perso_width, perso_height))  # Redimensionne right normal
        self.img_left_jump = pygame.transform.flip(self.img_right_jump, True, False)  # Mirroir right -> left

        # Charger perso "Sad"
        if color == "red":
            self.img_right_sad = pygame.image.load('assets/LuffyRedSad.png')
        elif color == "blue":
            self.img_right_sad = pygame.image.load('assets/LuffyBlueSad.png')
        else:
            self.img_right_sad = pygame.image.load('assets/LuffyGreenSad.png')

        self.img_right_sad = pygame.transform.scale(self.img_right_sad,
                                                    (perso_width, perso_height))  # Redimensionne right normal
        self.img_left_sad = pygame.transform.flip(self.img_right_sad, True, False)  # Mirroir right -> left

        # Par défaut la première image right
        self.image = self.img_right_normal

        self.dead_image = self.img_right_sad

        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.in_air = True

        self.death_wait = False
        pygame.mixer.music.play()
