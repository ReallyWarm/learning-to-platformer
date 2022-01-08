import pygame, sys
from Managers import fps
from Engine import Level, Player
from constants import SKY, WINDOW_SIZE, DISPLAY_SIZE

pygame.init()
clock = pygame.time.Clock()

pygame.display.set_caption('Jump Game')
win = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
screen = pygame.Surface(DISPLAY_SIZE)

def DrawAll(screen):
    screen.fill(SKY)

    level.draw()
    player.draw(screen)

    win.blit(pygame.transform.scale(screen, WINDOW_SIZE), (0, 0))
    
level = Level(screen)
player = Player(level.start_pos(), facing=1)
level.new_player(player)

# delta time
dt = 0
current_fps = 0
last_frame = pygame.time.get_ticks()

run = 1
while run:
    dt = pygame.time.get_ticks() - last_frame
    last_frame = pygame.time.get_ticks()
    fps.get_time()

    level.update()
    player.movement(level.blocked_tiles(), dt)

    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            run = 0

        player.control(event)

    # current_fps = int(fps.get_framerate())
    DrawAll(screen)
    clock.tick(60)
    pygame.display.update()

pygame.quit()
sys.exit()