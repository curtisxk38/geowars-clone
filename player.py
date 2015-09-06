import pygame
import math
import colors
import os
import wall

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join("data", "player.bmp"))
        self.image.set_colorkey(colors.BLACK)
        self.image.convert()
        self.original_image = self.image
        self.rect = self.image.get_rect()
        
        self.autofire_timer = 1
        self.autofire_last = 0
	   
        self.max_velocity = 4
        self.pos = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(0, 0)
        self.last_velocity = pygame.math.Vector2(0, 0)

        self.rect.topleft = (self.pos.x, self.pos.y)

        self.key_pressed = {"LEFT": False, "RIGHT": False, "UP": False, "DOWN": False}
        self.left_pressed = self.right_pressed = self.up_pressed = self.down_pressed = False
        self.recently_pressed = None

        self.PROJECTILE_SPEED = 10
        self.bullet_list = []

    def update(self):
        self.set_velocity()
        self.update_direction()
        self.move()
        self.pos.x, self.pos.y = self.rect.center

    def set_velocity(self):
        # not so good way of handling presses and releases of inputs
        # left and right
        if self.key_pressed["LEFT"] and not self.key_pressed["RIGHT"]:
            self.velocity.x = -1 * self.max_velocity
        elif not self.key_pressed["LEFT"] and self.key_pressed["RIGHT"]:
            self.velocity.x = self.max_velocity
        elif self.key_pressed["LEFT"] and self.key_pressed["RIGHT"]:
            if self.recently_pressed == "LEFT":
                self.velocity.x = -1 * self.max_velocity
            elif self.recently_pressed == "RIGHT":
                self.velocity.x = self.max_velocity
        else:
            if self.velocity.x != 0 or self.velocity.y != 0:
                self.last_velocity.x = self.velocity.x
            self.velocity.x = 0
        #up and down
        if self.key_pressed["UP"] and not self.key_pressed["DOWN"]:
            self.velocity.y = -1 * self.max_velocity
        elif not self.key_pressed["UP"] and self.key_pressed["DOWN"]:
            self.velocity.y = self.max_velocity
        elif self.key_pressed["DOWN"] and self.key_pressed["UP"]:
            if self.recently_pressed == "UP":
                self.velocity.y = -1 * self.max_velocity
            elif self.recently_pressed == "DOWN":
                self.velocity.y = self.max_velocity
        else:
            if self.velocity.y != 0 or self.velocity.x != 0:
                self.last_velocity.y = self.velocity.y
            self.velocity.y = 0

    def update_direction(self):
        # dont actually like this, but it works....
        if self.velocity.x != 0 or self.velocity.y != 0:
            direction_angle = math.atan2(-self.velocity.y, self.velocity.x)
        else:
            direction_angle = math.atan2(-self.last_velocity.y, self.last_velocity.x)
        direction_angle = math.degrees(direction_angle) - 90
        self.rotate_center(direction_angle)

    def move(self):
        # update each axis one at a time
        if self.velocity.x != 0:
            self.move_on_direction(self.velocity.x, 0)
        if self.velocity.y != 0:
            self.move_on_direction(0, self.velocity.y)

    def move_on_direction(self, dx, dy):
        self.rect.move_ip(dx, dy)
        wall_collision = self.rect.collidelist(wall.wall_list)
        if wall_collision != -1: # if there is a collision:
            if dx > 0:
                # moving right, hit left side of wall
                self.rect.right = wall.wall_list[wall_collision].rect.left
            if dx < 0:
                # moving left, hit right side of wall
                self.rect.left = wall.wall_list[wall_collision].rect.right
            if dy > 0:
                # moving down, hit top of wall
                self.rect.bottom = wall.wall_list[wall_collision].rect.top
            if dy < 0:
                # moving up, hit bottom of wall
                self.rect.top = wall.wall_list[wall_collision].rect.bottom

    def rotate_center(self, angle):
        # rotate counterclockwise to angle
        original_rect = self.image.get_rect()
        rotated_image = pygame.transform.rotate(self.original_image, angle)
        rotated_rect = original_rect.copy()
        rotated_rect.center = rotated_image.get_rect().center
        rotated_image = rotated_image.subsurface(rotated_rect).copy()
        self.image = rotated_image

    def shoot(self, mouse):
        difference = pygame.math.Vector2(mouse[0] - self.rect.centerx, mouse[1] - self.rect.centery)
        difference.scale_to_length(self.PROJECTILE_SPEED)
        # No copy() method of pygame.math.Vector2 ??
        # Guess I'll do it like below
        copy_of_pos = pygame.math.Vector2(self.rect.centerx, self.rect.centery)
        self.bullet_list.append(Bullet(copy_of_pos, difference))


class Bullet(pygame.sprite.Sprite):
    def __init__(self, position, velocity):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join("data", "bullet.bmp"))
        self.image.set_colorkey(colors.BLACK)
        self.image.convert()
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.pos = position
        self.velocity = velocity
        self.rotate_center(self.find_angle())

        self.kill = False

    def update(self):
        self.pos+=self.velocity
        self.rect.center = self.pos.x, self.pos.y
        if self.rect.collidelist(wall.wall_list) != -1:
            self.kill = True

    def find_angle(self):
        angle = 180+math.degrees(math.atan2(self.velocity.x, self.velocity.y))
        return angle

    def rotate_center(self, angle):
        # rotate counterclockwise to angle
        rotated_image = pygame.transform.rotate(self.original_image, angle)
        self.image = rotated_image
        self.rect = self.image.get_rect()

