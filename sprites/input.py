import pygame as pg
import configurations as conf

class TextInput:
    def __init__(self, pos, size, surface):
        self.surface = surface
        self.rect = pg.rect.Rect(*size, *pos)
        self.font = self.font = pg.font.Font(None, conf.font_size)
        self.is_active = False
        self.text = 'Введите имя'
        self.update()

    def update(self):
        self.image = self.font.render(self.text, False, (0, 0, 0))

    def draw(self):
        pg.draw.rect(self.surface, conf.WHITE, self.rect)
        self.surface.blit(self.image, (self.rect.x + 5, self.rect.y + 5))

    def mouse_event(self, event):
        if event.button == 1:
            if event.type == pg.MOUSEBUTTONDOWN:
                self.mouse_button_down(event)

    def mouse_button_down(self, event):
        if self.rect.collidepoint(event.pos):
            self.is_active = True
            self.text = ''
        else:
            self.is_active = False
        self.update()

    def key_down(self, event):
        if self.is_active:
            if event.key == pg.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            self.update()
