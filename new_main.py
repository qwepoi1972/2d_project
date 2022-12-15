import pygame
from numpy import sign
from random import randint, choice
from math import copysign

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
        self.speed_jump = 20

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
    def __init__(self, screen, pos_y, width, height):
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
        self.pos_x = randint(40, 640)
        self.image = pygame.image.load("platform.jpg")
        self.surf = pygame.transform.scale(self.image, (width, height))
        self.rect = pygame.Rect(self.pos_x, pos_y, width, height)

    def draw(self):
        """
        Функция отрисовки платформы.
        Рисует модельку объекта класса.
        """
        self.screen.blit(self.surf, self.rect)


class HorizontalMovingPlatform(Platform):
    def __init__(self, screen, pos_y, width, height):
        super().__init__(screen=screen, pos_y=pos_y, width=width, height=height)
        self.speed_x = 5
        self.traj_length = randint(100, 250)
        self.pos_x = randint(40 + self.traj_length, 640 - self.traj_length)

    def platform_move(self):
        self.rect[0] = self.rect[0] + self.speed_x
        if self.rect[0] < self.pos_x - self.traj_length and self.speed_x < 0 or \
           self.rect[0] > self.pos_x + self.traj_length and self.speed_x > 0:
            self.speed_x = -self.speed_x


def move(player, platforms, score):
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

    for plat in platforms:
        if plat.__class__ == HorizontalMovingPlatform:
            plat.platform_move()

    if collide:
        player.speed_y = 0
        player.rect[1] = platform.rect[1] - player.rect[3] + 1
    if not collide and player.speed_jump >= player.speed_y >= -13:
        player.speed_y -= 1
    if collide and (keys[pygame.K_UP] or keys[pygame.K_SPACE]):
        player.speed_y += player.speed_jump

    if player.rect[1] <= screen_height/2 and player.speed_y >= 0:
        for plat in platforms:
            plat.rect[1] += round(player.speed_y)

    elif (player.rect[1] <= screen_height/2 and player.speed_y < 0) or \
         (player.rect[1] > screen_height/2):
        player.rect[1] -= round(player.speed_y)

    player.rect[0] += round(player.speed_x)
    if player.rect[0] + player.rect.width / 2 > 800:
        player.rect[0] -= 800
    if player.rect[0] + player.rect.width / 2 < 0:
        player.rect[0] += 800

    if player.speed_y > 0:
        return score + player.speed_y
    else:
        return score


def spawn_start():
    platforms = []
    for i in range(7):
        platforms.append(Platform(screen=screen, pos_y=-50 + 100 * i,
                                  width=120, height=20))
    return platforms


def generating_platforms(platforms, score, score_):
    if score - score_ >= 50:
        max_height = 0
        for plat in platforms:
            if plat.rect[1] < max_height:
                max_height = plat.rect[1]
        chance = randint(1, 8)
        if chance > 5:
            platforms.append(HorizontalMovingPlatform(screen=screen,
                                                      pos_y=max_height-100,
                                                      width=120,
                                                      height=20))
        else:
            platforms.append(Platform(screen=screen,
                                      pos_y=max_height-100,
                                      width=120, height=20))
        return score
    else:
        return score_


def deleting_platforms(platforms):
    for plat in platforms:
        if plat.rect[1] > 600:
            platforms.remove(plat)


def game_over(player):
    if player.rect[1] > 600:
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
    platforms = spawn_start()
    player = Player(screen=screen, start_x=platforms[-1].rect[0],
                    start_y=platforms[-1].rect[1] - 53)
    while not finished:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            if event.type == pygame.KEYDOWN:
                game_over_status = False
        screen.fill(white)
        if not game_over_status:
            game_over_status = game_over(player=player)
            score_ = generating_platforms(platforms, score=score, score_=score_)
            deleting_platforms(platforms)
            score = move(player=player, platforms=platforms, score=score)
            player.draw()
            for plat in platforms:
                plat.draw()
        if game_over_status:
            platforms = spawn_start()
            player.rect[0] = platforms[-1].rect[0]
            player.rect[1] = platforms[-1].rect[1] - 50
            screen.blit(default_font.render("Game Over" , True, black),
                        (300, 200))
            screen.blit(default_font.render("Your score is: " + str(round(score/100)), True, black),
                        (250, 300))
            screen.blit(default_font.render("Press any button to restart", True, black),
                        (180, 400))
        pygame.display.update()


if __name__ == "__main__":
    main()
