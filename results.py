import pygame as pg
import configurations as conf
from sprites import Button
from sprites.base import TextObj


class Results:
    """
    Оформление экрана результатов.
    """
    def __init__(self, main_surf):
        self.main_surf = main_surf
        self.surface = pg.surface.Surface(conf.win_size)
        self.cur_res = TextObj(conf.cur_res_pos,
                               '',
                               20,
                               self.surface,
                               bg_color=conf.WHITE)
        self.button = Button(conf.next_button_pos,
                             conf.next_button_size,
                             self.surface,
                             conf.next_button_1,
                             conf.next_button_2)

        self.font = pg.font.SysFont('Arial', 20, True)
        self.line_1 = []
        self.line_2 = []

    def update_table(self, res, name, cur_res):
        self.line_1 = []
        self.line_2 = []
        self.cur_res.set_text(f'{name}, ваш результат: {cur_res}!')
        self.line_1 = [self.font.render('Name', True, conf.BLACK)]
        self.line_2 = [self.font.render('Score', True, conf.BLACK)]
        for i, row in enumerate(res):
            self.line_1.append(self.font.render(row[0], True, conf.BLACK))
            self.line_2.append(self.font.render(str(row[1]), True, conf.BLACK))
            if i >= 5:
                break

    def draw(self):
        self.main_surf.blit(self.surface, (0, 0))
        self.surface.fill(conf.MENU)
        self.cur_res.draw()
        self.button.draw()
        for i, item in enumerate(self.line_1):
            self.surface.blit(item, (conf.win_size[0]/3, conf.win_size[1]/3 + i*25))
            self.surface.blit((self.line_2[i]), (conf.win_size[0]*2/3, conf.win_size[1] / 3 + i * 25))
