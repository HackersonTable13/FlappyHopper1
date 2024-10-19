# main.py
import pygame, sys
from settings import WIDTH, HEIGHT, ground_space
from world import World
from game import GameIndicator, Game

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT + ground_space))
pygame.display.set_caption("Flappy Hopper")


class Main:
    def __init__(self, screen):
        self.screen = screen
        self.bg_img = pygame.image.load('assets/terrain/bg.png')
        self.bg_img = pygame.transform.scale(self.bg_img, (WIDTH, HEIGHT))
        self.ground_img = pygame.image.load('assets/terrain/ground.png')
        self.ground_scroll = 0
        self.FPS = pygame.time.Clock()
        self.stop_ground_scroll = False
        self.indicator = GameIndicator(screen)
        self.game = Game()

    def main(self):
        world = World(screen)
        while True:
            self.stop_ground_scroll = world.game_over
            self.screen.blit(self.bg_img, (0, 0))
            # Show ground scrolling effect
            self.screen.blit(self.ground_img, (self.ground_scroll, HEIGHT))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Handle input based on game state
                if self.game.state == "MENU":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.game.state = "PLAYING"

                elif self.game.state == "PLAYING":
                    if event.type == pygame.KEYDOWN:
                        if not world.playing and not world.game_over:
                            world.playing = True
                        if event.key == pygame.K_SPACE:
                            world.update("jump")
                        if event.key == pygame.K_r:
                            world.update("restart")

                elif self.game.state == "GAME_OVER":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            self.game.ret()
                            world.update("restart")
                        elif event.key == pygame.K_q:
                            pygame.quit()
                            sys.exit()

            # Update the game world and UI based on the current state
            if self.game.state == "MENU":
                self.stop_ground_scroll = world.game_over
                self.indicator.show_menu()

            elif self.game.state == "PLAYING":
                self.stop_ground_scroll = world.game_over

                # Handle game updates
                world.adjust_speed()  # Adjust the game speed based on the score
                world.update()


                if not self.stop_ground_scroll:
                    self.ground_scroll += world.scroll_speed
                    if abs(self.ground_scroll) > WIDTH:
                        self.ground_scroll = 0

                if world.game_over:
                    self.game.state = "GAME_OVER"

            elif self.game.state == "GAME_OVER":
                self.indicator.show_game_over(world.player.sprite.score)

            pygame.display.update()
            self.FPS.tick(60)


if __name__ == "__main__":
    play = Main(screen)
    play.main()
