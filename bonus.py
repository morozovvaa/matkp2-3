import pygame
import functions as gf

class Bonus(pygame.sprite.Sprite):
    """Класс, представляющий бонус в игре."""

    def __init__(self, ai_settings, screen, bonus_type, x, y):
        """
        Инициализирует бонус с заданным типом и начальной позицией.

        :param ai_settings: Объект настроек игры, содержащий параметры игры.
        :param screen: Экран, на котором будет отображаться бонус.
        :param bonus_type: Тип бонуса (например, 'life' или 'shield').
        :param x: Начальная позиция бонуса по оси X.
        :param y: Начальная позиция бонуса по оси Y.
        """
        super().__init__()  # Инициализация базового класса Sprite
        self.screen = screen
        self.ai_settings = ai_settings
        self.bonus_type = bonus_type  # Тип бонуса (например, 'life' или 'shield')

        # Создание изображения бонуса в зависимости от типа
        if bonus_type == 'life':
            self.image = pygame.image.load(gf.resource_path('images/bonus_life.bmp'))  # Бонус жизни
        elif bonus_type == 'shield':
            self.image = pygame.image.load(gf.resource_path('images/bonus_shield.bmp'))  # Бонус щита

        self.rect = self.image.get_rect()
        self.rect.x = x  # Устанавливаем позицию бонуса по оси X
        self.rect.y = y  # Устанавливаем позицию бонуса по оси Y

        # Скорость падения бонуса (скорость обновления позиции)
        self.speed = ai_settings.bonus_speed

    def update(self):
        """
        Обновляет позицию бонуса. Перемещает бонус вниз по экрану с заданной скоростью.

        Этот метод должен вызываться в основном игровом цикле для обновления состояния.
        """
        self.rect.y += self.speed  # Перемещает бонус вниз по экрану

    def blitme(self):
        """
        Отображает бонус на экране в текущей позиции.

        Этот метод рисует бонус на экране, используя текущее изображение и его прямоугольник.
        """
        self.screen.blit(self.image, self.rect)
