import pygame.font


class Button:
    """
    Класс для создания и отображения кнопки на экране.

    Этот класс управляет кнопками в игре, такими как кнопка "Играть".
    Кнопка отображается в центре экрана и может быть использована для взаимодействия с пользователем.
    """

    def __init__(self, ai_settings, screen, msg):
        """
        Инициализирует атрибуты кнопки.

        :param ai_settings: Объект настроек игры (пока не используется, но может быть полезен для будущих улучшений).
        :param screen: Экран, на котором будет отображаться кнопка.
        :param msg: Текст сообщения, который будет отображён на кнопке.
        """
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Размеры кнопки
        self.width, self.height = 200, 50
        # Цвет кнопки и текста
        self.button_color = (42, 104, 52)
        self.text_color = (255, 255, 255)
        # Шрифт для текста
        self.font = pygame.font.SysFont(None, 48)

        # Построение прямоугольника для кнопки и выравнивание по центру экрана
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # Создание изображения для сообщения кнопки
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """
        Преобразует сообщение в изображение и выравнивает его по центру кнопки.

        :param msg: Текст, который должен быть отображён на кнопке.
        """
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """
        Отображает кнопку на экране с сообщением.

        Рисует прямоугольник с цветом кнопки, а затем рисует текст сообщения по центру кнопки.
        """
        self.screen.fill(self.button_color, self.rect)  # Рисует кнопку с заданным цветом
        self.screen.blit(self.msg_image, self.msg_image_rect)  # Рисует текст на кнопке
