import pygame
import os
from settings import *
# IMPORTANT : Vérifie que cette ligne est bien là tout en haut
from src.utils import import_sprite_strip


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)

        # --- SETUP ANIMATION ---
        self.status = 'idle'
        self.frame_index = 0
        self.animation_speed = 0.15

        self.attacking = False
        self.attack_cooldown = 400  # 400 millisecondes entre deux attaques
        self.attack_time = 0

        # C'est ici que ça plantait : la fonction n'existait pas encore
        self.import_player_assets()

        # Image initiale
        self.image = self.animations[self.status][self.frame_index]

        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -20)
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.obstacle_sprites = obstacle_sprites
        self.facing_right = True

    # --- VOICI LE BLOC MANQUANT À AJOUTER ---
    # Attention à l'indentation : il doit être aligné avec def __init__
    def import_player_assets(self):
        character_path = os.path.join('assets', 'graphics', 'player')
        self.animations = {
            'idle': [],
            'run': [],
            'attack': []
        }

        # On remplit le dictionnaire
        # Assure-toi que les fichiers idle.png et run.png existent bien !
        self.animations['idle'] = import_sprite_strip(os.path.join(character_path, 'idle.png'), 4)
        self.animations['run'] = import_sprite_strip(os.path.join(character_path, 'run.png'), 4)
        self.animations['attack'] = import_sprite_strip(os.path.join(character_path, 'swordattack.png'), 4)

    # ----------------------------------------

    def input(self):
        if not self.attacking:
            keys = pygame.key.get_pressed()

            # Mouvements (inchangé)
            if keys[pygame.K_z] or keys[pygame.K_UP]: self.direction.y = -1
            elif keys[pygame.K_s] or keys[pygame.K_DOWN]: self.direction.y = 1
            else: self.direction.y = 0

            if keys[pygame.K_q] or keys[pygame.K_LEFT]: self.direction.x = -1
            elif keys[pygame.K_d] or keys[pygame.K_RIGHT]: self.direction.x = 1
            else: self.direction.x = 0

            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.direction.x = 0
                self.direction.y = 0
                self.frame_index = 0

    def get_status(self):
        if self.attacking:
            self.status = 'attack'
            # On stoppe le mouvement pendant l'attaque
            self.direction.x = 0
            self.direction.y = 0
        else:
            if self.direction.x == 0 and self.direction.y == 0:
                self.status = 'idle'
            else:
                self.status = 'run'

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            # Si le temps écoulé dépasse le cooldown, on finit l'attaque
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.hitbox):
                    if self.direction.x > 0: self.hitbox.right = sprite.rect.left
                    if self.direction.x < 0: self.hitbox.left = sprite.rect.right
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.hitbox):
                    if self.direction.y > 0: self.hitbox.bottom = sprite.rect.top
                    if self.direction.y < 0: self.hitbox.top = sprite.rect.bottom

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image_to_show = animation[int(self.frame_index)]

        # Gestion du flip (inchangée)
        if self.direction.x > 0:
            self.facing_right = True
        elif self.direction.x < 0:
            self.facing_right = False

        if not self.facing_right:
            self.image = pygame.transform.flip(image_to_show, True, False)
        else:
            self.image = image_to_show

    def update(self):
        self.input()
        self.cooldowns()  # ### NOUVEAU : On vérifie les timers
        self.get_status()
        self.move(self.speed)
        self.animate()