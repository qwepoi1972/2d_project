import pygame
from random import randint
from numpy import sign


FPS = 60
screen_width, screen_height = 800, 600
black = 0, 0, 0
white = 255, 255, 255
screen = pygame.display.set_mode([screen_width, screen_height])


class Player(pygame.sprite.Sprite):
    def __init__(self, screen, start_x, start_y):
        """
        Класс модельки, управляемой игроком.
        Способен передвигаться горизонтально и вертикально по нажатию соответствующих клавиш клавиатуры.
        :param screen: Surface - поверхность, на которую отрисовывается моделька.
        :param start_x: int - координата x экрана, на которой появляется моделька.
        :param start_y: int - координата y экрана, на которой появляется моделька.
        """

        super().__init__()
        self.screen = screen
        self.image = pygame.image.load("mario_stand_right.png")
        self.rect = self.image.get_rect()
        self.rect[0], self.rect[1] = start_x, start_y
        self.reflection = False
        self.speed_x = 0
        self.speed_y = 0
        self.speed_max = 10
        self.speed_jump = 15

    def draw(self):
        """
        Функция отрисовки.
        Рисует модельку объекта класса с учётом направления нажатых клавиш(влево или вправо) на поверхности self.screen.
        """
        self.screen.blit(pygame.transform.flip(self.image, self.reflection, False), self.rect)

    def check_collision(self, platforms):
        """
        Функция проверки коллизии.

        :param platforms: array, массив платформ, с которыми возможна коллизия.
        """
        self.rect[0] += round(self.speed_x)
        self.rect[1] -= round(self.speed_y)
        collide = pygame.sprite.spritecollideany(self, platforms)
        self.rect[0] -= round(self.speed_x)
        self.rect[1] += round(self.speed_y)
        for platform in platforms:
            if collide and abs(self.rect.bottom - platform.rect.top) <= 7:
                onground = True
                return onground, platform
        return False, None


class Platform(pygame.sprite.Sprite):
    def __init__(self, screen, pos_x, pos_y, width, height):
        """
        Класс платформ, способных к коллизии с моделькой игрока.
        Основа для разных типов платформ.
        :param screen: Surface - поверхность, на которую отрисовывается платформа.
        :param pos_x: int - координата x экрана, на которой появляется моделька.
        :param pos_y: int - координата y экрана, на которой появляется моделька.
        :param width: int - толщина в пикселях платформы.
        :param height: int - высота в пикселях платформы.
        """
        super().__init__()
        self.screen = screen
        self.image = pygame.image.load("platform.jpg")
        self.surf = pygame.transform.scale(self.image, (width, height))
        self.rect = pygame.Rect(pos_x, pos_y, width, height)

    def draw(self):
        """
        Функция отрисовки платформы.
        Рисует модельку объекта класса.
        """
        self.screen.blit(self.surf, self.rect)


def move(player, platforms):
    """
    Функция обновления и перемещения.
    Рассчитывает направление и скорость (горизонтальную и вертикальную),
    перемещает модельку на указанные координаты.
    При достижении моделькой середины экрана начинает двигать платформы
    вниз с той же по модулю скоростью, имитируя движение камеры вслед за игроком.
    :param player: объект класса игрок.
    :param platforms: array - массив платформ, с которыми возможна коллизия.
    """

    collide, platform = player.check_collision(platforms)
    keys = pygame.key.get_pressed()
    destination = max(keys[pygame.K_d], keys[pygame.K_RIGHT]) - max(
        keys[pygame.K_a], keys[pygame.K_LEFT])
    if destination != 0:
        player.reflection = not bool((destination + 1) / 2)
    if destination == 0:
        player.speed_x *= 0.7
    elif abs(player.speed_x) >= player.speed_max:
        player.speed_x = sign(player.speed_x) * player.speed_max
    else:
        player.speed_x += destination
    player.rect[0] += round(player.speed_x)

    if collide and abs(player.speed_y) >= 0:
        player.speed_y = 0
        player.rect[1] = platform.rect[1] - player.rect[3] + 1
    if not collide and player.speed_jump >= player.speed_y >= -6.5:
        player.speed_y -= 1
    if collide and (keys[pygame.K_UP] or keys[pygame.K_SPACE]):
        player.speed_y += player.speed_jump

    if player.rect[1] <= screen_height/2 and player.speed_y >= 0:
        for plat in platforms:
            plat.rect[1] += round(player.speed_y)

    elif (player.rect[1] <= screen_height/2 and player.speed_y < 0) or \
         (player.rect[1] > screen_height/2):
        player.rect[1] -= round(player.speed_y)


def spawn_start():
    platforms = []
    for i in range(7):
        platforms.append(Platform(screen=screen, pos_x=randint(50, 750),
                                  pos_y=-50 + 100 * i, width=120, height=20))
    return platforms


def changing_platforms(platforms):
    for i in range(len(platforms)):
        if platforms[i].rect[1] > screen_height:
            platforms[i] = Platform(screen=screen, pos_x=randint(50, 750),
                                    pos_y=-50, width=120, height=20)


def main():
    pygame.init()
    clock = pygame.time.Clock()
    finished = False
    platforms = spawn_start()
    player = Player(screen=screen, start_x=platforms[-1].rect[0],
                    start_y=platforms[-1].rect[1] - 53)
    while not finished:
        clock.tick(FPS)
        pygame.display.update()
        screen.fill(white)
        changing_platforms(platforms)
        move(player, platforms)
        for plat in platforms:
            plat.draw()
        player.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True


if __name__ == "__main__":
    main()
