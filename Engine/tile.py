import pygame
from Managers import SpriteSheet
from constants import KEY_B, TILE_SIZE

class Tile(pygame.sprite.Sprite):
    def __init__(self, id, pos, size):
        super().__init__()
        self.id = id
        self.pos = pos
        # Check new Row
        if self.id > 9:
            self.col = self.id - 9
            self.row = self.id // 10
        else:
            self.col = self.id
            self.row = 0

        image_location = 'data/images/Tile32.bmp'
        sprites = SpriteSheet(image_location)
        self.image = sprites.sprite_at(((self.col - 1) * TILE_SIZE, self.row * TILE_SIZE, size[0], size[1]), KEY_B)
        
        self.rect = self.image.get_rect(topleft=self.pos)
        self.scroll = [0, 0]

    def updateScroll(self, scroll):
        self.scroll = scroll
    
    def update(self, screen):
        screen.blit(self.image, (self.pos[0] - self.scroll[0] ,self.pos[1] - self.scroll[1]))
