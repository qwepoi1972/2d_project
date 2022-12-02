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

    def move(self, platforms):
        onground = pygame.sprite.spritecollideany(self, platforms)
        keys = pygame.key.get_pressed()
        destination = max(keys[pygame.K_d], keys[pygame.K_RIGHT]) - max(keys[pygame.K_a], keys[pygame.K_LEFT])
        if destination != 0:
            self.reflection = not bool((destination+1)/2)
        if destination == 0:
            self.speed_x *= 0.7
        elif abs(self.speed_x) >= self.speed_max:
            self.speed_x = copysign(self.speed_max, self.speed_x)
        else:
            self.speed_x += destination

        if onground and abs(self.speed_y) > 0:
            self.speed_y = 0
        if not onground and self.speed_y <= 15:
            self.speed_y -= 1
        if onground and (keys[pygame.K_UP] or keys[pygame.K_SPACE]):
            self.speed_y += self.speed_jump

        self.rect[0] += round(self.speed_x)
        self.rect[1] -= round(self.speed_y)


class Platform(pygame.sprite.Sprite):
    def __init__(self, screen, pos_x, pos_y, width, height):
        super().__init__()
        self.image = pygame.image.load("platform.jpg")
        self.surf = pygame.transform.scale(self.image, (width, height))
        self.rect = pygame.Rect(pos_x, pos_y, width, height)

    def draw(self, screen):
        screen.blit(self.surf, self.rect)


def main():
    pygame.init()
    clock = pygame.time.Clock()
    finished = False
    player = Player(screen, 700, 500)
    platform = Platform(screen, 650, 550, 120, 20)
    platforms = [platform]
    while not finished:
        clock.tick(FPS)
        pygame.display.update()
        screen.fill(white)
        player.move(platforms)
        player.draw(screen)
        platform.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True


if __name__ == "__main__":
    main()
