import pygame
from Managers import SpriteAnimate
from constants import KEY_B

class FieldObject(object):
    def __init__(self, id, pos, size):
        self.id = id
        self.pos = pos
        self.size = size

        if self.id == "C":
            self.sprite = SpriteAnimate('data/images/coin.png', (0, 0, self.size[0], self.size[1]), 6, KEY_B, True, 10)
        else:
            self.sprite = None

        self.rect = pygame.Rect((self.pos), (self.size[0], self.size[1]))
        self.scroll = [0, 0]

    def getId(self):
        return self.id

    def getPos(self):
        return self.pos

    def getSize(self):
        return self.size

    def updateScroll(self, scroll):
        self.scroll = scroll

    def checkCollision(self, player):
        if self.rect.colliderect(player):
            return True
    
    def update(self, screen):
        image = self.sprite.next().convert()
        screen.blit(image, (self.pos[0] - self.scroll[0], self.pos[1]  - self.scroll[1]))