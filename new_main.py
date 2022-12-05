import pygame
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
        self.speed_max = 10
        self.speed_jump = 10

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


def main():
    pygame.init()
    clock = pygame.time.Clock()
    finished = False
    player = Player(screen, 700, 500)
    platform1 = Platform(screen, 650, 550, 120, 20)
    platform2 = Platform(screen, 600, 500, 120, 20)
    platform3 = Platform(screen, 550, 450, 120, 20)
    platform4 = Platform(screen, 500, 400, 120, 20)
    platform5 = Platform(screen, 450, 350, 120, 20)
    platform6 = Platform(screen, 400, 300, 120, 20)
    platform7 = Platform(screen, 350, 250, 120, 20)
    platforms = [platform1, platform2, platform3, platform4, platform5, platform6, platform7]
    while not finished:
        clock.tick(FPS)
        pygame.display.update()
        screen.fill(white)
        move(player, platforms)
        player.draw(screen)
        for plat in platforms:
            plat.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True


if __name__ == "__main__":
    main()
