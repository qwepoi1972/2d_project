from new_main import *
import unittest


class Test(unittest.TestCase):
    def test_collision(self):
        '''
        Проверяет, падает ли персонаж при наложении его спрайта
        на спрайт прлатформы
        '''
        self.player = Player(pygame.sprite.Sprite, start_x=640, start_y=200)
        self.plats = [Platform(screen=screen, pos_y=200 + self.player.rect[3] - i,
                               width=20000, height=20)
                      for i in range(self.player.rect[3] + 20)]

        for platform in self.plats:
            move(self.player, [platform], stars=[], score=0)
            self.assertEqual(201, self.player.rect[1])
            self.player.rect[1] = 200
            self.player.speed_y = 0
