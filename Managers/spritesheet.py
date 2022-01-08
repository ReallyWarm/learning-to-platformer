import pygame

class SpriteSheet(object):
    def __init__(self, file_name):
        try:
            self.sheet = pygame.image.load(file_name).convert()
        except pygame.error as message:
            print(f'Unable to load spritesheet image: {file_name}')
            raise SystemExit(message)

    def sprite_at(self, rectangle, color_key=None):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if color_key is not None:
            if color_key == -1:
                color_key = image.get_at((0,0))
            image.set_colorkey(color_key, pygame.RLEACCEL)

        return image

    def sprites(self, rectangles, colorkey=None):
        return [self.sprite_at(rect, colorkey) for rect in rectangles]

    # Load a strip of images and returns them as a list
    def load_strip(self, rect, image_count, colorkey=None):
        rectangles = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3]) for x in range(image_count)]
        
        return self.sprites(rectangles, colorkey)