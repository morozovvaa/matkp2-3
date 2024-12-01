import pygame
from pygame.sprite import Sprite
import functions as gf


class Alien(Sprite):
    """Класс, представляющий одного пришельца"""

    def __init__(self, ai_settings, screen):
        """
        Инициализирует пришельца и задаёт его начальную позицию.

        :param ai_settings: Объект, содержащий настройки игры.
        :param screen: Объект экрана, на котором будет отображаться пришелец.
        """
        super().__init__()  # Инициализация родительского класса Sprite
        self.screen = screen
        self.ai_settings = ai_settings

        # Загрузка изображения пришельца и назначение атрибута rect
        self.image = pygame.image.load(gf.resource_path('images/alienship.bmp'))
        self.rect = self.image.get_rect()

        # Каждый новый пришелец появляется в левом верхнем углу экрана
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Сохранение точной позиции пришельца для более точных вычислений
        self.x = float(self.rect.x)

    def blitme(self):
        """
        Отображает пришельца в его текущей позиции на экране.

        Вызывает метод `blit`, чтобы отобразить изображение пришельца в его
        текущем прямоугольнике `rect`.
        """
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """
        Проверяет, находится ли пришелец у края экрана.

        :return: True, если пришелец касается края экрана (слева или справа).
        """
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """
        Перемещает пришельца влево или вправо.

        Обновляет позицию пришельца, учитывая текущую скорость и направление
        (вправо или влево) с помощью параметра `fleet_direction` из настроек игры.
        """
        self.x += (self.ai_settings.alien_speed_factor *
                   self.ai_settings.fleet_direction)
        self.rect.x = self.x