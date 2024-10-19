# bullet.py

import pygame
from settings import WIDTH, HEIGHT  # Ensure WIDTH and HEIGHT are imported

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, target_pos):
        super().__init__()
        img_path = 'assets/shooter/net.png'
        self.image = pygame.image.load(img_path).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.speed = 4  # Adjust as needed
        self.velocity = self.compute_velocity(pos, target_pos, self.speed)

    def compute_velocity(self, start_pos, target_pos, speed):
        dx = target_pos[0] - start_pos[0]
        dy = target_pos[1] - start_pos[1]
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance == 0:
            return pygame.math.Vector2(0, 0)
        else:
            dx /= distance
            dy /= distance
            return pygame.math.Vector2(dx * speed, dy * speed)

    def update(self):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
        if (self.rect.right < 0 or self.rect.left > WIDTH or
            self.rect.bottom < 0 or self.rect.top > HEIGHT):
            self.kill()
