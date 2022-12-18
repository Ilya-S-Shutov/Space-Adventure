import pygame as pg
import sys
import os


class Game:
    """
    Класс задаёт основную структуру и логику работы игры.
    """
    def __init__(self, size=(700, 500), caption='MyGame',
                 fps=60, bg_image=None, color=(0, 0, 0), music=None):
        pg.init()
        pg.font.init()
        pg.mixer.init()

        self.window = pg.display.set_mode(size)
        pg.display.set_caption(caption)

        self.clock = pg.time.Clock()

        if bg_image:
            bg_image = os.path.join('img', bg_image)
            self.bg = pg.transform.scale(pg.image.load(bg_image), size)
        else:
            self.bg = bg_image
        self.bg_color = color
        self.fps = fps
        self.game_over = False

        self.objects = pg.sprite.Group()
        self.labels = list()
        self.sounds = dict()

        self.keydown_handlers = list()
        self.keyup_handlers = list()
        self.user_handler = None
        self.mouse_handlers = []

        self.music_on = False
        if music:
            self.music = os.path.join('sounds', music)
            self.set_music(self.music)
            pg.mixer.music.play(-1)
            pg.mixer.music.pause()

    def add_sound(self, name: str, sound: str):
        """
        Метод добавляет пару: ключ-звуковой эффект в словарь.
        :param name: ключевое слово для обращения.
        :param sound: имя файла в папке звуков.
        """
        sound = os.path.join('sounds', sound)
        self.sounds[name] = pg.mixer.Sound(sound)

    def music_swich(self):
        """
        Переключение паузы фоновой музыки.
        """
        if self.music_on:
            self.music_on = False
            pg.mixer.music.pause()
        else:
            self.music_on = True
            pg.mixer.music.unpause()

    def set_music(self, music: str):
        """
        Добавляет фоновую музыку.
        :param music: имя файла с музыкой.
        """
        pg.mixer.music.load(self.music)

    def bg_draw(self):
        """
        Отрисовка заднего фона в зависимости от того, выбрана ли фоновая картинка или одноцветная заливка.
        """
        if self.bg:
            self.window.blit(self.bg, (0, 0))
        else:
            self.window.fill(self.bg_color)

    def draw(self):
        """
        Отрисовка всех игровых объектов.
        """
        self.bg_draw()
        self.objects.draw(self.window)
        for item in self.labels:
            item.draw()

    def update(self):
        """
        ООбновление состояний всех игровых объектов.
        """
        self.objects.update()

    def events(self):
        """
        Метод отвечает за обработку всех событий.
        Он перенаправляет объект события в необходимые обработчики из зарегистрированных в списках обработчиков.
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

            elif event.type == pg.USEREVENT and callable(self.user_handler):
                self.user_handler()

            elif event.type == pg.KEYDOWN:
                for handler in self.keydown_handlers:
                    handler(event)

            elif event.type in (pg.MOUSEBUTTONDOWN,
                                pg.MOUSEBUTTONUP):
                for handler in self.mouse_handlers:
                    handler(event)

    def exec_(self):
        """
        Главный игровой цикл.
        """
        while not self.game_over:
            self.events()
            self.update()
            self.draw()

            pg.display.update()
            self.clock.tick(self.fps)