import pygame, random

class VFX(object):
    def __init__(self, type, pos, intensity, velocity, time, gen_time):
        self.pos = pos
        self.velo = velocity
        self.insty = intensity
        self.time = time
        self.gen_time = gen_time
        self.particles = []
        self.type = type
        self.loop = 0
        self.done = False
        self.remove = False

    def DustVFX(self, screen):
        if not self.done:
            self.particles.append([[self.pos[0],self.pos[1]], [random.randint(self.insty[0], self.insty[1]) / 10 - 1, self.velo], random.randint(self.time[0], self.time[1])])
        for particle in self.particles:
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            particle[2] -= 0.1
            particle[1][1] += 0.1
            pygame.draw.circle(screen, (255, 255, 255), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
            self.loop += 1
            if particle[2] <= 0:
                self.particles.remove(particle)
            if self.loop > self.gen_time:
                self.done = True

        if not self.particles:
            self.remove = True


    def start(self, screen):
        if self.remove:
                return 1

        self.loop = 0
        if self.type == "dust":
            self.DustVFX(screen)