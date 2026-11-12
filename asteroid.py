import pygame
import random
from logger import log_state, log_event
from circleshape import CircleShape
from constants import SCREEN_WIDTH, ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS
from constants import SCREEN_HEIGHT, LINE_WIDTH

class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)
        
    def draw(self, screen: pygame.Surface) -> None:
        aster = pygame.draw.circle(screen, "White", self.position, self.radius, LINE_WIDTH)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        else:
            log_event("asteroid_split")
            bob = random.uniform(20, 50)
            velocity1 = self.velocity.rotate(bob)
            velocity2 = self.velocity.rotate(-bob)
            new_radius = self.radius - ASTEROID_MIN_RADIUS
            aster1 = Asteroid(self.position.x, self.position.y, new_radius)
            aster2 = Asteroid(self.position.x, self.position.y, new_radius)
            aster1.velocity = velocity1 * 1.2
            aster2.velocity = velocity2 * 1.2
            aster1.CAN_COLLIDE = False
            aster2.CAN_COLLIDE = False
            
            aster1.CAN_COLLIDE = True
            aster2.CAN_COLLIDE = True