import pygame as pg
from random import randint
from .base import ObjSprite


class Enemy(ObjSprite):

    def __init__(self, image, surface, size, pos, speed):
        super().__init__(image, surface, size, pos, speed)
        self.speed_x = randint(-1, 1)

    def update(self):
        self.rect.y += self.speed
        self.rect.x += self.speed_x
        if self.rect.y > self.surf_size[1]:
            self.kill()




