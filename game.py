import pygame
import control
import player
import colors
import wall

key_bindings_dict = {"LEFT": pygame.K_a,
                     "RIGHT": pygame.K_d,
                     "UP": pygame.K_w,
                     "DOWN": pygame.K_s}

def load_key_bindings():
    pass

class GameState(control.State):
    def __init__(self):
        control.State.__init__(self)
        self.pressed_keys = None

        self.my_player = player.Player(0, 0)
        self.player_pressed_dict = self.make_player_dict()
        self.make_level()
        self.all_sprites = pygame.sprite.Group(self.my_player, wall.wall_list)

    def startup(self):
        load_key_bindings()
        self.player_pressed_dict = self.make_player_dict()

    def cleanup(self):
        pass

    def get_event(self, event):
        self.pressed_keys = pygame.key.get_pressed()
        if self.pressed_keys[pygame.K_ESCAPE]:
            self.quit = True
        for key in self.player_pressed_dict:
            self.player_pressed_dict[key] = self.pressed_keys

    def update(self, screen):
        self.my_player.update()
        for bullet in self.my_player.bullet_list:
            bullet.update()
        # Draw
        screen.fill(colors.BLACK)
        for thing in self.all_sprites:
            screen.blit(thing.image, thing.rect)

    def make_player_dict(self):
        player_dict = {key_bindings_dict["LEFT"]: self.my_player.left_pressed,
                       key_bindings_dict["RIGHT"]: self.my_player.right_pressed,
                       key_bindings_dict["UP"]: self.my_player.up_pressed,
                       key_bindings_dict["DOWN"]: self.my_player.down_pressed}
        return player_dict

    def make_level(self):
        x = y = 0
        level = [
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
            "W                                                          W",
            "W                                                          W",
            "W                                                          W",
            "W                                                          W",
            "W                                                          W",
            "W                                                          W",
            "W                                                          W",
            "W                                                          W",
            "W                                                          W",
            "W                                                          W",
            "W                                                          W",
            "W                                                          W",
            "W                                                          W",
            "W                                                          W",
            "W                                                          W",
            "W                                                          W",
            "W                                                          W",
            "W                                                          W",
            "W                                                          W",
            "W                                                          W",
            "W                                                          W",
            "W                                                          W",
            "W                                                          W",
            "W                                                          W",
            "W                                                          W",
            "W                                                          W",
            "W                                                          W",
            "W                                                          W",
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
            ]
        for row in level:
            for col in row:
                if col == "W":
                    wall.Wall(x, y, 16, 16, colors.WHITE)
                x += 16
            y += 16
            x = 0