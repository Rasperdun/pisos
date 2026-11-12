import pygame
import sys

from constants import SCREEN_WIDTH
from constants import SCREEN_HEIGHT
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}") 
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    pygame.init()

    font = pygame.font.Font(None, 40)   # None = шрифт по умолчанию, 36 = размер
    big_font = pygame.font.Font(None, 90)
    score = 0

    pygame.display.set_caption("Game made by Пердольф Пуклер")

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    player = Player((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))
    asteroidfield = AsteroidField()

    clock = pygame.time.Clock()
    dt = 0.0

    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        dt = clock.tick(60) / 1000
        screen.fill("black", rect=None, special_flags=0)
        updatable.update(dt)

        for aster in asteroids:
            for aster2 in asteroids:
                if aster2 == aster:
                    pass
                else:
                    if aster.collides_with(aster2):
                        log_event("aster_bump")
                        aster.velocity = aster.velocity.rotate(90)
                        aster2.velocity = aster2.velocity.rotate(90)

            if aster.collides_with(player):
                log_event("player_hit")
                print("Game over!")
                sys.exit()
            for shot in shots:
                if aster.collides_with(shot):
                    log_event("asteroid_shot")
                    shot.kill()
                    aster.split()
                    score += 5



        for drawing in drawable:
            drawing.draw(screen)

        text1 = font.render(f"dt: {dt}", True, "white")
        text2 = font.render(f"Хуёвый счёт: {score}", True, "white")
        screen.blit(text1, (10, 10))
        screen.blit(text2, (10, 50))

        if score >= 100:
            text = big_font.render("ПОБЕДА", True, "white")
            rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            screen.blit(text, rect)
            pygame.display.flip()      # ВАЖНО: показать надпись до ожидания
            pygame.time.wait(8000)     # миллисекунды
            sys.exit()

            
        pygame.display.flip()
    

if __name__ == "__main__":
    main()
