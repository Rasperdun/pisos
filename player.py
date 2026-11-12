import pygame

from circleshape import CircleShape
from constants import PLAYER_RADIUS, PLAYER_SHOOT_COOLDOWN_SECONDS, MAX_SPEED, MAX_REV_SPEED, FRICTION, ACCELERATION
from constants import LINE_WIDTH, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_SPEED
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        icon = pygame.image.load("rocket.png").convert_alpha()
        self.image = pygame.transform.scale(icon, (PLAYER_RADIUS * 3, PLAYER_RADIUS * 3))
        self.shoot_timer = 0
        self.speed = 0

    def draw(self, screen):
        rotated = pygame.transform.rotate(self.image, (180 - self.rotation))
        rect = rotated.get_rect(center=self.position)
        screen.blit(rotated, rect)
    
    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()
        self.shoot_timer -= dt

        if keys[pygame.K_SPACE]:
            self.shoot()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)

        if keys[pygame.K_w]:
            self.speed += ACCELERATION * dt
        elif keys[pygame.K_s]:
            self.speed -= ACCELERATION * dt
        else:
            # без газа скорость плавно уходит к нулю
            if self.speed > 0:
                self.speed = max(0, self.speed - FRICTION * dt)
            elif self.speed < 0:
                self.speed = min(0, self.speed + FRICTION * dt)

        # ограничиваем скорость
        self.speed = max(-MAX_REV_SPEED, min(self.speed, MAX_SPEED))

        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * self.speed * dt

    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        moment_speed = min(PLAYER_SPEED + 1 * dt, MAX_SPEED)
        rotated_with_speed_vector = rotated_vector * moment_speed
        self.position += rotated_with_speed_vector
    
    def shoot(self):
        if self.shoot_timer > 0:
            pass
        else:
            self.shoot_timer = PLAYER_SHOOT_COOLDOWN_SECONDS
            shot = Shot(self.position.x, self.position.y)
            shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        