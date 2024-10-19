# powerup.py
import pygame
from settings import pipe_gap

class Powerup(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        super().__init__()
        # Load the power-up image
        self.image = pygame.image.load('assets/powerup/powerup.png').convert_alpha()
        self.rect = self.image.get_rect()
        if position == 1:
            self.rect.bottomleft = [x - 100, y - int(pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x - 100, y + int(pipe_gap / 2)]
    
    def update(self, x_shift):
        self.rect.x += x_shift  # Move with the world's shift
        if self.rect.right < 0:
            self.kill()
