import pygame
import math
import random

agent_list = []

def get_truncate_vector(vector, limit):
    if vector.x > limit:
        vector.x = limit
    if vector.y > limit:
        vector.y = limit
    return vector


class Agent:
    def __init__(self, x, y):
        self.pos = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(0, 0)

        self.mass = 20
        self.max_velocity = 5
        self.max_force = 10
        self.max_speed = 10

        # Wander
        self.w_angle = random.uniform(0, 2 * math.pi)
        self.w_circle_distance = .6
        self.w_circle_radius = .5
        self.w_angle_variance = math.pi / 6

    def agent_update(self, steering):
        steering = get_truncate_vector(steering, self.max_force)
        steering /= self.mass
        self.velocity += steering
        self.velocity = get_truncate_vector(self.velocity, self.max_speed)
        self.pos += self.velocity

    def seek(self, target):
        # target is a vector
        desired_velocity = target - self.pos
        desired_velocity.scale_to_length(self.max_velocity)
        desired_velocity -= self.velocity
        return desired_velocity

    def flee(self, target):
        # target is a vector
        desired_velocity = target - self.pos
        desired_velocity.scale_to_length(self.max_velocity)
        desired_velocity *= -1
        desired_velocity -= self.velocity
        return desired_velocity

    def pursuit(self, target_agent):
        # target_agent is an agent
        distance = target_agent.pos - self.pos
        prediction_const = distance.length() / target_agent.max_velocity
        future_pos = target_agent.pos + (target_agent.velocity * prediction_const)
        return self.seek(future_pos)

    def evade(self, target_agent):
        # target_agent is an agent
        distance = target_agent.pos - self.pos
        prediction_const = distance.length() / target_agent.max_velocity
        future_pos = target_agent.pos + (target_agent.velocity * prediction_const)
        return self.flee(future_pos)

    def wander(self):
        circle_center = pygame.math.Vector2(self.velocity.x, self.velocity.y)
        try:
            circle_center.scale_to_length(self.w_circle_distance)
        except ValueError:
            # Cannot scale a vector with zero length
            pass
        # calculate displacement force
        displacement = pygame.math.Vector2(1, 0)
        displacement *= self.w_circle_radius
        # change by small angle
        displacement.rotate_ip(math.degrees(self.w_angle))
        # change w_angle by small random amount
        self.w_angle += random.uniform(-1 * self.w_angle_variance, self.w_angle_variance)
        # finally, find steering force
        circle_center += displacement
        return circle_center

class WanderAgent(Agent):
    def __init__(self, x , y):
        Agent.__init__(self, x, y)
        self.rect = pygame.Rect(0, 0, 16, 16)
        self.rect.center = (x, y)

        agent_list.append(self)

    def update(self):
        self.agent_update(self.wander())
        self.rect.centerx = self.pos.x
        self.rect.centery = self.pos.y
