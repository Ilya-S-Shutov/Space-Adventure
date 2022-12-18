import pygame as pg
import configurations as conf
from sprites.sprites import ObjSprite


class Bullet(ObjSprite):
    def __init__(self, image, surface, size, pos, speed=5):
        super().__init__(image, surface, size, pos, speed)
        self.image = pg.transform.rotate(self.image, 90)

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()
