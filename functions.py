import sys
import os
import time
import pygame
import random

from bullet import Bullet
from alien import Alien
from bonus import Bonus
from stats import GameStats

import pickle

# Функция для получения пути к ресурсу
def resource_path(relative_path):
    """Определяет абсолютный путь к ресурсу, независимо от того, где запущен файл."""
    try:
        # Для PyInstaller
        base_path = sys._MEIPASS
    except Exception:
        # Для нормальной работы в разработке
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def save_game(stats, filename="savefile.pkl"):
    """
    Сохраняет данные игры в файл.

    :param stats: Объект GameStats, содержащий текущие статистические данные игры.
    :param filename: Имя файла для сохранения данных (по умолчанию "savefile.pkl").
    """
    game_data = stats.to_dict()  # Преобразует данные объекта в словарь
    with open(filename, "wb") as f:
        pickle.dump(game_data, f)
    print("Игра сохранена:", game_data)

# Загрузка игры
def load_game(stats, filename="savefile.pkl"):
    """
    Загружает данные игры из файла.

    :param stats: Объект GameStats, в который загружаются данные.
    :param filename: Имя файла для загрузки данных.
    """
    try:
        with open(filename, "rb") as f:
            game_data = pickle.load(f)
            stats.from_dict(game_data)  # Заполняем объект данными

            # Восстановление настроек игры из статистики
            stats.ai_settings.ship_speed_factor = stats.ship_speed_factor
            stats.ai_settings.bullet_speed_factor = stats.bullet_speed_factor
            stats.ai_settings.alien_speed_factor = stats.alien_speed_factor
            stats.ai_settings.alien_points = stats.alien_points

        print("Игра загружена:", game_data)
    except FileNotFoundError:
        print("Сохранение не найдено.")


def check_keydown_events(event, ai_settings, screen, ship, bullets, stats):
    """
    Реагирует на нажатие клавиш.

    :param event: Событие, произошедшее при нажатии клавиши.
    :param ai_settings: Настройки игры.
    :param screen: Экран, на котором рисуется игра.
    :param ship: Объект корабля.
    :param bullets: Группа пуль, выпущенных игроком.
    :param stats: Статистика игры.
    """
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True # Переместить корабль вправо
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True # Переместить корабль влево
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_s:
        save_game(stats)  # Сохраняем данные из объекта stats
    elif event.key == pygame.K_l:
        load_game(stats)  # Загружаем данные в объект stats

def fire_bullet(ai_settings, screen, ship, bullets):
    """
    Выпускает пулю, если максимальное количество пуль не достигнуто.

    :param ai_settings: Настройки игры.
    :param screen: Экран, на котором рисуется игра.
    :param ship: Объект корабля.
    :param bullets: Группа пуль, выпущенных игроком.
    """
    laser_sound = pygame.mixer.Sound(resource_path("sounds/laser.wav"))

    # Создание новой пули и включение её в группу bullets
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
        laser_sound.play()  # Воспроизведение звука выстрела

def check_keyup_events(event, ship):
    """
    Реагирует на отпускание клавиш.

    :param event: Событие, произошедшее при отпускании клавиши.
    :param ship: Объект корабля.
    """
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets):
    """
    Обрабатывает нажатия клавиш и события мыши.

    :param ai_settings: Настройки игры.
    :param screen: Экран, на котором рисуется игра.
    :param stats: Статистика игры.
    :param play_button: Кнопка для начала игры.
    :param ship: Объект корабля.
    :param aliens: Группа пришельцев.
    :param bullets: Группа пуль.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets, stats)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, play_button, ship,
                              aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, play_button, ship, aliens,
                      bullets, mouse_x, mouse_y):
    """
    Запускает новую игру при нажатии кнопки Play.

    :param ai_settings: Настройки игры.
    :param screen: Экран, на котором рисуется игра.
    :param stats: Статистика игры.
    :param play_button: Кнопка для начала игры.
    :param ship: Объект корабля.
    :param aliens: Группа пришельцев.
    :param bullets: Группа пуль.
    :param mouse_x: Координата мыши по оси X.
    :param mouse_y: Координата мыши по оси Y.
    """
    if play_button.rect.collidepoint(mouse_x, mouse_y):
        # сброс игровой статистики
        stats.reset_stats()
        stats.game_active = True

        # Сбросить динамические настройки на начальные значения
        ai_settings.initialize_dynamic_settings()

        # очистка списков пришельцев и пуль
        aliens.empty()
        bullets.empty()

        # создание нового флота и размещение корабля в центре
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def update_screen(ai_settings, screen, stats, ship, aliens, bullets, play_button, bonuses):
    """
    Обновляет изображение на экране и отображает новый экран.

    :param ai_settings: Настройки игры.
    :param screen: Экран, на котором рисуется игра.
    :param stats: Статистика игры.
    :param ship: Объект корабля.
    :param aliens: Группа пришельцев.
    :param bullets: Группа пуль.
    :param play_button: Кнопка для начала игры.
    :param bonuses: Группа бонусов.
    """
    # При каждом проходе цикла перерисовывается экран
    screen.fill(ai_settings.bg_color)

    # Все пули выводятся позади изображений корабля пришельцев
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()

    if stats.shield_active:
        # Отрисовка щита вокруг корабля
        pygame.draw.circle(screen, (0, 255, 0), (ship.rect.centerx, ship.rect.centery), 50, 2)


    aliens.draw(screen)
    for bonus in bonuses.sprites():
        bonus.blitme()

    # Кнопка Play отображается в том случае, если игра неактивна
    if not stats.game_active:
        play_button.draw_button()

    # Отрисовка статистики
    draw_stats(ai_settings, screen, stats)

    # Отображение последнего прорисованного экрана
    pygame.display.flip()


def draw_stats(ai_settings, screen, stats):
    """
    Отображает статистику (текущий счёт, лучший счёт, уровень, жизни) на экране.

    :param ai_settings: Настройки игры.
    :param screen: Экран, на котором рисуется игра.
    :param stats: Статистика игры.
    """
    font = pygame.font.SysFont(None, 48)

    # Жизни (Ships Left)
    lives_text = font.render(f"Корабли: {stats.ships_left}", True, (255, 255, 255))
    screen.blit(lives_text, (10, 10))

    # Отображаем уровень
    level_text = font.render(f"Уровень: {stats.level}", True, (255, 255, 255))
    screen.blit(level_text, (ai_settings.screen_width - level_text.get_width() - 10, 10))  # В правом верхнем углу

    # Текущий счёт (Current Score)
    score_text = font.render(f"Счёт: {stats.score}", True, (255, 255, 255))
    score_rect = score_text.get_rect()
    score_rect.topright = (ai_settings.screen_width - 10, 60)  # В правом верхнем углу
    screen.blit(score_text, score_rect)

    # Лучший счёт (Best Score)
    high_score_text = font.render(f"Лучший счёт: {stats.high_score}", True, (255, 255, 255))
    high_score_rect = high_score_text.get_rect()
    high_score_rect.midtop = (ai_settings.screen_width // 2, 10)  # По центру сверху
    screen.blit(high_score_text, high_score_rect)


def update_bullets(ai_settings, screen, stats, ship, aliens, bullets, bonuses):
    """
    Обновляет позиции пуль и удаляет старые пули.

    :param ai_settings: Настройки игры.
    :param screen: Экран, на котором отображается игра.
    :param stats: Статистика игры.
    :param ship: Объект корабля.
    :param aliens: Группа пришельцев.
    :param bullets: Группа пуль.
    :param bonuses: Группа бонусов.
    """

    bullets.update()

    # Удалить пули, вышедшие за пределы экрана
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    # Проверить попадания
    check_bullet_alien_collisions(ai_settings, screen, stats, ship, aliens, bullets, bonuses)

    # Проверить, уничтожен ли весь флот
    check_fleet_cleared(ai_settings, stats, screen, ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, ship, aliens, bullets, bonuses):
    """
    Проверяет попадания пуль в инопланетян и создаёт бонусы для уничтоженных пришельцев.

    :param ai_settings: Настройки игры.
    :param screen: Экран, на котором отображается игра.
    :param stats: Статистика игры.
    :param ship: Объект корабля.
    :param aliens: Группа пришельцев.
    :param bullets: Группа пуль.
    :param bonuses: Группа бонусов.
    """
    explosion_sound = pygame.mixer.Sound(resource_path("sounds/explosion.wav"))

    # Проверка попаданий пуль по инопланетянам
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            # Воспроизведение звука уничтожения
            explosion_sound.play()

            # Создать бонус для каждого уничтоженного пришельца
            for alien in aliens:
                create_bonus(ai_settings, screen, bonuses, alien)

        check_high_score(stats)

    if not aliens:
        bullets.empty()
        ai_settings.increase_speed()  # Увеличение скорости инопланетян и корабля
        stats.level += 1  # Увеличение уровня
        create_fleet(ai_settings, screen, ship, aliens) # Создаем новый флот пришельцев

def check_high_score(stats):
    """
    Проверяет, если новый рекорд, и обновляет его.

    :param stats: Статистика игры.
    """
    if stats.score > stats.high_score:
        stats.high_score = stats.score


def get_number_aliens_x(ai_settings, alien_width):
    """
    Вычисляет количество пришельцев в одном ряду.

    :param ai_settings: Настройки игры.
    :param alien_width: Ширина пришельца.
    :return: Количество пришельцев в ряду.
    """
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """
    Определяет количество рядов пришельцев, помещающихся на экране.

    :param ai_settings: Настройки игры.
    :param ship_height: Высота корабля.
    :param alien_height: Высота пришельца.
    :return: Количество рядов пришельцев.
    """
    availible_space_y = (ai_settings.screen_height -
                       (3 * alien_height) - ship_height)
    number_rows = int(availible_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """
    Создает пришельца и размещает его в соответствующем ряду.

    :param ai_settings: Настройки игры.
    :param screen: Экран, на котором отображается игра.
    :param aliens: Группа пришельцев.
    :param alien_number: Индекс пришельца в ряду.
    :param row_number: Индекс ряда.
    """
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    """
    Создает флот пришельцев, размещая их на экране.

    :param ai_settings: Настройки игры.
    :param screen: Экран, на котором отображается игра.
    :param ship: Объект корабля.
    :param aliens: Группа пришельцев.
    """
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)

    # создание флота пришельцев
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen,
                         aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    """
    Реагирует на достижение пришельцем края экрана.

    :param ai_settings: Настройки игры.
    :param aliens: Группа пришельцев.
    """


    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """
    Меняет направление флота пришельцев и опускает его вниз.

    :param ai_settings: Настройки игры.
    :param aliens: Группа пришельцев.
    """
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    """
    Обновляет позиции всех пришельцев и проверяет на столкновения с кораблем.

    :param ai_settings: Настройки игры.
    :param stats: Статистика игры.
    :param screen: Экран, на котором отображается игра.
    :param ship: Объект корабля.
    :param aliens: Группа пришельцев.
    :param bullets: Группа пуль.
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Проверка времени действия щита
    if stats.shield_active:
        current_time = pygame.time.get_ticks()
        if current_time - stats.shield_timer > ai_settings.shield_duration:
            stats.shield_active = False  # Отключаем щит

    # Проверка столкновений "пришелец - корабль"
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)

    # Проверка, добрались ли пришельцы до нижнего края
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)

def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    """
    Проверяет, добрались ли пришельцы до нижнего края экрана.

    :param ai_settings: Настройки игры.
    :param stats: Статистика игры.
    :param screen: Экран, на котором отображается игра.
    :param ship: Объект корабля.
    :param aliens: Группа пришельцев.
    :param bullets: Группа пуль.
    """
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            if stats.shield_active:
                # Уничтожить пришельца, если щит активен
                aliens.remove(alien)
            else:
                # Обработка столкновения при отсутствии щита
                ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
                break


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    """
    Обрабатывает столкновение корабля с пришельцем.

    :param ai_settings: Настройки игры.
    :param stats: Статистика игры.
    :param screen: Экран, на котором отображается игра.
    :param ship: Объект корабля.
    :param aliens: Группа пришельцев.
    :param bullets: Группа пуль.
    """
    if stats.shield_active:
        return  # Игнорируем столкновение при активном щите

    life_lost_sound = pygame.mixer.Sound(resource_path("sounds/life_lost.wav"))
    game_over_sound = pygame.mixer.Sound(resource_path("sounds/game_over.wav"))

    if stats.ships_left > 0:
        # Уменьшение количества оставшихся кораблей
        stats.ships_left -= 1

        # Воспроизведение звука потери жизни
        life_lost_sound.play()

        # Очистка списка пришельцев и пуль
        aliens.empty()
        bullets.empty()

        # Создание нового флота и размещение корабля в центре
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Пауза
        time.sleep(1)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

        # Воспроизведение звука окончания игры
        game_over_sound.play()


def check_fleet_cleared(ai_settings, stats, screen, ship, aliens, bullets):
    """
    Проверяет, уничтожен ли весь флот пришельцев.
    Если флот уничтожен, переходит на следующий уровень.

    :param ai_settings: Настройки игры.
    :param stats: Статистика игры.
    :param screen: Экран, на котором отображается игра.
    :param ship: Объект корабля.
    :param aliens: Группа пришельцев.
    :param bullets: Группа пуль.
    """
    if not aliens:
        bullets.empty() # Очистить оставшиеся пули
        level_up(stats) # Увеличить уровень через функцию level_up
        create_fleet(ai_settings, screen, ship, aliens) # Создать новый флот

def level_up(stats):
    """
    Повышает уровень игры.

    :param stats: Статистика игры.
    """
    stats.ai_settings.increase_speed()
    stats.update_from_settings()  # Обновляем статистику из настроек
    stats.level += 1

def create_bonus(ai_settings, screen, bonuses, alien):
    """
    Создает бонус с определенной вероятностью, когда инопланетянин уничтожен.

    :param ai_settings: Настройки игры.
    :param screen: Экран, на котором отображается игра.
    :param bonuses: Группа бонусов.
    :param alien: Инопланетянин, от которого будет выпасть бонус.
    """
    # Вероятность появления бонуса
    if random.random() < ai_settings.bonus_chance:
        bonus_type = random.choice(['life', 'shield'])  # Случайный тип бонуса
        bonus = Bonus(ai_settings, screen, bonus_type, alien.rect.x, alien.rect.y)
        bonuses.add(bonus)

def check_bonus_collisions(ai_settings, stats, ship, bonuses):
    """
    Проверяет столкновения бонусов с кораблем.

    :param ai_settings: Настройки игры.
    :param stats: Статистика игры.
    :param ship: Объект корабля.
    :param bonuses: Группа бонусов.
    """
    collisions = pygame.sprite.spritecollide(ship, bonuses, True)

    for bonus in collisions:
        if bonus.bonus_type == 'life':
            # Восстановление жизни
            if stats.ships_left < ai_settings.ship_limit:
                stats.ships_left += 1
        elif bonus.bonus_type == 'shield':
            # Включение временного щита
            stats.shield_active = True
            stats.shield_timer = pygame.time.get_ticks()  # Засекаем время
