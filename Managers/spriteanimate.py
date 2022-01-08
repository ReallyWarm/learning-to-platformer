from .spritesheet import SpriteSheet

class SpriteAnimate(object):
    def __init__(self, file_name, rect, image_count, color_key=None, loop=False, frames=1):
        self.file_name = file_name
        sprite = SpriteSheet(file_name)
        self.sprites = sprite.load_strip(rect, image_count, color_key)
        self.loop = loop
        self.image_num = 0
        self.frames_time = frames
        self.frame_num = frames

    def iter(self):
        self.image_num = 0
        self.frame_num = self.frames_time

        return self

    def next(self):
        if self.image_num >= len(self.sprites):
            if not self.loop:
                raise StopIteration
            else:
                self.image_num = 0
        
        image = self.sprites[self.image_num]
        self.frame_num -= 1
        if self.frame_num == 0:
            self.image_num += 1
            self.frame_num = self.frames_time

        return image

    def __add__(self, sprite):
        self.sprites.extend(sprite.sprites)

        return self

