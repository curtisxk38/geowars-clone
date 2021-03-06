import pygame
import math
import random
import os
import wall
import colors

agent_list = []



def get_truncate_vector(vector, limit):
    if vector.x > limit:
        vector.x = limit
    if vector.y > limit:
        vector.y = limit
    return vector

class AgentSpawner():
    def __init__(self, level_size, safe_radius):
        self.level_size = level_size
        self.radius = safe_radius
        # Score to start spawning at, tick last spawned, tick duration before spawning again, Agent type
        self.spawn_list = [
                           [0, 0, 800, WanderAgent],
                           [15, 0, 1000, SeekAgent],
                           [50, 0, 1200, FleeAgent],
                          ]

    def agent_limit(self, score):
        agent_limit = 20
        if(score > 100):
            agent_limit += (score - 100) / 20
        return agent_limit

    def update(self, now, player_pos, score):
        if len(agent_list) < self.agent_limit(score):
            for entry in self.spawn_list:
                if entry[0] <= score and now - entry[1] > entry[2]:
                    self.spawn(entry[3], player_pos)
                    entry[1] = now
    
    def get_random_xy(self):
        return random.randint(30, self.level_size[0] - 30), random.randint(30, self.level_size[1] - 30)
    
    def spawn(self, agent, player_pos):
        safe = False
        while not safe:
            point = pygame.math.Vector2(self.get_random_xy())
            diff = player_pos - point
            safe = diff.length_squared() >= self.radius**2
        agent(point.x, point.y)


class Agent:
    def __init__(self, x, y):
        agent_list.append(self)

        self.pos = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(0, 0)

        self.mass = 20
        self.max_velocity = 2.5
        self.max_force = 10
        self.max_speed = 2.5

        # Wander
        self.w_angle = random.uniform(0, 2 * math.pi)
        self.w_circle_distance = .6
        self.w_circle_radius = .5
        self.w_angle_variance = math.pi / 6
    
    def move(self):
        # update each axis one at a time
        x = y = False
        if self.velocity.x != 0:
            x = self.move_on_direction(self.velocity.x, 0)
        if self.velocity.y != 0:
            y = self.move_on_direction(0, self.velocity.y)
        return x or y

    def move_on_direction(self, dx, dy):
        self.rect.move_ip(dx, dy)
        wall_collision = self.rect.collidelist(wall.wall_list)
        if wall_collision != -1:
        # if there is a collision:
            if dx > 0:
                # moving right, hit left side of wall
                self.rect.right = wall.wall_list[wall_collision].rect.left
                self.velocity.x *= -1
            if dx < 0:
                # moving left, hit right side of wall
                self.rect.left = wall.wall_list[wall_collision].rect.right
                self.velocity.x *= -1
            if dy > 0:
                # moving down, hit top of wall
                self.rect.bottom = wall.wall_list[wall_collision].rect.top
                self.velocity.y *= -1
            if dy < 0:
                # moving up, hit bottom of wall
                self.rect.top = wall.wall_list[wall_collision].rect.bottom
                self.velocity.y *= -1
            return True
        return False

    def seek(self, target):
        # target is a vector
        desired_velocity = target - self.pos
        try:
            desired_velocity.scale_to_length(self.max_velocity)
            desired_velocity -= self.velocity
        except ValueError:
            pass
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
        #self.image = pygame.image.load(os.path.join("data", "wander.bmp"))
        surface = pygame.Surface((16,16))
        surface.fill(colors.RED)
        self.image = surface
        self.image.convert()
        self.rect = self.image.get_rect()#pygame.Rect(0, 0, 16, 16)
        self.rect.center = (x, y)

        self.max_velocity = 1.5

    def update(self, player):
        steering = self.wander()
        steering = get_truncate_vector(steering, self.max_force)
        steering /= self.mass
        self.velocity += steering
        self.velocity = get_truncate_vector(self.velocity, self.max_speed)

        if self.move():
            self.w_angle += (math.pi / 2)
            if self.w_angle > 2* math.pi:
                self.w_angle -= 2* math.pi
        self.pos.x, self.pos.y = self.rect.center

class SeekAgent(Agent):
    def __init__(self, x , y):
        Agent.__init__(self, x, y)

        surface = pygame.Surface((16,16))
        surface.fill(colors.GREEN)
        self.image = surface
        self.image.convert()
        self.rect = self.image.get_rect()#pygame.Rect(0, 0, 16, 16)
        self.rect.center = (x, y)

        self.max_velocity = 4
        self.max_force = 8.0

    def update(self, player):
        steering = self.seek(player.pos)
        steering = get_truncate_vector(steering, self.max_force)
        steering /= self.mass
        self.velocity += steering
        self.velocity = get_truncate_vector(self.velocity, self.max_speed)

        self.move()
        self.pos.x, self.pos.y = self.rect.center

class FleeAgent(Agent):
    def __init__(self, x, y):
        Agent.__init__(self, x, y)
        
        surface = pygame.Surface((16,16))
        surface.fill(colors.BLUE)
        self.image = surface
        self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        self.flee_radius = 80
        
        self.max_velocity = 10
        self.max_speed = 10
        
    def update(self, player):
        steering = self.flee_vector(player.bullet_list) + self.wander()
        steering = get_truncate_vector(steering, self.max_force)
        steering /= self.mass
        self.velocity += steering
        self.velocity = get_truncate_vector(self.velocity, self.max_speed)
        
        if self.move():
            self.w_angle += (math.pi / 2)
            if self.w_angle > 2* math.pi:
                self.w_angle -= 2* math.pi
        self.pos.x, self.pos.y = self.rect.center
    
    def flee_vector(self, b_list):
        if len(b_list) == 0:
            return pygame.math.Vector2(0, 0)
        index, min_dist = self.find_nearest_bullet(b_list)
        if min_dist < self.flee_radius**2:
            return self.flee(b_list[index].pos)
        return pygame.math.Vector2(0, 0)
        
    def find_nearest_bullet(self, b_list):
        dist = [(self.pos - b.pos).length_squared() for b in b_list]
        min_dist = min(dist)
        index = dist.index(min_dist)
        return index, min_dist
        
    
