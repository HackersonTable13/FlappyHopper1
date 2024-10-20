# shooter.py

import pygame
from bullet import Bullet
from settings import WIDTH, HEIGHT  # Import WIDTH and HEIGHT

class Shooter(pygame.sprite.Sprite):
    def __init__(self, bullets_group, bird):
        super().__init__()
        img_path = 'assets/shooter/shooter.png'
        self.image = pygame.image.load(img_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topright = (WIDTH, HEIGHT // 2)  # Position at right central
        self.shoot_delay = 200  # Frames between shots
        self.shoot_timer = 0
        self.bullets_group = bullets_group
        self.bird = bird

    def update(self):
        # Shooter remains stationary at top-right corner
        self.rect.topright = (WIDTH, HEIGHT // 2)
        
        # Handle shooting bullets at intervals
        self.shoot_timer += 1
        if self.shoot_timer >= self.shoot_delay:
            self.shoot_timer = 0
            self.shoot_bullet()

    def shoot_bullet(self):
        bullet_pos = self.rect.center
        target_pos = self.bird.rect.center
        bullet = Bullet(bullet_pos, target_pos)
        self.bullets_group.add(bullet)
