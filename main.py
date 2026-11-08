import pygame

from constants import SCREEN_WIDTH
from constants import SCREEN_HEIGHT
from logger import log_state
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}") 
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    pygame.init()

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)

    player = Player((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
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
            if aster.collides_with(player):
                log_event("player_hit")
                print("Game over!")
                sys.exit()

        for drawing in drawable:
            drawing.draw(screen)
            
        pygame.display.flip()
    

if __name__ == "__main__":
    main()
