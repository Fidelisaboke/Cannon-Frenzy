""" This module initializes and manages the game. """

import sys
import pygame
import sprites
from constants import *
from level import Level
from levels_config import LEVELS_CONFIG


class CannonFrenzy:
    def __init__(self):
        # Initialize pygame modules
        pygame.init()

        # Stop the game if pygame fails to initialize
        if not pygame.get_init():
            print("Failed to initialize Pygame!")
            sys.exit()

        # Set game properties
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Cannon Frenzy")
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.font = pygame.font.Font(None, 36)


        # Levels configuration
        self.levels = [Level(self.screen, **config) for config in LEVELS_CONFIG]
        self.current_level_index = 0
        self.current_level = self.levels[self.current_level_index]

        # Initial properties -> Level 1
        self.score = 0
        self.game_over = False
        self.cannonballs = []
        self.cannon = sprites.Cannon(self.screen, self.cannonballs, self.current_level.cannonballs_left)

    def reset_game(self):
        """ Resets the game state. """
        self.current_level_index = 0
        self.current_level = self.levels[self.current_level_index]
        self.score = 0
        self.game_over = False
        self.cannonballs = []
        self.cannon = sprites.Cannon(self.screen, self.cannonballs, self.current_level.cannonballs_left)

    def run(self):
        """ Runs the game loop. """

        while True:
            # Event handling
            for event in pygame.event.get():

                # On exiting the game
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Press 'R' key to restart the game
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and self.game_over:
                        self.reset_game()

            # Game over condition
            if self.cannon.cannonballs_left == 0 and len(self.cannon.cannonballs) == 0:
                self.game_over = True

            if self.game_over:
                self.display_game_over()
            else:
                self.screen.fill("White")
                self.cannon.draw()
                self.current_level.draw()


                for cannonball in self.cannonballs[:]:
                    cannonball.move()
                    cannonball.draw()

                    if cannonball.is_off_screen():
                        self.cannonballs.remove(cannonball)

                    for target in self.current_level.targets[:]:
                        if target.hit(cannonball):
                            self.current_level.targets.remove(target)
                            self.cannonballs.remove(cannonball)
                            self.score += 10
                            break


                # Check if all targets are hit
                if not self.current_level.targets:
                    self.current_level_index += 1
                    if self.current_level_index < len(self.levels):
                        self.current_level = self.levels[self.current_level_index]
                        cannonballs_left = self.current_level.cannonballs_left
                        self.cannon = sprites.Cannon(self.screen, self.cannonballs, cannonballs_left)


                # Display level, score and cannonballs left
                self.font = pygame.font.Font(None, 36)

                level_text = self.font.render(f"Level: {self.current_level.level_number}", True, "Black")
                level_text_rect = level_text.get_rect(topleft=(10, 10))
                self.screen.blit(level_text, level_text_rect)

                score_text = self.font.render(f"Score: {self.score}", True, "Black")
                score_text_rect = score_text.get_rect(topleft=(10, 50))
                self.screen.blit(score_text, score_text_rect)

                cannonballs_left_text = self.font.render(
                    f"Cannonballs Left: {self.cannon.cannonballs_left}",
                    True,
                    "Black"
                )
                cannonballs_left_text_rect = cannonballs_left_text.get_rect(topleft=(10, 90))
                self.screen.blit(cannonballs_left_text, cannonballs_left_text_rect)

                # Update the cannon sprite
                self.cannon.update()

            pygame.display.update()
            self.clock.tick(self.fps)


    def display_game_over(self):
        """ Displays the game over screen. """
        pygame.display.update()
        self.clock.tick(self.fps)
        pygame.time.delay(1000)

        # Game over screen
        self.screen.fill("White")
        self.font = pygame.font.Font(None, 36)
        game_over_text = self.font.render("GAME OVER!", True, "Black")
        game_over_rect = game_over_text.get_rect(center=(400, 260))
        self.screen.blit(game_over_text, game_over_rect)

        score_text = self.font.render(f"Score: {self.score}", True, "Black")
        score_text_rect = score_text.get_rect(center=(400, 300))
        self.screen.blit(score_text, score_text_rect)

        restart_text = self.font.render("Press R to restart game", True, "Black")
        restart_text_rect = restart_text.get_rect(center=(400, 340))
        self.screen.blit(restart_text, restart_text_rect)
