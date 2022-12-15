import pygame
from numpy import sign
from random import randint

FPS = 60
screen_width, screen_height = 800, 600
black = 0, 0, 0
white = 255, 255, 255
screen = pygame.display.set_mode([screen_width, screen_height])
background = pygame.transform.scale(pygame.image.load("background.jpg"), [screen_width, screen_height])


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


def move(player, platforms, stars, score):
    """
    Функция обновления и перемещения.
    Рассчитывает направление и скорость (горизонтальную и вертикальную),
    перемещает модельку на указанные координаты.
    При достижении моделькой середины экрана начинает двигать платформы
    вниз с той же по модулю скоростью, имитируя движение камеры вслед за игроком.
    :param player: объект класса игрок.
    :param platforms: array - массив платформ, с которыми возможна коллизия.
    :param stars: array - массив звёзд, с которыми возможна коллизия.
    :param score: int - значение счёта.
    """

    collide, platform = player.check_collision_platforms(platforms)
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

    for plat in platforms:
        if plat.__class__ == HorizontalMovingPlatform:
            plat.platform_move()

    if not player.star_check and collide:
        player.speed_y = 0
        player.rect[1] = platform.rect[1] - player.rect[3] + 5
    if not player.star_check and not collide \
            and player.speed_jump >= player.speed_y >= -13:
        player.speed_y -= 1
    else:
        player.speed_y = min(player.speed_y + 1, player.speed_jump)
        if player.speed_y < player.speed_jump:
            player.speed_y += 1
    if not player.star_check and collide \
            and (keys[pygame.K_UP] or keys[pygame.K_SPACE]):
        player.speed_y = player.speed_jump

    if player.rect[1] <= screen_height/2 and player.speed_y >= 0:
        for plat in platforms:
            plat.rect[1] += round(player.speed_y)
        for star in stars:
            star.rect[1] += round(player.speed_y)
        score += round(player.speed_y)

    elif (player.rect[1] <= screen_height/2 and player.speed_y < 0) or \
         (player.rect[1] > screen_height/2):
        player.rect[1] -= round(player.speed_y)

    player.rect[0] += round(player.speed_x)
    if player.rect[0] + player.rect.width / 2 > 800:
        player.rect[0] -= 800
    if player.rect[0] + player.rect.width / 2 < 0:
        player.rect[0] += 800

    return score


def spawn_start():
    """
    Функция создания платформ для начального экрана.
    :return: platforms - array, массив платформ.
    """
    platforms = [Platform(screen=screen, pos_y=-50 + 100 * i, width=120, height=20) for i in range(7)]
    return platforms


def generating_platforms(platforms, stars, score, score_):
    """
    Функция создания платформ в ходе игры.
    :param platforms: array - массив платформ, с которыми возможна коллизия.
    :param stars: array - массив звёзд, с которыми возможна коллизия.
    :param score: int - значение счёта.
    :param score_: int - координата y самой высокой платформы.
    :return: int - Значение score_.
    """
    if score - score_ >= 50:
        max_height = min(platform.rect[1] for platform in platforms)
        if randint(1, 8) > 6:
            platforms.append(HorizontalMovingPlatform(screen=screen,
                                                      pos_y=max_height-100,
                                                      width=120,
                                                      height=20))
        else:
            platforms.append(Platform(screen=screen,
                                      pos_y=max_height-100,
                                      width=120, height=20))
            stars.append(Star(screen=screen, start_x=platforms[-1].pos_x,
                              start_y=max_height-120))
        return score
    else:
        return score_


def deleting_objects(platforms, stars):
    """
    Функция удаления платформ, находящихся ниже нижней границы экрана.
    :param platforms: array - массив платформ, с которыми возможна коллизия.
    :param stars: array - массив звёзд, с которыми возможна коллизия.
    """
    for plat in platforms:
        if plat.rect[1] > screen_height:
            platforms.remove(plat)
    for star in stars:
        if star.rect[1] > screen_height:
            stars.remove(star)


def game_over(player):
    """
    Функция проверки смерти игрока(моделька игрока ниже нижней границы экрана).
    :param player: Player - объект класса, управляемый игроком.
    :return: bool - значение флага game_over_status.
    """
    if player.rect[1] > screen_height:
        return True
    else:
        return False


def main():
    pygame.init()
    default_font = pygame.font.SysFont('Verdana', 36)
    clock = pygame.time.Clock()
    finished = False
    game_over_status = False
    score = 0
    score_ = 0
    stars = []
    platforms = spawn_start()
    player = Player(screen=screen, start_x=platforms[-1].rect[0],
                    start_y=platforms[-1].rect[1] - 75)
    while not finished:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif game_over_status and event.type == pygame.KEYDOWN:
                game_over_status = False
                score = 0
                score_ = 0
            elif event.type == pygame.USEREVENT+1:
                player.star_check = False

        if not player.star_check:
            player.star_check = player.check_collision_stars(stars)

        screen.blit(background, background.get_rect())
        if not game_over_status:
            game_over_status = game_over(player=player)
            screen.blit(
                default_font.render(str(round(score / 100)), True, black),
                (10, 10))
            score_ = generating_platforms(platforms, stars, score=score, score_=score_)
            deleting_objects(platforms, stars)
            score = move(player=player, platforms=platforms,
                         score=score, stars=stars)
            player.draw(platforms)
            for plat in platforms:
                plat.draw()
            for star in stars:
                star.draw()
        if game_over_status:
            platforms = spawn_start()
            stars = []
            player.rect[0] = platforms[-1].rect[0]
            player.rect[1] = platforms[-1].rect[1] - 75
            screen.blit(default_font.render("Game Over", True, black),
                        (300, 200))
            screen.blit(default_font.render("Your score is: " + str(round(score/100)), True, black),
                        (250, 300))
            screen.blit(default_font.render("Press any button to restart", True, black),
                        (180, 400))
        pygame.display.update()


if __name__ == "__main__":
    main()
