# world.py
import time
import pygame
from pipe import Pipe
from bird import Bird
from game import GameIndicator
from settings import WIDTH, HEIGHT, pipe_size, pipe_gap, pipe_pair_sizes
import random
from life import Life  # Import the Life class
from powerup import Powerup  # Import the Powerup class



class World:
    def __init__(self, screen):
        self.pipe_counter = 0  # Counter for adding life objects
        self.screen = screen
        self.world_shift = 0
        self.current_x = 0
        self.gravity = 0.5
        self.current_pipe = None
        self.powerups = pygame.sprite.Group()  # Sprite group for power-ups
        self.pipes = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.lives = pygame.sprite.Group()  # Sprite group for life objects

        self._generate_world()
        self.playing = False
        self.game_over = False
        self.game = GameIndicator(screen)

        self.last_life_spawn_time = time.time()  # Track the last spawn time
        self.life_spawn_interval = random.randint(5, 10)

    # adds pipe once the last pipe added reached the desired pipe horizontal spaces
    def _add_pipe(self):
        pipe_pair_size = random.choice(pipe_pair_sizes)
        top_pipe_height, bottom_pipe_height = pipe_pair_size[0] * pipe_size, pipe_pair_size[1] * pipe_size
        pipe_top = Pipe((WIDTH, 0 - (bottom_pipe_height + pipe_gap)), pipe_size, HEIGHT, True)

        # Create bottom pipe (used for scoring)
        pipe_bottom = Pipe((WIDTH, top_pipe_height + pipe_gap), pipe_size, HEIGHT, False, is_bottom=True)

        self.pipes.add(pipe_top)
        self.pipes.add(pipe_bottom)
        self.current_pipe = pipe_top
        # Randomly decide whether to spawn a power-up
        if random.randint(1, 5) == 1:  # 20% chance to spawn a power-up
            position = random.choice([1, -1])  # Position above or below the pipe gap
            powerup = Powerup(WIDTH, HEIGHT // 2, position)
            self.powerups.add(powerup)

    # New method to spawn life objects randomly
    def _spawn_life_object(self):
        current_time = time.time()
        if current_time - self.last_life_spawn_time > self.life_spawn_interval:
            life_y_pos = random.randint(50, HEIGHT - 100)
            life = Life((WIDTH + 50, life_y_pos), 30)
            self.lives.add(life)
            self.last_life_spawn_time = current_time
            self.life_spawn_interval = random.randint(5, 10)  # Reset interval
            
    # creates the player and the obstacle
    def _generate_world(self):
        self._add_pipe()
        bird = Bird((WIDTH//2 - pipe_size, HEIGHT//2 - pipe_size), 30)
        self.player.add(bird)



    # for moving background/obstacle
    def _scroll_x(self):
        if self.playing:
            self.world_shift = self.scroll_speed
        else:
            self.world_shift = 0

    # add gravity to bird for falling
    def _apply_gravity(self, player):
        if self.playing or self.game_over:
            player.direction.y += self.gravity
            player.rect.y += player.direction.y

    def _handle_collisions(self):
        bird = self.player.sprite
        
        # Collision with pipes or boundaries
        collision = (
            pygame.sprite.spritecollide(bird, self.pipes, False, pygame.sprite.collide_mask)
            or bird.rect.bottom >= HEIGHT
            or bird.rect.top <= 0
        )

        if collision:
            if bird.invulnerable:
                return
            if bird.lives > 1:
                bird.lives -= 1
                bird.invulnerable = True
                bird.invulnerable_end_time = time.time() + 2  # 2 seconds of invulnerability
            else:
                self.playing = False
                self.game_over = True

        # Collision with power-ups
        powerup_collision = pygame.sprite.spritecollide(bird, self.powerups, True, pygame.sprite.collide_mask)
        if powerup_collision:
            bird.score += 1  # Increase score by 1

        # Collision with life objects (if any)
        life_collision = pygame.sprite.spritecollide(bird, self.lives, True, pygame.sprite.collide_mask)
        if life_collision:
            bird.lives += 1  # Increase lives by 1



    # updates the bird's overall state
    def update(self, player_event = None):
        # new pipe adder
        if self.current_pipe.rect.centerx  <= (WIDTH // 2) - pipe_size:
            self._add_pipe()
        # Spawn life objects during gameplay
        if self.playing:
            self._spawn_life_object()
        # updates, draws pipes
        self.pipes.update(self.world_shift)
        self.pipes.draw(self.screen)
        # Update and draw life objects
        self.lives.update(self.world_shift)
        self.lives.draw(self.screen)
        # Update and draw power-ups
        self.powerups.update(self.world_shift)
        self.powerups.draw(self.screen)
        # Check for scoring
        bird = self.player.sprite
        for pipe in self.pipes:
            if (
                pipe.is_bottom
                and not pipe.scored
                and pipe.rect.right < bird.rect.left
            ):
                bird.score += 1
                pipe.scored = True
        # applying game physics
        self._apply_gravity(self.player.sprite)
        self._scroll_x()
        self._handle_collisions()
        # configuring player actions
        if player_event == "jump" and not self.game_over:
            player_event = True
        elif player_event == "restart":
            self.game_over = False
            self.playing = False
            self.pipes.empty()
            self.lives.empty()
            self.powerups.empty()  # Clear power-ups
            self.player.empty()
            self._generate_world()
        else:
            player_event = False
        if not self.playing:
            self.game.instructions()
        # updates, draws pipes
        self.player.update(player_event)
        self.player.draw(self.screen)
        self.game.show_score(self.player.sprite.score)
        #display lives
        self.game.show_lives(self.player.sprite.lives)

    # Adjust speed
    def adjust_speed(self):
        bird = self.player.sprite
        # Increase the speed when score reaches multiples of 10
        if bird.score >= 10:
            self.scroll_speed = -7  # faster speed
        elif bird.score >= 5:
            self.scroll_speed = -5  # moderate speed
        else:
            self.scroll_speed = -3  # default speed
