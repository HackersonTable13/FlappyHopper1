# life.py
import pygame

class Life(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        # Load and scale the life image
        self.image = pygame.image.load('assets/life/life.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(topleft=pos)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, x_shift):
        # Move the life object horizontally
        self.rect.x += x_shift
        # Remove the life object if it moves off-screen
        if self.rect.right < 0:
            self.kill()
