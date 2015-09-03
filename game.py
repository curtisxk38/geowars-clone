import pygame
import control
import player
import colors
import wall
import camera
import agent

key_bindings_dict = {"LEFT": pygame.K_a,
                     "RIGHT": pygame.K_d,
                     "UP": pygame.K_w,
                     "DOWN": pygame.K_s,
                     "AUTOFIRE": False,
                     }

SCREEN_SIZE = []
TOTAL_LEVEL_SIZE = [720, 1080]

def load_key_bindings():
    pass

def simple_camera(camera_used, target_rect):
    x, y, _, _, = target_rect
    _, _, l, w = camera_used # length, width
    # center on target rect
    return pygame.Rect(-x+SCREEN_SIZE[0]/2, -y+SCREEN_SIZE[1]/2, l, w)

class GameState(control.State):
    def __init__(self):
        control.State.__init__(self)
        self.pressed_keys = None

        SCREEN_SIZE.extend(pygame.display.get_surface().get_size())
        self.now = 0
        self.mouse_list = []
        self.my_player = player.Player(50, 50)
        self.player_pressed_dict = self.make_player_dict()
        self.make_level()
        self.all_sprites = pygame.sprite.Group(self.my_player, wall.wall_list)

        self.my_camera = camera.Camera(simple_camera, *TOTAL_LEVEL_SIZE)
        self.spawner = agent.AgentSpawner((960, 480) , 80, 10)        

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
            self.my_player.key_pressed[self.player_pressed_dict[key]] = self.pressed_keys[key]
        if event.type == pygame.KEYDOWN:
            self.my_player.recently_pressed = self.player_pressed_dict.get(event.key)
        if event.type == pygame.MOUSEBUTTONDOWN:                	
            # get_pressed() returns a tuple with booleans
            # for (leftclick, mwheelclick, rightclick)
            if pygame.mouse.get_pressed()[0] == 1:
                self.my_player.shoot(self.mouse_list)
    
    def update_mouse_list(self):
        del self.mouse_list[:]
        self.mouse_list.extend(pygame.mouse.get_pos())
        self.mouse_list[0] -= self.my_camera.state.left
        self.mouse_list[1] -= self.my_camera.state.top
    
    def autofire(self):
        if key_bindings_dict["AUTOFIRE"] and self.now - self.my_player.autofire_last >= self.my_player.autofire_timer:
            self.my_player.shoot(self.mouse_list)
            self.my_player.autofire_last = self.now
    
    def update(self, screen):
        self.now = pygame.time.get_ticks()
        
        self.update_mouse_list()
        self.autofire()
    
        self.my_player.update()
        self.my_camera.update(self.my_player)
        self.spawner.update(self.now, self.my_player.pos)
        
        for bullet in self.my_player.bullet_list:
            bullet.update()
            if bullet.kill:
                self.my_player.bullet_list.remove(bullet)
        for x in agent.agent_list:
            x.update()
            if x.rect.collidelist(self.my_player.bullet_list) != -1:
                agent.agent_list.remove(x)

        # Draw
        screen.fill(colors.BLACK)
        for thing in self.all_sprites:
            screen.blit(thing.image, self.my_camera.apply(thing.rect))
        for bullet in self.my_player.bullet_list:
            screen.blit(bullet.image, self.my_camera.apply(bullet.rect))
        for x in agent.agent_list:
            screen.blit(x.image, self.my_camera.apply(x.rect))

    def make_player_dict(self):
        player_dict = {key_bindings_dict["LEFT"]: "LEFT",
                       key_bindings_dict["RIGHT"]: "RIGHT",
                       key_bindings_dict["UP"]: "UP",
                       key_bindings_dict["DOWN"]: "DOWN"}
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
