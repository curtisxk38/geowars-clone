import pygame
import control
import button
import pickle

BLACK = (0,0,0)
ORANGE = (255, 102, 0)
TRANSPARENT = (0, 0, 0, 0)


class InstructionsState(control.State):
    def __init__(self):
        control.State.__init__(self)
        self.next = "menu"
        self.key_buttons = []
        self.menu_button = self.make_menu_button()
        self.key_bindings = None
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.text = []
        self.pressed_keys = None
        
        self.key_func = []
        self.waiting_for_key = False
        self.pressed_button_index = 1
        
        self.load_keybindings()
        self.make_key_func()
        
        self.key_list = ["LEFT","RIGHT","UP","DOWN"]

    def make_menu_button(self):
        rect = pygame.Rect(0, 0, 80, 20)
        rect.centerx, rect.centery = pygame.display.get_surface().get_size()[0]/2, pygame.display.get_surface().get_size()[1]-60
        my_button = button.Button(rect, "Menu", BLACK, 15, self.finish)
        return my_button

    def make_text(self):
        for i in range(4):
            text = self.font.render("Move " + self.key_list[i] + ": ", True, BLACK)
            rect = text.get_rect()
            rect.topleft = (40, 200 + i * 40)
            self.text.append((text, rect))
    
    def make_key_func(self):
        def make(i):
            def a():
                if not self.waiting_for_key:
                    self.waiting_for_key = True
                    self.pressed_button_index = i
                    self.key_buttons[i].text = "___"
                    self.key_buttons[i].render_text()
                elif self.waiting_for_key and self.pressed_button_index == i:
                    self.waiting_for_key = False
                    self.key_buttons[i].text = pygame.key.name(self.key_bindings[self.key_list[i]])
                    self.key_buttons[i].render_text()
            return a
            
        for i in range(4):
            index = i
            b = make(index)
            self.key_func.append(b)

    def bind_key(self, key):
        for i in range(4):
            if self.pressed_button_index == i:
                self.key_bindings[self.key_list[i]] = key
                self.key_func[i]()

    def make_key_buttons(self):
        for i in range(4):
            rect = pygame.Rect(180, 200 + i * 40, 60, 20)
            self.key_buttons.append(button.Button(rect, pygame.key.name(self.key_bindings[self.key_list[i]]), BLACK, 15, self.key_func[i]))

    def load_keybindings(self):
        try:
            self.key_bindings = pickle.load(open("keybindings.pkl", "rb"))
        except FileNotFoundError:
            self.key_bindings = {"LEFT": pygame.K_a,
                                 "RIGHT": pygame.K_d,
                                 "UP": pygame.K_w,
                                 "DOWN": pygame.K_s,
                                 "AUTOFIRE": True,
                                 }

    def finish(self):
        self.done = True

    def startup(self):
        self.load_keybindings()
        if not self.text:
            self.make_text()
        if len(self.key_buttons) == 0:
            self.make_key_buttons()

    def cleanup(self):
        pickle.dump(self.key_bindings, open("keybindings.pkl", "wb"))
        self.key_buttons.clear()
        self.waiting_for_key = False

    def get_event(self, event):
        self.pressed_keys = pygame.key.get_pressed()
        for button in self.key_buttons:
            button.get_event(event)
        self.menu_button.get_event(event)
        if self.pressed_keys[pygame.K_ESCAPE]:
            self.done = True
        if self.waiting_for_key and event.type == pygame.KEYDOWN:
            self.bind_key(event.key)

    def update(self, screen):
        screen.fill((255, 255, 255))
        for button in self.key_buttons:
            button.update(screen)
        self.menu_button.update(screen)
        for i in self.text:
            screen.blit(*i)
