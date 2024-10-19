# world.py
import time
import pygame
from pipe import Pipe
from bird import Bird
from game import GameIndicator
from settings import WIDTH, HEIGHT, pipe_size, pipe_gap, pipe_pair_sizes
from shooter import Shooter
from bullet import Bullet
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
        self.scroll_speed = -3
        self.last_speed_increase = 0
        self._generate_world()
        self.playing = False
        self.game_over = False
        self.game = GameIndicator(screen)

        self.last_life_spawn_time = time.time()  # Track the last spawn time
        self.life_spawn_interval = random.randint(5, 10)


        # shooter logic 
        self.bullets_group = pygame.sprite.Group()
        self.shooter_group = pygame.sprite.Group()
        self.shooter_active = False
        self.shooter_start_score = 0
        self.last_shooter_score = -6

    def _add_shooter(self):
        shooter = Shooter(self.bullets_group, self.player.sprite)
        self.shooter_group.add(shooter)
        self.shooter_active = True
        self.shooter_start_score = self.player.sprite.score
        self.last_shooter_score = self.player.sprite.score

    def _handle_shooter(self):
        bird_score = self.player.sprite.score
        # Check if it's time to add a shooter
        if (bird_score % 6 == 0 and bird_score != 0 and
            not self.shooter_active and bird_score != self.last_shooter_score):
            self._add_shooter()
        # Remove shooter after 5 additional points
        if self.shooter_active and bird_score >= self.shooter_start_score + 5:
            self.shooter_group.empty()
            self.bullets_group.empty()
            self.shooter_active = False
            


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
            or pygame.sprite.spritecollide(bird, self.bullets_group, False, pygame.sprite.collide_mask)
            or bird.rect.bottom >= HEIGHT
            or bird.rect.top <= 0
        )

        if collision:
            if bird.invulnerable:
                return  # Ignore collisions while invulnerable
            if bird.lives > 1:
                bird.lives -= 1
                bird.invulnerable = True
                bird.invulnerable_end_time = time.time() + 2  # 2 seconds of invulnerability
            else:
                self.playing = False
                self.game_over = True
        else:
            # Existing scoring logic
            if bird.rect.x >= self.current_pipe.rect.centerx and self.passed:
                bird.score += 1
                self.passed = False
            if bird.rect.x < self.current_pipe.rect.centerx:
                self.passed = True

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
            self.shooter_group.empty()
            self.bullets_group.empty()
            self.shooter_active = False
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

        if self.player.sprite.score % 10 == 0 and self.player.sprite.score != 0:
            self.game.show_speed_up()



        # shooter logic
        self._handle_shooter()

        # Update and draw shooter
        if self.shooter_active:
            self.shooter_group.update()
            self.shooter_group.draw(self.screen)

        # Update and draw bullets
        self.bullets_group.update()
        self.bullets_group.draw(self.screen)

    # Adjust speed
    def adjust_speed(self):
        bird = self.player.sprite
        speed = self.scroll_speed
        # Increase the speed every time the score reaches a new multiple of 10
        if bird.score >= 10:
            self.scroll_speed = speed
            if bird.score % 10 == 0:
                if bird.score != self.last_speed_increase:
                    self.scroll_speed -= 2  # increase the speed (decrease the value)
                    self.last_speed_increase = bird.score
        else:
            self.scroll_speed = -3  # default speed when score is below 10
