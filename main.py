import pygame
import colors
import player
import wall
import camera
import os
import vector

pygame.init()
#pygame.font.init()
#pygame.mixer.init()

CLOCK = pygame.time.Clock()

def print_text(text, color, size):
    font1 = pygame.font.Font("Comic_Book.ttf", size)
    printed_text = font1.render(text, 1, color)
    return printed_text

def simple_camera(camera_used, target_rect):
    x, y, _, _, = target_rect
    _, _, l, w = camera_used #length, width
    #center on player
    return pygame.Rect(-x+WINDOW_SIZE[0]/2, -y+WINDOW_SIZE[1]/2, l, w)

lines_list = []
class BackgroundLine(pygame.sprite.Sprite):
    def __init__(self, p1, p2, width, color):
        pygame.sprite.Sprite.__init__(self)
        if p1.x == p2.x:
            x = p1.x + width
            y = abs(p1.y - p2.y)
        else:
            x = abs(p1.x - p2.x)
            y = p1.y + width
        self.image = pygame.Surface((x,y))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (p1.x, p1.y)
        lines_list.append(self)

    def update(self):
        pass


def generate_background_lines(x, y, interval):
    counter = 0
    while counter<x:
        point1 = vector.Vector(counter, 0)
        point2 = vector.Vector(counter, y)
        BackgroundLine(point1, point2, 2, colors.PURPLEY_BLACK)
        counter += interval
    counter = 0
    while counter<y:
        point1 = vector.Vector(0, counter)
        point2 = vector.Vector(x, counter)
        BackgroundLine(point1, point2, 2, colors.PURPLEY_BLACK)
        counter+= interval


WINDOW_SIZE = (720, 480)
main_screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Geowars Clone")

def main():
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

    TOTAL_LEVEL_SIZE = (720, 1080)

    #generate_background_lines(TOTAL_LEVEL_SIZE[0], TOTAL_LEVEL_SIZE[1], 32)

    camera_obj = camera.Camera(simple_camera, TOTAL_LEVEL_SIZE[0], TOTAL_LEVEL_SIZE[1])
    player_obj = player.Player(WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2)

    all_sprites = pygame.sprite.Group(player_obj, wall.wall_list, lines_list)

    game_running = True
    while game_running:
        #Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            #key pressed down
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_running= False
                if event.key == pygame.K_a:
                    player_obj.left_pressed = True
                if event.key == pygame.K_d:
                    player_obj.right_pressed = True
                if event.key == pygame.K_w:
                    player_obj.up_pressed = True
                if event.key == pygame.K_s:
                    player_obj.down_pressed = True
                if event.key == pygame.K_SPACE:
                    print(player_obj.bullet_list)
                player_obj.recently_pressed = event.key
            #key released
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    player_obj.left_pressed = False
                if event.key == pygame.K_d:
                     player_obj.right_pressed = False
                if event.key == pygame.K_w:
                    player_obj.up_pressed = False
                if event.key == pygame.K_s:
                    player_obj.down_pressed = False
            #any mouse button down
            if event.type == pygame.MOUSEBUTTONDOWN:
                #get_pressed() returns a tuple with booleans
                #for (leftclick, mwheelclick, rightclick)
                if pygame.mouse.get_pressed()[0] == 1:
                    player_obj.shoot(pygame.mouse.get_pos())

        #Logic
        camera_obj.update(player_obj)

        player_obj.update()
        #all_sprites.add(player_obj.bullet_list)
        for bullet in player_obj.bullet_list:
            bullet.update()

        x = player_obj.last_velocity
        text_to_print = {'test': (print_text(str(x), colors.BLACK, 25), (100,100))}
        #Draw
        main_screen.fill(colors.BLACK)
        #main_screen.blit(pygame.image.load(os.path.join("data", "background.bmp")), pygame.Rect(0, 0, 720, 480))
        for entry in text_to_print:
            text_ready, text_pos = text_to_print[entry]
            main_screen.blit(text_ready, text_pos)
        for entry in all_sprites:
            main_screen.blit(entry.image, camera_obj.apply(entry))
        for entry in player_obj.bullet_list:
            main_screen.blit(entry.image, camera_obj.apply(entry))
        pygame.display.flip()
        CLOCK.tick(60)

if __name__ == "__main__":
    main()