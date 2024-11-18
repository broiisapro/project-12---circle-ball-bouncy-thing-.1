import pygame
import random
import math
import sys

# Initialize pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Simulation with Circular Boundary and Ball Collisions")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Constants
BALL_RADIUS = 10
CIRCLE_RADIUS = min(WIDTH, HEIGHT) // 3
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2
FPS = 60

# Ball class
class Ball:
    def __init__(self, x, y, dx, dy, radius=BALL_RADIUS, color=None):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.radius = radius
        self.color = color if color else self.random_color()

    def random_color(self):
        # Randomly generate a rainbow color
        return (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))

    def move(self):
        self.x += self.dx
        self.y += self.dy

        # Check for collision with circular boundary
        dist_from_center = math.sqrt((self.x - CENTER_X)**2 + (self.y - CENTER_Y)**2)
        if dist_from_center + self.radius > CIRCLE_RADIUS:
            angle = math.atan2(self.y - CENTER_Y, self.x - CENTER_X)
            # Reflect the ball off the boundary
            normal_dx = math.cos(angle)
            normal_dy = math.sin(angle)
            dot_product = self.dx * normal_dx + self.dy * normal_dy
            self.dx -= 2 * dot_product * normal_dx
            self.dy -= 2 * dot_product * normal_dy

            # Move the ball back within the boundary
            overlap = dist_from_center + self.radius - CIRCLE_RADIUS
            self.x -= normal_dx * overlap
            self.y -= normal_dy * overlap

    def check_collision(self, other):
        # Check if this ball collides with another ball
        dx = self.x - other.x
        dy = self.y - other.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance < self.radius + other.radius:
            # Vector from ball to ball
            normal_dx = dx / distance
            normal_dy = dy / distance

            # Relative velocity in terms of normal direction
            relative_velocity = (self.dx - other.dx) * normal_dx + (self.dy - other.dy) * normal_dy

            # If balls are moving towards each other, apply elastic collision
            if relative_velocity < 0:
                # Calculate the scalar factor
                impulse = 2 * relative_velocity / (self.radius**2 + other.radius**2)

                # Update velocities
                self.dx -= impulse * self.radius * normal_dx
                self.dy -= impulse * self.radius * normal_dy
                other.dx += impulse * other.radius * normal_dx
                other.dy += impulse * other.radius * normal_dy

                # To prevent the balls from speeding up, normalize the velocities to their initial speeds
                self.speed = math.sqrt(self.dx**2 + self.dy**2)
                other.speed = math.sqrt(other.dx**2 + other.dy**2)
                
                max_speed = 8  # Set a maximum speed for the balls

                # Limit speed to prevent speeding up
                if self.speed > max_speed:
                    self.dx = (self.dx / self.speed) * max_speed * 2
                    self.dy = (self.dy / self.speed) * max_speed * 2
                if other.speed > max_speed:
                    other.dx = (other.dx / other.speed) * max_speed
                    other.dy = (other.dy / other.speed) * max_speed

            # Separate the balls to avoid overlap
            overlap = self.radius + other.radius - distance
            self.x += (overlap / 2) * normal_dx
            self.y += (overlap / 2) * normal_dy
            other.x -= (overlap / 2) * normal_dx
            other.y -= (overlap / 2) * normal_dy

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

# Function to create random balls
def create_balls(num_balls):
    balls = []
    for _ in range(num_balls):
        angle = random.uniform(0, 2 * math.pi)
        radius = random.uniform(0, CIRCLE_RADIUS - BALL_RADIUS)
        x = CENTER_X + radius * math.cos(angle)
        y = CENTER_Y + radius * math.sin(angle)
        dx = random.uniform(-3, 3)
        dy = random.uniform(-3, 3)
        balls.append(Ball(x, y, dx, dy))
    return balls

# Main function
def main():
    clock = pygame.time.Clock()
    num_balls = 5
    balls = create_balls(num_balls)
    running = True
    while running:
        screen.fill(BLACK)

        # Draw circular boundary
        pygame.draw.circle(screen, WHITE, (CENTER_X, CENTER_Y), CIRCLE_RADIUS, 2)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart the simulation
                    balls = create_balls(num_balls)
                elif event.key == pygame.K_UP:  # Increase the number of balls
                    num_balls += 1
                    balls = create_balls(num_balls)
                elif event.key == pygame.K_DOWN:  # Decrease the number of balls
                    num_balls = max(1, num_balls - 1)
                    balls = create_balls(num_balls)

        # Move and check collisions for each ball
        for i, ball in enumerate(balls):
            ball.move()

            # Check collisions with other balls
            for j in range(i + 1, len(balls)):
                other_ball = balls[j]
                ball.check_collision(other_ball)

            ball.draw(screen)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()