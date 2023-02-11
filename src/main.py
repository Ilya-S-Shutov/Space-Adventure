import pygame as pg
import os

from screens import Game, Menu, Results
from sprites import Player, Bullet, Enemy
from sprites.base import TextObj

from data_base import DataBase
import configurations as conf
from random import randint

os.chdir(os.path.split(os.path.abspath(__file__))[0])


class SpaceAdventure(Game):
    """
    Класс, содержащий основную логику игры. Предусмотрен один пользовательский тип событий и
    смена состояний: menu, game, results, от которых зависит отображение текущего экрана. Подключена
    база данных для записи результатов
    """

    def __init__(self):
        super().__init__(
            size=conf.win_size,
            caption=conf.caption,
            fps=conf.fps,
            bg_image=conf.bg_img,
            music=conf.bg_music
            )

        self.enemy_speed_ticks = pg.time.get_ticks()
        self.enemy_rate_ticks = pg.time.get_ticks()
        self.bullet_ticks = pg.time.get_ticks()
        self.enemy_ticks = pg.time.get_ticks()

        self.enemies = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.user_handler = self.change_time

        self.name = None
        self.lives = None
        self.time = None
        self.score = None
        self.enemy_speed = None
        self.enemy_rate = None
        self.winner = False
        self.is_game_over = False

        self.create_main()

        self.state = 'menu'

        self.db = DataBase('db_file.sqlite')
        self.db.execute('CREATE TABLE IF NOT EXISTS results (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, scores INTEGER)')

    def start(self):
        """
        Метод обнуляет ключевые переменные игровой сессии.
        """
        pg.time.set_timer(pg.USEREVENT, conf.delay)
        self.lives = conf.start_lives
        self.time = conf.start_time
        self.score = 0
        self.enemy_speed = conf.enemy_speed
        self.enemy_rate = conf.enemy_rate
        self.winner = False
        self.is_game_over = False
        self.labels_update()

    def create_main(self):
        """
        Метод вызывает методы для создания спрайта игрока, спрайтов надписей, привязки звуковых эффектов
        главного меню и окна результатов.
        """
        self.create_player()
        self.create_labels()
        self.create_sounds()
        self.create_menu()
        self.create_results()

    def create_sounds(self):
        """
        Медтод добавляет в игру звуковые эффекты.
        """
        self.add_sound('fail', conf.fail)
        self.add_sound('lose', conf.lose)
        self.add_sound('destruction', conf.destruction)
        self.add_sound('button', conf.button)

    def create_player(self):
        """
        Метод создаёт спрайт главного персонажа (ракеты).
        """
        self.player = Player(
                conf.player_img,
                self.window,
                conf.player_size,
                (conf.win_size[0] / 2, conf.win_size[1] * 0.8),
                conf.player_speed
            )
        self.objects.add(self.player)

    def create_enemies(self):
        """
        Метод создаёт спрайты врагов (метеоров), координата по горизонтали выбирается случайным образом.
        """
        enemy = Enemy(
                conf.enemy_img,
                self.window,
                conf.enemy_size,
                (randint(0, conf.win_size[0] - conf.enemy_size[0]), 0),
                self.enemy_speed
            )
        self.objects.add(enemy)
        self.enemies.add(enemy)

    def create_bullet(self):
        """
        Метод создаёт спрайты двух снарядов. Место появления привязано к координатам ракеты.
        """
        bullet_left = Bullet(
                conf.bullet_img,
                self.window,
                conf.bullet_size,
                (self.player.rect.center[0] - self.player.rect.size[0]/3,
                self.player.rect.center[1]),
                conf.bullet_speed
            )
        bullet_right = Bullet(
            conf.bullet_img,
            self.window,
            conf.bullet_size,
            (self.player.rect.center[0] + self.player.rect.size[0]/6,
            self.player.rect.center[1]),
            conf.bullet_speed
        )
        self.objects.add(bullet_left, bullet_right)
        self.bullets.add(bullet_left, bullet_right)

    def create_labels(self):
        """
        Метод создаёт спрайты-надписи: жизнь, таймер, очки
        """
        self.time_label = TextObj(
                conf.time_label_pos,
                f'Time: {self.time}',
                conf.font_size,
                self.window,
                text_color=conf.GREEN
        )
        self.lives_label = TextObj(
            conf.lives_label_pos,
            f'HP: {self.lives}',
            conf.font_size,
            self.window,
            text_color=conf.GREEN
        )
        self.score_label = TextObj(
            conf.score_label_pos,
            f'Score: {self.score}',
            conf.font_size,
            self.window,
            text_color=conf.GREEN
        )
        self.labels.extend([self.time_label, self.lives_label, self.score_label])

    def create_results(self):
        """
        Метод создаёт финальный экран. Добавляет кнопке возможность переключения на главное меню.
        Добавляет обработчики событий к списку обработчиков.
        """
        self.results = Results(self.window)

        def restart():
            """
            Функция подключение звукового эффекта, смена состояния на 'menu' для возврата к стартовому экрану.
            """
            self.sounds['button'].play()
            self.state = 'menu'

        self.results.button.on_click = restart
        self.mouse_handlers.append(self.results.button.mouse_event)

    def update_results(self):
        """
        Метод сохраняет текущий результат в БД, после чего запрашивает 5 лучших результатов
        (с фильтрацией по уникальным именам). Обновляет таблицу экрана результатов
        """
        self.db.execute('INSERT INTO results (username, scores) VALUES (?, ?)', (self.name, self.score))
        self.db.commit()
        top_res = self.db.query('SELECT DISTINCT username, scores FROM results ORDER BY scores DESC')
        self.results.update_table(top_res, self.name, self.score)

    def create_menu(self):
        """
        Метод создаёт экран стартового меню. Добавляет функционал двум кнопкам экрана.
        Добавляет обработчики событий к списку обработчиков.
        """
        self.menu = Menu(self.window)

        def play():
            """
            Функция переключает состояние на 'game', что позволяет начать основную игру.
            Обнуляет ключевые переменные игровой сессии, сохраняет введённое имя игрока. Возобновляет проигрывание
            фоновой музыки и подключает звуковой эффект к нажатию кнопки.
            Стирает всех оставшихся с предыдущей сессии противников.
            Перемещает игрока в стартовую точку.
            """
            self.sounds['button'].play()
            self.music_swich()
            self.state = 'game'
            self.start()
            self.name = self.menu.get_name()
            for enemy in self.enemies:
                enemy.kill()
            self.player.move_to((conf.win_size[0] / 2, conf.win_size[1] * 0.8))

        def game_exit():
            """
            Функция позволяет выйти из игры, зафиксировав окончательные изменения в БД.
            """
            self.sounds['button'].play()
            self.db.close()
            quit_event = pg.event.Event(pg.QUIT)
            pg.event.post(quit_event)

        self.menu.play_button.on_click = play
        self.menu.quit_button.on_click = game_exit

        self.mouse_handlers.extend([self.menu.text_input.mouse_event, self.menu.play_button.mouse_event, self.menu.quit_button.mouse_event])
        self.keydown_handlers.append(self.menu.text_input.key_down)

    def collide_enemies(self):
        """
        Проверка столкновений врагов. При столкновении с персонажем, снимается одна жизнь, враг исчезает.
        При столкновении с пулей, добавляются очки, исчезают оба спрайта.
        """
        player_collide = pg.sprite.spritecollide(self.player, self.enemies, True)
        if player_collide:
            if self.lives > 1:
                self.sounds['fail'].play()
            else:
                self.sounds['lose'].play()
            self.change_lives()

        bullets_collide = pg.sprite.groupcollide(self.bullets, self.enemies, True, True)
        if bullets_collide:
            self.change_score()
            self.sounds['destruction'].play()

    def labels_update(self):
        """
        Метод обновления содержимого надписей.
        """
        self.time_label.set_text(f'Time: {self.time}')
        self.score_label.set_text(f'Score: {self.score}')
        self.lives_label.set_text(f'HP: {self.lives}')

    def change_time(self):
        """
        Метод изменяет значение таймера. При переходе через "переломные точки", надпись меняет цвет:
        с зелёного на жёлтый, с жёлтого на красный.
        """
        self.time -= 1
        if conf.start_time * 0.33 < self.time < conf.start_time * 0.66:
            self.time_label.change_color(conf.YELLOW)
        elif self.time < conf.start_time * 0.33:
            self.time_label.change_color(conf.RED)

    def change_score(self):
        """
        Метод изменяет значение очков.
        """
        self.score += 10

    def change_lives(self):
        """
        Метод изменяет значение жизней. При переходе через "переломные точки", надпись меняет цвет:
        с зелёного на жёлтый, с жёлтого на красный.
        """
        self.lives -= 1
        if conf.start_lives * 0.33 < self.time < conf.start_lives * 0.66:
            self.lives_label.change_color(conf.YELLOW)
        elif self.lives < conf.start_lives * 0.33:
            self.lives_label.change_color(conf.RED)

    def time_events(self):
        """
        Метод отслеживает действия, зависящие от времени. Один раз в определённое кол-во игровых
        "тиков" происходит появление врагов, пуль, а также изменение скорости новых врагов и уменьшение
        между появлением новых врагов.
        """
        now = pg.time.get_ticks()

        if now - self.enemy_speed_ticks > conf.change_speed_delay:
            self.enemy_speed_ticks = now
            self.enemy_speed += conf.change_speed_step

        if now - self.enemy_rate_ticks > conf.change_rate_delay:
            self.enemy_rate_ticks = now
            self.enemy_rate -= conf.change_rate_step

        if now - self.bullet_ticks > conf.bullet_rate:
            self.bullet_ticks = now
            self.create_bullet()

        if now - self.enemy_ticks > self.enemy_rate:
            self.enemy_ticks = now
            self.create_enemies()

    def calc_final_score(self):
        """
        Метод для подсчёта очков.
        """
        if self.winner:
            self.score = self.score + 1000 + 500 * self.lives

    def draw(self):
        """Модифицированный метод отрисовки всех игровых объектов"""
        if self.state == 'game':
            super().draw()
        elif self.state == 'menu':
            self.menu.draw()
        elif self.state == 'results':
            self.results.draw()

    def update(self):
        """Модифицированный метод изменения состояний всех игровых объектов"""
        if self.state == 'game':

            if self.time <= 0 and self.lives >= 1:
                self.winner = True
                self.is_game_over = True

            if self.lives <= 0:
                self.is_game_over = True

            if self.is_game_over:
                self.calc_final_score()
                self.state = 'results'
                self.music_swich()
                self.update_results()

            self.time_events()
            self.collide_enemies()
            self.labels_update()
            super().update()


if __name__ == '__main__':
    SpaceAdventure().exec_()


