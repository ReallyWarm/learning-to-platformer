import math, pygame

def deltatime(dt):
    return dt / 1000 * 60 if dt > 16 else 1

def move_collision(blocked_tiles, rect, movement):
    collision = {"top":False, "bottom":False, "right":False, "left":False}
    rect.x += movement[0]
    for tile in blocked_tiles:
        if tile.rect.colliderect(rect):
            if movement[0] > 0:
                rect.right = tile.rect.left
                collision["right"] = True
            elif movement[0] < 0:
                rect.left = tile.rect.right
                collision["left"] = True

    rect.y += movement[1]
    for tile in blocked_tiles:
        if tile.rect.colliderect(rect):
            if movement[1] > 0:
                rect.bottom = tile.rect.top
                collision["bottom"] = True
            elif movement[1] < 0:
                rect.top = tile.rect.bottom
                collision["top"] = True

    return rect, collision

def scrollMap(TrueScroll, player, DisplaySize, P_WIDTH, X=True, Y=False):
    if X:
        TrueScroll[0] += (player.rect.centerx - TrueScroll[0] - DisplaySize[0]//2 - P_WIDTH//2) // 4
    if Y:
        TrueScroll[1] += (player.rect.centery - TrueScroll[1] - DisplaySize[1]//2 - P_WIDTH//2) // 4
    scroll = TrueScroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    return scroll