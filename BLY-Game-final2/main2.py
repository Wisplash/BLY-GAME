import pygame
from pygame.locals import *
from pygame import mixer

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 1500
screen_height = 1000

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')

# define game variables
tile_size = 50
game_over = 0
main_menu = True

# load images
sun_img = pygame.image.load('assets/sun.png')
bg_img = pygame.image.load('assets/bg4.jpeg')
bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))
restart_img = pygame.image.load('assets/restart_btn.png')
start_img = pygame.image.load('assets/start_btn.png')
exit_img = pygame.image.load('assets/exit_btn.png')


#load sounds
pygame.mixer.music.load('assets/adhesivewombat-8-bit-adventure.wav')
pygame.mixer.music.play(-1, 0.0, 5000)
# coin_fx = pygame.mixer.Sound('img/coin.wav')
# coin_fx.set_volume(0.5)
jump_fx = pygame.mixer.Sound('assets/jump.wav')
jump_fx.set_volume(0.5)
# game_over_fx = pygame.mixer.Sound('assets/oof.wav')
# game_over_fx.set_volume(0.5)

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False

        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False


        #draw button
        screen.blit(self.image, self.rect)

        return action


class Player():
    death_wait = False
    def __init__(self, x, y, color):
        self.reset(x, y, color)

    def update(self, game_over):
        dx = 0
        dy = 0
        walk_cooldown = 5

        if game_over == 0:
            # get keypresses
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False:
                jump_fx.play()
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
            if pygame.sprite.spritecollide(self, ennemi_group, False):
                game_over = -1
                self.image = self.dead_image
                pygame.mixer.music.stop()
                # game_over_fx.play()

            # check for collision with stalagmite
            if pygame.sprite.spritecollide(self, stalagmite_group, False):
                game_over = -1
                self.image = self.dead_image
                pygame.mixer.music.stop()
                # game_over_fx.play()

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
        # pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)


        return game_over

    def reset(self, x, y, color):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0

        perso_width = 71.5
        perso_height = 50

        for num in range(1, 3):
            if color == "red":
                img_right = pygame.image.load(f'assets/LuffyRed{num}.png')
            elif color == "blue":
                img_right = pygame.image.load(f'assets/LuffyBlue{num}.png')
            else:
                img_right = pygame.image.load(f'assets/LuffyGreen{num}.png')

            img_right = pygame.transform.scale(img_right, (perso_height, perso_width))
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
                                                       (perso_height, perso_width))  # Redimensionne right normal
        self.img_left_normal = pygame.transform.flip(self.img_right_normal, True, False)  # Mirroir right -> left

        # Charger perso "Jump"
        if color == "red":
            self.img_right_jump = pygame.image.load('assets/LuffyRedJump.png')
        elif color == "blue":
            self.img_right_jump = pygame.image.load('assets/LuffyBlueJump.png')
        else:
            self.img_right_jump = pygame.image.load('assets/LuffyGreenJump.png')

        self.img_right_jump = pygame.transform.scale(self.img_right_jump,
                                                     (perso_height, perso_width))  # Redimensionne right normal
        self.img_left_jump = pygame.transform.flip(self.img_right_jump, True, False)  # Mirroir right -> left

        # Charger perso "Sad"
        if color == "red":
            self.img_right_sad = pygame.image.load('assets/LuffyRedSad.png')
        elif color == "blue":
            self.img_right_sad = pygame.image.load('assets/LuffyBlueSad.png')
        else:
            self.img_right_sad = pygame.image.load('assets/LuffyGreenSad.png')

        self.img_right_sad = pygame.transform.scale(self.img_right_sad,
                                                    (perso_height, perso_width))  # Redimensionne right normal
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


class World():
    def __init__(self, data):
        self.tile_list = []

        # load images
        dirt_img = pygame.image.load('assets/IceBlock2.png')
        grass_img = pygame.image.load('assets/IceBlock1.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    ennemi = Enemy(col_count * tile_size, row_count * tile_size)
                    ennemi_group.add(ennemi)
                if tile == 6:
                    stalagmite = Stalagmite(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                    stalagmite_group.add(stalagmite)

                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/stalactite.png')
        self.image = pygame.transform.flip(self.image, False, True)
        self.image = pygame.transform.scale(self.image, (tile_size - (tile_size / 2) , tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 40:
            self.move_direction *= -1
            self.move_counter *= -1


class Stalagmite(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('assets/stalactite.png')
        img = pygame.transform.flip(img, False, True)
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - (tile_size / 2)


world_data = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 7, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 7, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 2, 0, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 2, 0, 0, 4, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 2, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 2, 2, 2, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 6, 6, 6, 6, 6, 6, 6, 2, 2, 2, 1],
    [1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

player = Player(100, screen_height - 130, "blue")

ennemi_group = pygame.sprite.Group()
stalagmite_group = pygame.sprite.Group()

world = World(world_data)

restart_button = Button(screen_width // 2 - 50, screen_height // 2 + 100, restart_img)
start_button = Button(screen_width // 2 - 350, screen_height // 2, start_img)
exit_button = Button(screen_width // 2 + 150, screen_height // 2, exit_img)

run = True
while run:

    clock.tick(fps)

    screen.blit(bg_img, (0, 0))
    screen.blit(sun_img, (100, 100))

    if main_menu == True:
        if exit_button.draw():
            run = False
        if start_button.draw():
            main_menu = False
    else:
        world.draw()

        if game_over == 0:
            ennemi_group.update()

        ennemi_group.draw(screen)
        stalagmite_group.draw(screen)

        game_over = player.update(game_over)

        # if player has died
        if game_over == -1:
            if restart_button.draw():
                player.reset(100, screen_height - 130, "blue")
                game_over = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        pygame.display.update()

pygame.quit()