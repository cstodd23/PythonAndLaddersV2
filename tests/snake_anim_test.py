import pygame
import math
from pygame.math import Vector2

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1500, 1500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Animation")

# Colors
WHITE = (255, 255, 255)
RED = (172, 57, 49)

class Chain:
    def __init__(self, origin, num_joints, length, angle):
        self.joints = [Vector2(origin)]
        self.angles = [0]
        for _ in range(1, num_joints):
            prev_joint = self.joints[-1]
            new_joint = prev_joint + Vector2(length, 0).rotate_rad(self.angles[-1])
            self.joints.append(new_joint)
            self.angles.append(self.angles[-1] + angle)

    def resolve(self, target_pos):
        self.joints[0] = Vector2(target_pos)
        for i in range(1, len(self.joints)):
            diff = self.joints[i] - self.joints[i-1]
            self.angles[i-1] = math.atan2(diff.y, diff.x)
            self.joints[i] = self.joints[i-1] + Vector2(64, 0).rotate_rad(self.angles[i-1])

class Snake:
    def __init__(self, origin):
        self.spine = Chain(origin, 48, 64, math.pi/8)

    def resolve(self, mouse_pos):
        head_pos = self.spine.joints[0]
        target_pos = head_pos + (Vector2(mouse_pos) - head_pos).normalize() * 8
        self.spine.resolve(target_pos)

    def display(self, screen):
        pygame.draw.lines(screen, WHITE, False, [joint for joint in self.spine.joints], 4)

        points = []
        # Right half of the snake
        for i in range(len(self.spine.joints)):
            points.append(self.get_pos(i, math.pi/2, 0))
        points.append(self.get_pos(47, math.pi, 0))
        # Left half of the snake
        for i in range(len(self.spine.joints) - 1, -1, -1):
            points.append(self.get_pos(i, -math.pi/2, 0))
        # Top of the head
        points.append(self.get_pos(0, -math.pi/6, 0))
        points.append(self.get_pos(0, 0, 0))
        points.append(self.get_pos(0, math.pi/6, 0))

        pygame.draw.polygon(screen, RED, points)

        # Eyes
        pygame.draw.circle(screen, WHITE, self.get_pos(0, math.pi/2, -18), 12)
        pygame.draw.circle(screen, WHITE, self.get_pos(0, -math.pi/2, -18), 12)

    def body_width(self, i):
        if i == 0:
            return 76
        elif i == 1:
            return 80
        else:
            return 64 - i

    def get_pos(self, i, angle_offset, length_offset):
        angle = self.spine.angles[i] + angle_offset
        width = self.body_width(i) + length_offset
        return (
            self.spine.joints[i].x + math.cos(angle) * width,
            self.spine.joints[i].y + math.sin(angle) * width
        )

# Create snake
snake = Snake(Vector2(WIDTH // 2, HEIGHT // 2))

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse_pos = pygame.mouse.get_pos()
    snake.resolve(mouse_pos)

    screen.fill((0, 0, 0))  # Clear screen
    snake.display(screen)
    pygame.display.flip()

    clock.tick(60)  # 60 FPS

pygame.quit()