import pygame as pg
import os


class Button(pg.sprite.Sprite):
    def __init__(self, pos, size, surface, image_1, image_2):
        super().__init__()
        self.surface = surface
        self.state = 1
        img_path = os.path.join('img', image_1)
        self.image_1 = pg.transform.scale(pg.image.load(img_path), size)
        img_path = os.path.join('img', image_2)
        self.image_2 = pg.transform.scale(pg.image.load(img_path), size)
        self.rect = self.image_1.get_rect(center=pos)
        self.on_click = None

    def on_click(self):
        pass

    def mouse_event(self, event):
        if event.button == 1:
            if event.type == pg.MOUSEBUTTONDOWN:
                self.mouse_button_down(event)
            elif event.type == pg.MOUSEBUTTONUP:
                self.mouse_button_up(event)

    def mouse_button_down(self, event):
        if self.rect.collidepoint(event.pos):
            self.state = 2

    def mouse_button_up(self, event):
        if self.state == 2:
            self.state = 1
            self.on_click()

    def draw(self):
        if self.state == 1:
            self.surface.blit(self.image_1, self.rect)
        elif self.state == 2:
            self.surface.blit(self.image_2, self.rect)
