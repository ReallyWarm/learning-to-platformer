import pygame, json
from .tile import Tile
from .fieldobject import FieldObject
from Managers import scrollMap
from constants import DISPLAY_SIZE, P_WIDTH

class Level:
    def __init__(self, screen):
        self.screen = screen
        self.point = 0
        self.current_map = 1
        self.MaxWidth = [0, 0]
        self.load_level()

        self.player = None
        self.collected = [] # collected item
        self.TrueScroll = [0, 0] # float variable for scrolling map
        self.scroll = [0, 0] # int variable for scrolling map // use to make scrolling
        self.TrackScroll = True

        # Position to stop scrolling
        self.MaxPosScroll = [self.MaxWidth[0] + (DISPLAY_SIZE[0]//2), self.MaxWidth[1] - (DISPLAY_SIZE[0]//2)]
        self.MaxScroll = [self.MaxPosScroll[0] - DISPLAY_SIZE[0]//2, self.MaxPosScroll[1] - DISPLAY_SIZE[0]//2]

        self.sky = pygame.image.load('data/images/sky_edit.png').convert_alpha()
        self.pine = pygame.image.load('data/images/pine1.png').convert_alpha()

        # scene effect
        self.fade = False
        self.fade_time = [0, 20]

    def blocked_tiles(self):
        return self.main

    def start_pos(self):
        return self.player_pos

    def new_player(self, player):
        self.player = player

    def Scroll(self):
        last_scroll = self.scroll.copy()
        # Track player position
        if self.TrackScroll:
            self.scroll = scrollMap(last_scroll, self.player, DISPLAY_SIZE, P_WIDTH, True, False)

        # Leftmost of current map
        if self.player.rect.centerx - P_WIDTH//2 <= self.MaxPosScroll[0]:
            self.TrackScroll = False
            if self.scroll[0] > self.MaxScroll[0]:
                self.scroll[0] += (self.MaxScroll[0] - last_scroll[0]) // 8
            else:
                self.scroll[0] = self.MaxScroll[0]

        # Rightmost of current map
        elif self.player.rect.centerx - P_WIDTH//2 >= self.MaxPosScroll[1]:
            self.TrackScroll = False
            if self.scroll[0] < self.MaxScroll[1]:
                self.scroll[0] += (self.MaxScroll[1] - last_scroll[0]) // 8
            else:
                self.scroll[0] = self.MaxScroll[1]

        # Not at the leftmost and the rightmost of current map
        else:
            self.TrackScroll = True

        self.player.updateScroll(self.scroll)

    def update(self):
        player_pos = self.player.getPos()
        if player_pos >= self.MaxWidth[1]:
            self.fade = True
            self.current_map += 1
            self.load_level()
            self.player.updatePos(self.player_pos)

        if player_pos <= self.MaxWidth[0]:
            self.fade = True
            self.current_map -= 1
            self.load_level()
            self.player.updatePos(self.player_pos)

        if self.mapCoin:
            for coin in self.mapCoin:
                rm_coin = coin.checkCollision(self.player)

                if rm_coin is True:
                    self.collected.append([self.current_map, [coin.getId(), coin.getPos(), coin.getSize()]])
                    self.mapCoin.remove(coin)
                    self.point += 100
                    print(self.collected)


        self.Scroll()

    def draw(self):
        # Fade when level change
        if self.fade:
            self.player.lockPos()
            self.screen.fill((0,0,0))
            self.fade_time[0] += 1
            if self.fade_time[0] == self.fade_time[1]:
                self.fade = False
                self.fade_time[0] = 0
        else:
            self.screen.blit(self.sky, (0, 0))
            self.screen.blit(self.pine, (0, DISPLAY_SIZE[1] - self.pine.get_height() + 20))

            for tile in self.background:
                tile.updateScroll(self.scroll)
                tile.update(self.screen)
            for tile in self.main:
                tile.updateScroll(self.scroll)
                tile.update(self.screen)
            for tile in self.decor:
                tile.updateScroll(self.scroll)
                tile.update(self.screen)

            if self.mapCoin:
                for coin in self.mapCoin:
                    coin.updateScroll(self.scroll)
                    coin.update(self.screen)

    def load_level(self):
        if self.current_map < 10:
            map_num = "0" + str(self.current_map)
        else:
            map_num = str(self.current_map)
        filename = f'data/map/m{map_num}.json'

        with open(filename, 'r') as f:
            tile_data = json.load(f)
            f.close()

        self.background = []
        self.main = []
        self.decor = []
        self.player_pos = None
        self.mapCoin = []
        dontAdd = False

        if tile_data["background"]:
            for tile in tile_data["background"]:
                if tile[0] != 0:
                    background = Tile(tile[0], tile[1], tile[2])
                    self.background.append(background)

        if tile_data["main"]:
            for tile in tile_data["main"]:
                if tile[0] != 0:
                    if tile[0] == "P":
                        self.player_pos = tile[1]

                    elif tile[0] == "C":
                        if self.collected:
                            for collected in self.collected:
                                dontAdd = True if collected[0] == self.current_map and collected[1] == tile else False

                        if dontAdd is False:
                            self.mapCoin.append(FieldObject(tile[0], tile[1], tile[2]))

                    else:
                        main = Tile(tile[0], tile[1], tile[2])
                        self.main.append(main)
                        self.MaxWidth[0] = tile[1][0] if self.MaxWidth[0] > tile[1][0] else self.MaxWidth[0]
                        self.MaxWidth[1] = tile[1][0] + tile[2][0] if self.MaxWidth[1] < tile[1][0] + tile[2][0] else self.MaxWidth[1]

        if tile_data["decor"]:
            for tile in tile_data["decor"]:
                if tile[0] != 0:
                    decor = Tile(tile[0], tile[1], tile[2])
                    self.decor.append(decor)
