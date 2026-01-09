import pygame
from settings import TILE_SIZE


def import_sprite_strip(path, frame_count):
    """
    Charge une image 'bande' et la découpe en une liste d'images carrées.
    Suppose que les sprites sont carrés et font la taille TILE_SIZE.
    """
    surface_list = []
    try:
        # On charge la grande image
        strip_image = pygame.image.load(path).convert_alpha()

        # On la découpe
        for x in range(frame_count):
            # On crée une surface vide de la taille d'une tuile
            image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            # On copie ("blit") la bonne portion de la bande sur cette surface vide
            # Le rectangle de découpe est (x * TILE_SIZE, 0, TILE_SIZE, TILE_SIZE)
            image.blit(strip_image, (0, 0), (x * TILE_SIZE, 0, TILE_SIZE, TILE_SIZE))
            surface_list.append(image)

    except FileNotFoundError:
        print(f"ERREUR : Impossible de charger l'animation à {path}")
        # Fallback : un carré rouge pour ne pas faire planter le jeu
        img = pygame.Surface((TILE_SIZE, TILE_SIZE))
        img.fill('red')
        surface_list.append(img)

    return surface_list