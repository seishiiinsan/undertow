import pygame
import sys
from settings import *
from src.game import Game

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    # Instance du jeu
    game = Game(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Logique et Affichage
        screen.fill(WATER_COLOR)  # Nettoie l'écran
        game.run()  # Lance la logique du jeu

        pygame.display.update()
        clock.tick(FPS)