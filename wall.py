import pygame
import os

wall_list = []

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, l, w, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((l,w))
        self.image.fill(color)
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, l, w)
        wall_list.append(self)
        # self.image = pygame.image.load(os.path.join("data", "brick.bmp"))

    def update(self):
        # update sprite, wall doesn't change so...
        pass

    def __repr__(self):
        return "<Wall at %s, %s>" % (self.x, self.y)
