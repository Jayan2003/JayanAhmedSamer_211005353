
import random
from OpenGL.GL import *
import math

class FallingShape:
    def __init__(self, correct_type):
        self.x = random.randint(50, 750)
        self.y = 600
        self.speed = 2
        self.rotation_angle = random.uniform(0, 360)
        self.rotation_speed = random.uniform(1, 3)

        # 70% chance to be correct shape, 30% wrong
        if random.random() < 0.7:
            self.type = correct_type
        else:
            self.type = random.choice(["circle", "square", "triangle", "star"])

        self.size = 30
        self.color = {
            "circle": (0.6, 0.1, 0.7),
            "square": (1, 0.5, 0),
            "triangle": (0.1, 0.7, 0.3),
            "star": (1, 1, 0)
        }[self.type]

    def update(self):
        self.y -= self.speed
        self.rotation_angle = (self.rotation_angle + self.rotation_speed) % 360

    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, 0)
        glRotatef(self.rotation_angle, 0, 0, 1)
        glColor3f(*self.color)

        if self.type == "circle":
            self.draw_circle()
        elif self.type == "square":
            self.draw_square()
        elif self.type == "triangle":
            self.draw_triangle()
        elif self.type == "star":
            self.draw_star()

        glPopMatrix()

    def draw_circle(self):
        glBegin(GL_POLYGON)
        for i in range(30):
            angle = 2 * math.pi * i / 30
            glVertex2f(math.cos(angle) * self.size, math.sin(angle) * self.size)
        glEnd()

    def draw_square(self):
        half = self.size
        glBegin(GL_QUADS)
        glVertex2f(-half, -half)
        glVertex2f(half, -half)
        glVertex2f(half, half)
        glVertex2f(-half, half)
        glEnd()

    def draw_triangle(self):
        glBegin(GL_TRIANGLES)
        glVertex2f(0, self.size)
        glVertex2f(-self.size, -self.size)
        glVertex2f(self.size, -self.size)
        glEnd()

    def draw_star(self):
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(0, 0)
        for i in range(11):
            angle = math.pi * i / 5
            radius = self.size if i % 2 == 0 else self.size / 2
            glVertex2f(math.cos(angle) * radius, math.sin(angle) * radius)
        glEnd()
