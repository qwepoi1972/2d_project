import pygame
from random import randint


class Player(pygame.sprite.Sprite):
    def __init__(self, screen, start_x, start_y):
        """
        Класс модельки, управляемой игроком.
        Способен передвигаться горизонтально и вертикально по нажатию соответствующих клавиш клавиатуры.
        Способен совершать прыжки на некоторое расстояние.
        :param screen: Surface - поверхность, на которую отрисовывается моделька.
        :param start_x: int - координата x экрана, на которой появляется моделька.
        :param start_y: int - координата y экрана, на которой появляется моделька.
        """

        super().__init__()
        self.screen = screen
        self.image_stand = pygame.image.load("mario_stand_right.png")
        self.image_jump = pygame.image.load("mario_jump_right.png")
        self.rect = self.image_stand.get_rect()  # (start_x, start_y, 38, 72)
        self.rect[0], self.rect[1] = start_x, start_y
        self.reflection = False
        self.speed_x = 0
        self.speed_y = 0
        self.speed_max = 10
        self.speed_jump = 20
        self.star_check = False

    def check_collision_platforms(self, platforms):
        """
        Метод проверки коллизии с платформами.
        :param platforms: array - массив платформ, с которыми возможна коллизия.
        """
        self.rect[0] += round(self.speed_x)
        self.rect[1] -= round(self.speed_y)
        collide = pygame.sprite.spritecollideany(self, platforms)
        self.rect[0] -= round(self.speed_x)
        self.rect[1] += round(self.speed_y)
        for platform in platforms:
            if collide and abs(self.rect.bottom - platform.rect.top) <= 7:
                return True, platform
        return False, None

    def check_collision_stars(self, stars):
        """
        Метод проверки коллизии со звёздами.
        :param stars: array - массив звёзд, с которыми возможна коллизия.
        """
        collide = pygame.sprite.spritecollideany(self, stars)
        if collide:
            self.star_check = True
            pygame.time.set_timer(pygame.USEREVENT+1, 3000)
            return True
        else:
            return False

    def draw(self, platforms):
        """
        Метод отрисовки объекта класса.
        Рисует модельку объекта класса с учётом направления нажатых клавиш(влево или вправо) на поверхности self.screen.
        :param platforms: array, передаётся массив платформ для проверки коллизии.
        """
        collide = self.check_collision_platforms(platforms)[1]
        if not collide:
            self.screen.blit(pygame.transform.flip(self.image_jump, self.reflection, False), self.rect)
        else:
            self.screen.blit(pygame.transform.flip(self.image_stand, self.reflection, False), self.rect)


class Platform(pygame.sprite.Sprite):
    def __init__(self, screen, pos_y, width, height):
        """
        Класс платформ, способных к коллизии с моделькой игрока.
        Основа для разных типов платформ.
        :param screen: Surface - поверхность, на которую отрисовывается платформа.
        :param pos_y: int - координата y экрана, на которой появляется моделька.
        :param width: int - толщина в пикселях платформы.
        :param height: int - высота в пикселях платформы.
        """
        super().__init__()
        self.screen = screen
        self.pos_x = randint(40, 640)
        self.image = pygame.image.load("platform.jpg")
        self.surf = pygame.transform.scale(self.image, (width, height))
        self.rect = pygame.Rect(self.pos_x, pos_y, width, height)

    def draw(self):
        """
        Метод отрисовки объекта класса.
        Рисует модельку объекта класса.
        """
        self.screen.blit(self.surf, self.rect)


class HorizontalMovingPlatform(Platform):
    def __init__(self, screen, pos_y, width, height):
        """
        Класс платформ, способных к коллизии с моделькой игрока и движению горизонтально с постоянной скоростью.
        :param screen: Surface - поверхность, на которую отрисовывается платформа.
        :param pos_y: int - координата y экрана, на которой появляется моделька.
        :param width: int - толщина в пикселях платформы.
        :param height: int - высота в пикселях платформы.
        """
        super().__init__(screen=screen, pos_y=pos_y, width=width, height=height)
        self.speed_x = 5
        self.traj_length = randint(100, 250)
        self.pos_x = randint(40 + self.traj_length, 640 - self.traj_length)

    def platform_move(self):
        """
        Метод класса, отвечающий за движение объектов класса.
        """
        self.rect[0] = self.rect[0] + self.speed_x
        if self.rect[0] < self.pos_x - self.traj_length and self.speed_x < 0 or \
           self.rect[0] > self.pos_x + self.traj_length and self.speed_x > 0:
            self.speed_x = -self.speed_x


class Star(pygame.sprite.Sprite):
    def __init__(self, screen, start_x, start_y):
        """
        Класс звёзд, способных к коллизии с моделькой игрока.
        При коллизии с моделькой игрока игрок получает постоянную вертикальную скорость на ограниченное время.
        :param screen: Surface - поверхность, на которую отрисовывается платформа.
        :param start_x: int - координата x экрана, на которой появляется моделька.
        :param start_y: int - координата y экрана, на которой появляется моделька.
        """
        super().__init__()
        self.screen = screen
        self.image = pygame.image.load("star.png")
        self.rect = self.image.get_rect()
        self.rect[0], self.rect[1] = start_x, start_y
        self.reflection = False

    def draw(self):
        """
        Метод отрисовки объектов класса.
        Рисует модельку объекта класса на поверхности self.screen.
        """
        self.screen.blit(self.image, self.rect)


if __name__ == "__main__":
    print("Этот файл не для прямого запуска!")
