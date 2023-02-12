import pygame as pg
from sprites.base import ObjSprite


class Player(ObjSprite):

    def update(self):
        """
        Реализация перемещения персонажа.
        """
        pressed = pg.key.get_pressed()

        if pressed[pg.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
            # if self.rect.bottom < 0:
            #     self.rect.top = self.surf_size[1]

        if pressed[pg.K_DOWN] and self.rect.bottom < self.surf_size[1]:
            self.rect.y += self.speed
            # if self.rect.top > self.surf_size[1]:
            #     self.rect.bottom = 0

        if pressed[pg.K_RIGHT]:
            self.rect.x += self.speed
            if self.rect.left > self.surf_size[0]:
                self.rect.right = 0

        if pressed[pg.K_LEFT]:
            self.rect.x -= self.speed
            if self.rect.right < 0:
                self.rect.left = self.surf_size[0]

    def move_to(self, coord):
        """
        Перемещение персонажа в указанную точку.
        """
        self.rect.center = coord
