import pygame
from pygame.locals import *
from pygame import mixer

class World():
    def __init__(self, data, tile_size, Traps, myTraps_group, Stalagmite, stalagmite_group):
        self.tile_list = []

        # load images
        iceblock_img = pygame.image.load('assets/IceBlock.png')
        icecobble_img = pygame.image.load('assets/IceCobble.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(iceblock_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(icecobble_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    myTraps = Traps(col_count * tile_size, row_count * tile_size, tile_size)
                    myTraps_group.add(myTraps)
                if tile == 4:   # Stalagmite traps
                    stalagmite = Stalagmite(col_count * tile_size, row_count * tile_size + (tile_size // 2), tile_size)
                    stalagmite_group.add(stalagmite)

                col_count += 1
            row_count += 1

    def draw(self, screen):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)