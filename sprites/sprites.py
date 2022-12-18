import pygame as pg
import os


class ObjSprite(pg.sprite.Sprite):
    def __init__(self, image, surface, size, pos, speed=0, color=None):
        super().__init__()
        img_path = os.path.join('img', image)
        self.image = pg.transform.scale(pg.image.load(img_path), size)
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed
        self.surface = surface
        self.surf_size = self.surface.get_size()

    def update(self):
        pass

    # def draw(self):
    #     self.surface.blit(self.image, self.rect)
