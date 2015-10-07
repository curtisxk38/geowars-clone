import pygame
import control
import button
import pickle
import colors

class ScoresState(control.State):
    def __init__(self):
        control.State.__init__(self)
        self.next = "menu"
        self.recent_score = None
        rect = pygame.Rect(0, 0, 80, 20)
        rect.centerx, rect.centery = pygame.display.get_surface().get_size()[0]/2, pygame.display.get_surface().get_size()[1]-60
        self.menu_button = button.Button(rect, "Menu", colors.WHITE, 15, self.finish)
        self.score_text = []

        self.score_board = None

    def receive_recent_score(self, score):
        self.recent_score = score

    def update_score_board(self):
        """Precondition: self.text is not None"""
        self.score_board.append(self.recent_score)
        # sort score_board, largest to smallest
        self.score_board.sort(reverse=True)
        if len(self.score_board) > 10:
            # if score_board has more than 10 entries, trim of the lower values to make it have 10 entries
            self.score_board = self.score_board[:10]

    def make_game_over_text(self):
        """Precondition: self.text is not None"""
        font = pygame.font.Font('freesansbold.ttf', 30)
        self.game_over_text = font.render("Game Over! Your score was %s!" % self.recent_score, True, colors.WHITE)
        self.game_over_text_rect = self.game_over_text.get_rect()
        self.game_over_text_rect.center = (pygame.display.get_surface().get_size()[0]/2, 50)

    def make_score_board_text(self):
        font = pygame.font.Font('freesansbold.ttf', 25)
        # Making the recent score underlined
        recent_index = -1
        if self.recent_score is not None and self.recent_score in self.score_board:
            recent_index = self.score_board.index(self.recent_score)

        for place, score in enumerate(self.score_board):
            if place == recent_index:
                font.set_underline(True)
            text_line = font.render("%s. %s" % (place+1,score), True, colors.WHITE)
            if font.get_underline():
                font.set_underline(False)
            text_line_rect = text_line.get_rect()
            text_line_rect.center = (pygame.display.get_surface().get_size()[0]/2, place*30 + 120)
            self.score_text.append((text_line, text_line_rect))

    def finish(self):
        self.done = True

    def startup(self):
        try:
            self.score_board = pickle.load(open("scoreboard.pkl", "rb"))
        except FileNotFoundError:
            self.score_board = []

        if self.recent_score is not None:
            self.update_score_board()
            self.make_game_over_text()

        self.make_score_board_text()

    def cleanup(self):
        pickle.dump(self.score_board, open("scoreboard.pkl", "wb"))
        self.recent_score = None
        self.score_text.clear()

    def get_event(self, event):
        self.menu_button.get_event(event)
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            self.done = True

    def update(self, screen):
        screen.fill(colors.BLACK)
        if self.recent_score is not None:
            screen.blit(self.game_over_text, self.game_over_text_rect)
        for text_tuple in self.score_text:
            screen.blit(*text_tuple)
        self.menu_button.update(screen)
