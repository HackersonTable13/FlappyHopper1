import pygame
from settings import WIDTH, HEIGHT

pygame.font.init()

class GameIndicator:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('Bauhaus 93', 60)
        self.inst_font = pygame.font.SysFont('Bauhaus 93', 30)
        self.color = pygame.Color("white")
        self.inst_color = pygame.Color("black")
        self.lives_images = {
            1: pygame.image.load('assets/life/1life.png'),
            2: pygame.image.load('assets/life/2life.png'),
            3: pygame.image.load('assets/life/3life.png')
        }

    def show_lives(self, lives):
        if lives in self.lives_images:
            lives_image = self.lives_images[lives]
            self.screen.blit(lives_image, (10, 10))

    def show_score(self, int_score):
        bird_score = str(int_score)
        score = self.font.render(bird_score, True, self.color)
        self.screen.blit(score, (WIDTH // 2 - 20, 50))  # Centered score display

    def instructions(self):
        inst_text1 = "Press SPACE button to Jump,"
        inst_text2 = "Press \"R\" Button to Restart Game."
        ins1 = self.inst_font.render(inst_text1, True, self.inst_color)
        ins2 = self.inst_font.render(inst_text2, True, self.inst_color)
        self.screen.blit(ins1, (95, 400))
        self.screen.blit(ins2, (70, 450))

    def show_speed_up(self):
        inst_text = "Speed Up!"
        ins = self.inst_font.render(inst_text, True, self.inst_color)
        self.screen.blit(ins, (WIDTH // 2 - 100, HEIGHT // 2 - 100))