import pygame
import functions as gf


class Ship:
    """Класс для создания и управления кораблём."""

    def __init__(self, ai_settings, screen):
        """
        Инициализирует корабль и задаёт его начальную позицию.

        Параметры:
        ai_settings (Settings): объект, содержащий параметры игры.
        screen (pygame.Surface): объект экрана, на котором будет отображаться корабль.
        """
        self.screen = screen
        self.ai_settings = ai_settings

        # Загрузка изображения корабля и получение его прямоугольника
        self.image = pygame.image.load(gf.resource_path('images/spaceship.bmp'))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Каждый новый корабль появляется у нижнего края экрана, по центру
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Сохранение вещественной координаты центра корабля для более точного контроля
        self.center = float(self.rect.centerx)

        # Флаги для управления движением корабля
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """
        Обновляет позицию корабля в зависимости от флагов движения.

        Этот метод вызывается в основном игровом цикле для обновления позиции корабля.
        Если флаг движения вправо установлен и корабль не выходит за правую границу экрана,
        то его позиция сдвигается вправо. Аналогично для движения влево.
        """
        # Обновление координаты корабля (атрибут center), не rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor

        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        # Обновление атрибута rect на основе изменённой координаты center
        self.rect.centerx = self.center

    def blitme(self):
        """
        Рисует корабль на экране в текущей позиции.

        Этот метод вызывается для отображения корабля на экране в своём текущем месте.
        """
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """
        Размещает корабль в центре нижней части экрана.

        Этот метод используется, чтобы вернуть корабль в центр экрана после его уничтожения.
        """
        self.center = self.screen_rect.centerx
