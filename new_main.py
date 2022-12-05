import pygame
from random import randint
from math import copysign
FPS = 60
size = [800, 600]
black = 0, 0, 0
white = 255, 255, 255
screen = pygame.display.set_mode(size)


class Player(pygame.sprite.Sprite):
    def __init__(self, screen, start_x, start_y):
        super().__init__()
        self.image = pygame.image.load("mario_stand_right.png")
        self.rect = self.image.get_rect()
        self.rect[0], self.rect[1] = start_x, start_y
        self.reflection = False
        self.speed_x = 0
        self.speed_y = 0
        self.speed_max = 15
        self.speed_jump = 15

    def draw(self, screen):
        screen.blit(pygame.transform.flip(self.image, self.reflection, False), self.rect)


class Platform(pygame.sprite.Sprite):
    def __init__(self, screen, pos_x, pos_y, width, height):
        super().__init__()
        self.image = pygame.image.load("platform.jpg")
        self.surf = pygame.transform.scale(self.image, (width, height))
        self.rect = pygame.Rect(pos_x, pos_y, width, height)

    def draw(self, screen):
        screen.blit(self.surf, self.rect)


def move(player, platforms):
    onground = pygame.sprite.spritecollideany(player, platforms)
    keys = pygame.key.get_pressed()
    destination = max(keys[pygame.K_d], keys[pygame.K_RIGHT]) - max(
        keys[pygame.K_a], keys[pygame.K_LEFT])
    if destination != 0:
        player.reflection = not bool((destination + 1) / 2)
    if destination == 0:
        player.speed_x *= 0.7
    elif abs(player.speed_x) >= player.speed_max:
        player.speed_x = copysign(player.speed_max, player.speed_x)
    else:
        player.speed_x += destination

    if onground and abs(player.speed_y) > 0:
        player.speed_y = 0
    if not onground and player.speed_y <= 15:
        player.speed_y -= 1
    if onground and (keys[pygame.K_UP] or keys[pygame.K_SPACE]):
        player.speed_y += player.speed_jump

    if player.rect[1] <= 300 and player.speed_y >= 0:
        for plat in platforms:
            plat.rect[1] += round(player.speed_y)

    elif (player.rect[1] <= 300 and player.speed_y < 0) or \
         (player.rect[1] > 300):
        player.rect[1] -= round(player.speed_y)

    player.rect[0] += round(player.speed_x)


def spawn_start():
    platforms = []
    for i in range(7):
        platforms.append(Platform(screen=screen, pos_x=randint(50, 750),
                                  pos_y=-50 + 100 * i, width=120, height=20))
    return platforms


def changing_platforms(platforms):
    for i in range(len(platforms)):
        if platforms[i].rect[1] > 600:
            platforms[i] = Platform(screen=screen, pos_x=randint(50, 750),
                                    pos_y=-50, width=120, height=20)


def main():
    pygame.init()
    clock = pygame.time.Clock()
    finished = False
    platforms = spawn_start()
    player = Player(screen=screen, start_x=platforms[-1].rect[0],
                    start_y=platforms[-1].rect[1] - 50)
    while not finished:
        clock.tick(FPS)
        pygame.display.update()
        screen.fill(white)
        changing_platforms(platforms)
        move(player, platforms)
        player.draw(screen)
        for plat in platforms:
            plat.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True


if __name__ == "__main__":
    main()
