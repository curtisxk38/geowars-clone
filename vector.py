import math

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "<Vector: (%s, %s)>" % (self.x, self.y)

    def get_mag_sqr(self):
        return self.x**2 + self.y**2

    def get_mag(self):
        return math.hypot(self.x, self.y)

    def normalize(self):
        self.divide_by_scalar(self.get_mag())

    def add_vector(self, vector2):
        self.x += vector2.x
        self.y += vector2.y

    def subtract_vector(self, vector2):
        self.x -= vector2.x
        self.y -= vector2.y

    def multiply_by_scalar(self, scalar):
        self.x *= scalar
        self.y *= scalar

    def divide_by_scalar(self, scalar):
        scalar += 0.0
        try:
            self.x /= scalar
            self.y /= scalar
        except ZeroDivisionError:
            self.x = 0
            self.y = 0

    def rotate(self, angle_in_radians):
        #keeps magnitude, but rotates vector by angle in radians
        #rotates clockwise, because of the way pixels in top left are 0,0 unlike graph
        #don't worry about it though, just know it rotates clockwise
        new_x = self.x * math.cos(angle_in_radians) - self.y * math.sin(angle_in_radians)
        new_y = self.y * math.cos(angle_in_radians) + self.x * math.sin(angle_in_radians)
        self.x = new_x
        self.y = new_y

    def set_angle(self, value_in_radians):
        length = self.get_mag()
        self.x = math.cos(value_in_radians) * length
        self.y = math.sin(value_in_radians) * length

    def truncate(self, limiting_value):
        if self.x > limiting_value:
            self.x = limiting_value
        if self.y > limiting_value:
            self.y = limiting_value