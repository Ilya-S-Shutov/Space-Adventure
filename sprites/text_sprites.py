import pygame as pg


class TextObj:
    def __init__(self, pos, start_text, font_size, surface, font='Arial', text_color=(0, 0, 0), bg_color=None):
        self.font = pg.font.SysFont(font, font_size, True)
        self.image = None
        self.bg_color = bg_color
        self.surface = surface
        self.change_color(text_color)
        self.set_text(start_text)
        self.rect = self.image.get_rect(center=pos)

    def change_color(self, color):
        self.text_color = color

    def set_text(self, text):
        self.image = self.font.render(text, True, self.text_color)

    def draw(self):
        if self.bg_color:
            pg.draw.rect(self.surface, self.bg_color, self.rect)
        self.surface.blit(self.image, self.rect)