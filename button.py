import pygame


class Button():
    def __init__(self, rect, text, color, size, function):
        self.rect = pygame.Rect(rect)
        self.hovered = False
        self.text = text
        self.color = color
        self.function = function
        self.font = pygame.font.Font('freesansbold.ttf', size)
        self.render_text()

    def render_text(self):
        if self.text is not None:
            self.text = self.font.render(self.text, True, self.color)
            self.text_rect = self.text.get_rect()
            self.text_rect.center = self.rect.center

    def check_hover(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if not self.hovered:
                # start hover
                self.hovered = True
                self.rect.inflate_ip(5, 5)
        else:
            if self.hovered:
                # end hover
                self.rect.inflate_ip(-5, -5)
            self.hovered = False

    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos):
            if self.function is not None:
                self.function()

    def update(self, surface):
        self.check_hover()
        pygame.draw.rect(surface, self.color, self.rect, 1)
        surface.blit(self.text, self.text_rect)
