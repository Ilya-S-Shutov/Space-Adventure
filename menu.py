import pygame as pg
import configurations as conf
from sprites import Button
from sprites import TextInput
import os


class Menu:
    """
    Стартовое меню.
    """
    def __init__(self, main_surf):
        """
        Оформление меню.
        """
        self.main_surf = main_surf
        self.surface = pg.surface.Surface(conf.win_size)
        # self.rect = self.surface.get_rect()

        self.text_input = TextInput(
            conf.input_size,
            conf.input_pos,
            self.surface
        )

        self.play_button = Button(
            conf.play_button_pos,
            conf.play_button_size,
            self.surface,
            conf.play_button_1,
            conf.play_button_2
        )
        self.quit_button = Button(
            conf.quit_button_pos,
            conf.quit_button_size,
            self.surface,
            conf.quit_button_1,
            conf.quit_button_2
        )
        instr_path = os.path.join('img', conf.instr)
        self.instr = pg.transform.scale(pg.image.load(instr_path), conf.instr_size)

    def get_name(self):
        """
        Извлечение текста из поля для ввода.
        :return: str
        """
        return self.text_input.text

    def draw(self):
        """
        Отрисовка меню.
        """
        self.main_surf.blit(self.surface, (0, 0))
        # pg.draw.rect(self.surface, conf.MENU, self.rect)
        self.surface.fill(conf.MENU)
        self.surface.blit(self.instr, conf.instr_pos)
        self.play_button.draw()
        self.quit_button.draw()
        self.text_input.draw()
