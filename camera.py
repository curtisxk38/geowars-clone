import pygame

class Camera():
    def __init__(self, camera_function, width, height):
        self.camera_function = camera_function
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_function(self.state, target.rect)