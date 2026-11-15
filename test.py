import pygame
import random
from pathlib import Path

COLOR = (255, 100, 98)        
SURFACE_COLOR = (167, 255, 100) 
WIDTH = 500
HEIGHT = 500

class Sprite(pygame.sprite.Sprite):
    def __init__(self, color, height, width):
        super().__init__()

        texture_path = Path(__file__).parent / "assets" / "player" / "0_idle.png"
        texture = pygame.image.load(texture_path).convert_alpha()
        self.image = pygame.transform.scale(texture, (width, height))

        self.rect = self.image.get_rect()

# ---------------------------------------------------------------------------- #

pygame.init()

BLUE = (0, 0, 255)  
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Creating Sprite")

all_sprites_list = pygame.sprite.Group()

object_ = Sprite((0, 0, 255), 200, 200)
object_.rect.x = 150  
object_.rect.y = 150  

all_sprites_list.add(object_)

exit_game = True
clock = pygame.time.Clock()

while exit_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_game = False

    all_sprites_list.update()  
    screen.fill(SURFACE_COLOR)  
    all_sprites_list.draw(screen) 
    pygame.display.flip()       
    clock.tick(60)              

pygame.quit()