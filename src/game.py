import pygame
from settings import *
from src.entities import Player


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # Le vecteur de décalage (offset)
        self.offset = pygame.math.Vector2()

        # On calcule le centre de l'écran pour garder le joueur au milieu
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

    def custom_draw(self, player):
        """Dessine les sprites avec le décalage de la caméra."""
        # 1. Calculer le décalage (Offset)
        # On veut que le joueur soit au centre.
        # Donc Offset = Position du Joueur - Centre de l'écran
        self.offset.x = player.rect.centerx - self.half_w
        self.offset.y = player.rect.centery - self.half_h

        # 2. Dessiner chaque sprite avec le décalage
        # Note : On trie les sprites par position Y pour gérer la profondeur (2.5D)
        # (Ceux qui sont plus bas sur l'écran sont dessinés DEVANT ceux qui sont plus haut)
        for sprite in sorted(self.sprites(), key=lambda s: s.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((64, 64, 64)) # Gris foncé pour les murs
        self.rect = self.image.get_rect(topleft=pos)
        # Hitbox un peu plus petite pour le mur aussi (optionnel mais sympa)
        self.hitbox = self.rect.inflate(0, -10)

class Game:
    def __init__(self, screen):
        self.screen = screen

        # MODIF 1 : On utilise notre CameraGroup au lieu de Group standard
        self.visible_sprites = CameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()  # ### NOUVEAU

        self.create_map()

    def create_map(self):
        # On parcourt la liste WORLD_MAP ligne par ligne (row), index par index (col)
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, cell in enumerate(row):

                # Calcul de la position X, Y en pixels
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE

                if cell == 'x':
                    # Créer un mur
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites])

                if cell == 'p':
                    # Créer le joueur
                    # Note : On le crée ici, donc plus besoin de le faire dans __init__
                    self.player = Player(
                        (x, y),
                        [self.visible_sprites],
                        self.obstacle_sprites
                    )

    def run(self):
        # Update classique (logique de mouvement)
        self.visible_sprites.update()

        # MODIF 3 : On appelle notre custom_draw au lieu de draw
        # On doit lui passer le joueur pour qu'il sache qui suivre !
        self.visible_sprites.custom_draw(self.player)