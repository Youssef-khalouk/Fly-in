
import pygame

WIDTH = 900
HEIGHT = 700

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Drones")

drone_image = pygame.image.load("images/drone.png").convert_alpha()

drone = pygame.transform.smoothscale(drone_image, (100, 100))
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)


def drow_circle(size: int):
    big_surface = pygame.Surface((size*4, size*4), pygame.SRCALPHA)
    pygame.draw.circle(big_surface, BLUE, (size*2, size*2), size*2)
    return pygame.transform.smoothscale(big_surface, (size, size))


small_surface = drow_circle(200)


clock = pygame.time.Clock()
running = True
x = 0
while running:
    screen.fill(BLACK)
    screen.blit(drone, (x, 30))
    screen.blit(small_surface, (100, 200))
    x += 1
    if x == 600:
        x = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
