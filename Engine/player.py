import pygame
from Managers import SpriteAnimate, move_collision, deltatime
from constants import P_WIDTH, P_HEIGHT, DISPLAY_SIZE, KEY_G
from .visualeffect import VFX

class Player(object):
    def __init__(self, StartPos, facing=1):
        self.sprite = [SpriteAnimate('data/images/Catster_idel.bmp', (0, 0, P_WIDTH, P_HEIGHT), 5, KEY_G, True, 38),
                       SpriteAnimate('data/images/Catster_run.bmp', (0, 0, P_WIDTH + 2, P_HEIGHT), 9, KEY_G, True, 4)]
        self.ani = 0

        self.StartPos = StartPos
        self.rect = pygame.Rect((self.StartPos), (P_WIDTH, P_HEIGHT))
        self.scroll = [0, 0]

        self.player_control = True
        self.setState(facing)

        # VFX
        self.VFX = []
        self.JumpVFX = False
        self.DropVFX = [False, 0]

        # RUN
        self.MaxVx = 3
        self.Vx = 0
        self.Ax = 0.5
        self.StopMulti = 1.5

        # JUMP
        self.MaxVy = 10
        self.Vy = 0
        self.VyJump = -9
        self.grav = 0.5
        self.JumpMovement = {"Ground_JUMP":True, "Air_JUMP":[0, 1]}
        self.AirMulti = 0.7
        self.VyAirJump = self.VyJump * self.AirMulti

        # SPECIAL
        self.MaxAirTime = 8
        self.AirTime = 0
        self.DashTime = 3
        self.MaxMomentumTime = 8
        self.momentumTime = 0
        self.AxDash = 5
        self.VyDash = -7
        self.StopDashX = 3
        self.StopDashY = 1

    def setState(self, facing):
        self.facing = facing
        self.moveR = False
        self.moveL = False
        self.moveUp = False
        self.run = False
        self.jump = False

        # MOVEMENT STATE
        self.dash = False
        self.dashUp = False
        self.climb = False
        self.keepMomentum = False
        self.RemainMomentum = False

    def updatePos(self, new_pos):
        self.StartPos = new_pos
        self.rect.move_ip(self.StartPos)

    def lockPos(self):
        self.rect.move_ip(self.rect.x, self.rect.y)

    def updateScroll(self, scroll):
        self.scroll = scroll

    def getPos(self):
        return self.rect.centerx

    def draw(self, screen):
        if self.run == True:
            self.ani = 1
        else:
            self.ani = 0

        now_x = self.rect.x - self.scroll[0]
        now_y = self.rect.y

        image = self.sprite[self.ani].next().convert()
        flip = pygame.transform.flip(image, True, False).convert()
        if self.run:
            if self.moveL:
                screen.blit(flip, (now_x, now_y))
            if self.moveR:
                screen.blit(image, (now_x, now_y))
        else:
            if self.facing == 0:
                screen.blit(flip, (now_x, now_y))
            if self.facing == 1:
                screen.blit(image, (now_x, now_y))

        # VFX
        if self.JumpVFX and self.JumpMovement["Air_JUMP"][0] < self.JumpMovement["Air_JUMP"][1]:
            self.VFX.append(VFX("dust", (now_x + P_WIDTH//2, now_y + P_HEIGHT), [0, 20], -1, [2, 3], 5))

        if self.DropVFX[0] and self.DropVFX[1] < 1:
            self.DropVFX[1] += 1
            self.VFX.append(VFX("dust", (now_x + P_WIDTH//2, now_y + P_HEIGHT), [-10, 30], 0, [3, 4], 4))

        for vfx in self.VFX:
            vfx_done = vfx.start(screen)

            if vfx_done == 1:
                self.VFX.remove(vfx)

    def control(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.moveUp = True
            if event.key == pygame.K_a:
                self.moveL = True
                self.run = not self.run
                self.facing = 0
            if event.key == pygame.K_d:
                self.moveR = True
                self.run = not self.run
                self.facing = 1
            if event.key == pygame.K_o:
                self.jump = True
                self.JumpVFX = True
            if event.key == pygame.K_p:
                self.dash = True
                if self.moveUp:
                    self.dashUp = True
                self.keepMomentum = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self.moveUp = False
            if event.key == pygame.K_a:
                self.moveL = False
                self.run = not self.run
            if event.key == pygame.K_d:
                self.moveR = False
                self.run = not self.run


    def movement(self, blocked_tiles, dt):
        movement = [0, 0]
        old_Vx = self.Vx
        old_Vy = self.Vy

        # MOMENTUM
        if self.run and not self.keepMomentum:
            if self.Vx <= -self.MaxVx:
                self.Vx = -self.MaxVx * deltatime(dt)
            if self.Vx >= self.MaxVx:
                self.Vx = self.MaxVx * deltatime(dt)

        if not self.dash and self.keepMomentum:
            if self.Vx < -self.MaxVx:
                self.Vx += self.StopDashX * deltatime(dt)
            if self.Vx > self.MaxVx:
                self.Vx -= self.StopDashX * deltatime(dt)
            if self.Vy < 0:
                self.Vy += self.StopDashY * deltatime(dt)
            if self.Vy > 0:
                self.Vy = 0

        # RUN
        if self.moveR == True:
            self.Vx += self.Ax * deltatime(dt)                
        if self.moveL == True:
            self.Vx -= self.Ax * deltatime(dt)

        if not self.run:
            if self.facing == 1:
                if self.Vx > 1:
                    self.Vx -= self.Ax * self.StopMulti * deltatime(dt)
                else:
                    self.Vx = 0
            if self.facing == 0:
                if self.Vx < -1:
                    self.Vx += self.Ax * self.StopMulti * deltatime(dt)
                else:
                    self.Vx = 0

        # JUMP
        if self.jump == True:
            if self.JumpMovement["Ground_JUMP"] is True:
                self.Vy = self.VyJump * deltatime(dt)
                self.JumpMovement["Ground_JUMP"] = False
            elif self.JumpMovement["Air_JUMP"][0] < self.JumpMovement["Air_JUMP"][1]:
                self.JumpMovement["Air_JUMP"][0] += 1
                self.Vy = self.VyAirJump * deltatime(dt)

            self.jump = False

        # DASH
        if self.dash == True:
            if self.dashUp:
                self.Vy = self.VyDash * deltatime(dt)
            else:
                self.Vy = 0
            if self.run:
                if self.moveR:
                    self.Vx += self.AxDash * deltatime(dt) 
                if self.moveL:
                    self.Vx -= self.AxDash * deltatime(dt)
            else:
                if self.facing == 1:
                    self.Vx += self.AxDash * deltatime(dt) 
                if self.facing == 0:
                    self.Vx -= self.AxDash * deltatime(dt)

        # MOVEMENT COLLISION
        if not self.dash:
            self.Vy += self.grav * deltatime(dt)
        if self.Vy >= self.MaxVy:
            self.Vy = self.MaxVy * deltatime(dt)
        movement[0] = (old_Vx + self.Vx) * 0.5 * deltatime(dt)
        movement[1] = (old_Vy + self.Vy) * 0.5 * deltatime(dt)
        self.rect, collision = move_collision(blocked_tiles, self.rect, movement)

        # RESET VAL
        if not collision["bottom"]:
            self.AirTime += 1
            self.JumpVFX = False
            self.DropVFX[0] = False
        
        if collision["bottom"]:
            self.Vy = 0
            self.AirTime = 0
            self.JumpMovement["Ground_JUMP"] = True
            self.JumpMovement["Air_JUMP"][0] = 0
            self.DropVFX[0] = True

        if collision["top"]:
            self.Vy = 0

        if self.AirTime >= self.MaxAirTime:
            self.JumpMovement["Ground_JUMP"] = False
            self.DropVFX[1] = 0

        if self.keepMomentum:
            self.momentumTime += 1

        if self.momentumTime >= self.DashTime:
            self.dash = False
            self.dashUp = False

        if self.momentumTime >= self.MaxMomentumTime:
            self.keepMomentum = False
            self.momentumTime = 0

        if self.rect.y > DISPLAY_SIZE[1]:
            self.rect.midbottom = self.StartPos
