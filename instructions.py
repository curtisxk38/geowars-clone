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
        self.buttonlist = [self.make_menu_button()]
        self.key_bindings = None
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.text = []
        self.pressed_keys = None
        
        self.key_func = []
        self.waiting_for_key = False
        self.pressed_button_index = 1
        
        self.load_keybindings()
        self.make_key_func()

    def make_menu_button(self):
        rect = pygame.Rect(0, 0, 80, 20)
        rect.centerx, rect.centery = pygame.display.get_surface().get_size()[0]/2, pygame.display.get_surface().get_size()[1]-60
        my_button = button.Button(rect, "Menu", BLACK, 15, self.finish)
        return my_button

    def make_text(self):
        left = self.font.render("Move Left: ", True, BLACK)
        left_rect = left.get_rect()
        left_rect.topleft = (40, 200)
        self.text.append((left, left_rect))

        right = self.font.render("Move Right: ", True, BLACK)
        right_rect = right.get_rect()
        right_rect.topleft = (40, 240)
        self.text.append((right, right_rect))

        up = self.font.render("Move Up: ", True, BLACK)
        up_rect = up.get_rect()
        up_rect.topleft = (40, 280)
        self.text.append((up, up_rect))

        down = self.font.render("Move Down: ", True, BLACK)
        down_rect = down.get_rect()
        down_rect.topleft = (40, 320)
        self.text.append((down, down_rect))
    
    def make_key_func(self):
        d = {1: "LEFT", 2: "RIGHT", 3: "UP", 4: "DOWN"}
        def make(i):
            def a():
                if not self.waiting_for_key:
                    self.waiting_for_key = True
                    self.pressed_button_index = i
                    self.buttonlist[i].text = "___"
                    self.buttonlist[i].render_text()
                elif self.waiting_for_key and self.pressed_button_index == i:
                    self.waiting_for_key = False
                    self.buttonlist[i].text = pygame.key.name(self.key_bindings[d[i]])
                    self.buttonlist[i].render_text()
            return a
            
        for i in range(4):
            index = i + 1
            b = make(index)
            self.key_func.append(b)

    def bind_key(self, key):
        if self.pressed_button_index == 1:
            self.key_bindings["LEFT"] = key
            self.key_func[0]()
        elif self.pressed_button_index == 2:
            self.key_bindings["RIGHT"] = key
            self.key_func[1]()
        elif self.pressed_button_index == 3:
            self.key_bindings["UP"] = key
            self.key_func[2]()
        elif self.pressed_button_index == 4:
            self.key_bindings["DOWN"] = key
            self.key_func[3]()

    def make_key_buttons(self):
        left_rect = pygame.Rect(0, 0, 60, 20)
        left_rect.topleft = (180, 200)
        self.buttonlist.append(button.Button(left_rect, pygame.key.name(self.key_bindings["LEFT"]), BLACK, 15, self.key_func[0]))

        right_rect = pygame.Rect(0, 0, 60, 20)
        right_rect.topleft = (180, 240)
        self.buttonlist.append(button.Button(right_rect, pygame.key.name(self.key_bindings["RIGHT"]), BLACK, 15, self.key_func[1]))
        
        up_rect = pygame.Rect(0, 0, 60, 20)
        up_rect.topleft = (180, 280)
        self.buttonlist.append(button.Button(up_rect, pygame.key.name(self.key_bindings["UP"]), BLACK, 15, self.key_func[2]))
        
        down_rect = pygame.Rect(0, 0, 60, 20)
        down_rect.topleft = (180, 320)
        self.buttonlist.append(button.Button(down_rect, pygame.key.name(self.key_bindings["DOWN"]), BLACK, 15, self.key_func[3]))

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
        if len(self.buttonlist) < 4:
            self.make_key_buttons()

    def cleanup(self):
        pickle.dump(self.key_bindings, open("keybindings.pkl", "wb"))
        del self.buttonlist[1:]
        self.waiting_for_key = False

    def get_event(self, event):
        self.pressed_keys = pygame.key.get_pressed()
        for button in self.buttonlist:
            button.get_event(event)
        if self.pressed_keys[pygame.K_ESCAPE]:
            self.done = True
        if self.waiting_for_key and event.type == pygame.KEYDOWN:
            self.bind_key(event.key)

    def update(self, screen):
        screen.fill((255, 255, 255))
        for button in self.buttonlist:
            button.update(screen)
        for i in self.text:
            screen.blit(*i)
