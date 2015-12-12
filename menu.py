import pygame
import control
import button
import colors


class MenuState(control.State):
    def __init__(self):
        control.State.__init__(self)
        self.next = "game"
        self.button_list = []

        self.background_color = colors.BLACK
        self.button_color = colors.WHITE

    def go_to_game(self):
        self.next = "game"
        self.done = True

    def go_to_instructions(self):
        self.next = "instructions"
        self.done = True

    def go_to_scores(self):
        self.next = "scores"
        self.done = True

    def quit_game(self):
        self.quit = True

    def make_buttons(self):
        rect = pygame.Rect(0, 0, 100, 20)
        rect.centerx = pygame.display.get_surface().get_size()[0]/2
        rect.centery = pygame.display.get_surface().get_size()[1]/2
        self.button_list.append(button.Button(rect, "Start", self.button_color, 15, self.go_to_game))
        rect.centery += 30
        self.button_list.append(button.Button(rect, "Instructions", self.button_color, 15, self.go_to_instructions))
        rect.centery += 30
        self.button_list.append(button.Button(rect, "Scores", self.button_color, 15, self.go_to_scores))
        rect.centery += 30
        self.button_list.append(button.Button(rect, "Quit", self.button_color, 15, self.quit_game))

    def startup(self):
        # if its empty
        if not self.button_list:
            self.make_buttons()

    def cleanup(self):
        pass

    def get_event(self, event):
        for b in self.button_list:
            b.get_event(event)
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            self.quit = True

    def update(self, screen):
        screen.fill(self.background_color)
        for b in self.button_list:
            b.update(screen)
