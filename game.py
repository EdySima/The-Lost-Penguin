import pygame
import config
from random import randint
from music import music, sound_effect

from penguin import Penguin
from map import Map
from unit_move import UnitMove
from game_state import GameState
from bat import Bat
from weapon import Weapon

element = {
    'option_background': pygame.image.load('resources/gui/option/option_background.png'),
    'game_over': pygame.image.load('resources/gui/game_over/game_over.png'),
    'background': pygame.image.load('resources/gui/main_menu/background.png'),
    'start_button': pygame.image.load('resources/gui/main_menu/start_button.png'),
    'option_button': pygame.image.load('resources/gui/main_menu/option_button.png'),
    'quit_button': pygame.image.load('resources/gui/main_menu/quit_button.png'),
    'reset_button': pygame.image.load('resources/gui/game_over/reset_button.png'),
    'main_menu_button': pygame.image.load('resources/gui/game_over/main_menu_button.png'),
    'back_button': pygame.image.load('resources/gui/option/back_button.png'),
    'minus_button': pygame.image.load('resources/gui/option/minus_button.png'),
    'plus_button': pygame.image.load('resources/gui/option/plus_button.png')
}


class Game:
    def __init__(self, screen):
        pygame.font.init()
        self.screen = screen
        self.game_state = GameState.MAIN_MENU
        self.objects = []
        self.player = None
        self.enemy = None
        self.weapon = None
        self.map = None
        self.player_tiles = [0, 0, 0, 0]
        self.grid = False
        self.player_is_attacking = False
        self.count_time_attacking = 0
        self.score = 0
        self.is_playing_music = False
        self.music_volume = 0.5
        self.sound_effect_volume = 0.2
        self.click = False

    def set_up(self):
        self.play_music(music['main_world'])
        self.objects = []
        self.enemy = []
        self.player = Penguin(config.START_X * config.TILESIZE, config.START_Y * config.TILESIZE)
        self.weapon = Weapon(self.player)
        self.score = 0
        self.map = Map("main_world")
        self.game_state = GameState.RUNNING

    def update(self):

        if self.game_state == GameState.RUNNING:
            self.screen.fill(config.BLACK)
            self.player_manager()
            self.enemy_manager()
            self.draw()
            self.handle_events()
        if self.game_state == GameState.PLAYER_DEAD:
            self.game_over_screen()
        if self.game_state == GameState.MAIN_MENU:
            self.main_menu()
        if self.game_state == GameState.OPTION:
            self.option_screen()

    def play_music(self, string):
        self.is_playing_music = False
        pygame.mixer.music.unload()
        pygame.mixer.music.load(string)
        pygame.mixer.music.set_volume(self.music_volume)
        pygame.mixer.music.play(-1)

    def play_sound_effect(self, string):
        sound = pygame.mixer.Sound(string)
        sound.set_volume(self.sound_effect_volume)
        sound.play()

    def main_menu(self):
        if not self.is_playing_music:
            self.play_music(music['main_menu'])
            self.is_playing_music = True

        self.screen.blit(element['background'], (0, 0))
        mouse_x, mouse_y = pygame.mouse.get_pos()

        start_rect = pygame.Rect(70, 350, element['start_button'].get_width(), element['start_button'].get_height())
        option_rect = pygame.Rect(70, 470, element['option_button'].get_width(), element['option_button'].get_height())
        quit_rect = pygame.Rect(70, 590, element['quit_button'].get_width(), element['quit_button'].get_height())

        if start_rect.collidepoint((mouse_x, mouse_y)):
            self.play_sound_effect(sound_effect['button_hover'])
            start_rect = pygame.Rect(70, 350, start_rect[2] * 1.1, start_rect[3] * 1.1)
            self.screen.blit(pygame.transform.scale(element['start_button'], (start_rect[2], start_rect[3])), (70, 350))
            if self.click:
                self.game_state = GameState.RUNNING
                self.set_up()
        else:
            self.screen.blit(element['start_button'], (70, 350))

        if option_rect.collidepoint((mouse_x, mouse_y)):
            self.play_sound_effect(sound_effect['button_hover'])
            option_rect = pygame.Rect(70, 470, option_rect[2] * 1.1, option_rect[3] * 1.1)
            self.screen.blit(pygame.transform.scale(element['option_button'], (option_rect[2], option_rect[3])),
                             (70, 470))
            if self.click:
                self.game_state = GameState.OPTION
        else:
            self.screen.blit(element['option_button'], (70, 470))

        if quit_rect.collidepoint((mouse_x, mouse_y)):
            self.play_sound_effect(sound_effect['button_hover'])
            quit_rect = pygame.Rect(70, 590, quit_rect[2] * 1.1, quit_rect[3] * 1.1)
            self.screen.blit(pygame.transform.scale(element['quit_button'], (quit_rect[2], quit_rect[3])), (70, 590))
            if self.click:
                self.game_state = GameState.ENDING
        else:
            self.screen.blit(element['quit_button'], (70, 590))

        if not start_rect.collidepoint((mouse_x, mouse_y)) and not option_rect.collidepoint((mouse_x, mouse_y)) and not\
                quit_rect.collidepoint((mouse_x, mouse_y)):
            pygame.mixer.stop()

        if self.grid:
            pygame.draw.rect(self.screen, config.HITBOX_COLOR, start_rect, 1)
            pygame.draw.rect(self.screen, config.HITBOX_COLOR, option_rect, 1)
            pygame.draw.rect(self.screen, config.HITBOX_COLOR, quit_rect, 1)

        self.click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_state = GameState.ENDING
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.click = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    self.grid = not self.grid
                if event.key == pygame.K_F5:
                    self.game_state = GameState.RUNNING
                    self.set_up()

    def option_screen(self):
        self.screen.blit(element['option_background'], (0, 0))
        mouse_x, mouse_y = pygame.mouse.get_pos()
        music_volume = self.music_volume * 10
        sound_volume = self.sound_effect_volume * 10

        minus_sound_rect = pygame.Rect(861, 320, element['minus_button'].get_width(),
                                       element['minus_button'].get_height())
        minus_effect_rect = pygame.Rect(861, 460, element['minus_button'].get_width(),
                                        element['minus_button'].get_height())
        plus_sound_rect = pygame.Rect(980, 320, element['minus_button'].get_width(),
                                      element['minus_button'].get_height())
        plus_effect_rect = pygame.Rect(980, 460, element['minus_button'].get_width(),
                                       element['minus_button'].get_height())
        elem = (element['back_button'].get_width(), element['back_button'].get_height())
        back_rect = pygame.Rect(config.WIDTH / 2 - elem[0] / 2, config.HEIGHT - elem[1] - config.BACK_OFFSET[1],
                                elem[0], elem[1])

        option_font = pygame.font.SysFont(config.TEXT_FONT, config.OPTION_FONT_SIZE)
        text = option_font.render(str(int(music_volume)), False, config.WHITE)
        self.screen.blit(text, (930, 305))
        text = option_font.render(str(int(sound_volume)), False, config.WHITE)
        self.screen.blit(text, (930, 445))

        if minus_sound_rect.collidepoint((mouse_x, mouse_y)):
            minus_sound_rect = pygame.Rect(minus_sound_rect[0] - minus_sound_rect[2] * 0.15,
                                           minus_sound_rect[1] - minus_sound_rect[3] * 0.15,
                                           minus_sound_rect[2] * 1.3, minus_sound_rect[3] * 1.3)
            self.screen.blit(pygame.transform.scale(element['minus_button'],
                                                    (minus_sound_rect[2], minus_sound_rect[3])),
                             (minus_sound_rect[0], minus_sound_rect[1]))
            if self.click:
                if music_volume > 0:
                    music_volume -= 1
        else:
            self.screen.blit(element['minus_button'], (minus_sound_rect[0], minus_sound_rect[1]))

        if minus_effect_rect.collidepoint((mouse_x, mouse_y)):
            minus_effect_rect = pygame.Rect(minus_effect_rect[0] - minus_effect_rect[2] * 0.15,
                                            minus_effect_rect[1] - minus_effect_rect[3] * 0.15,
                                            minus_effect_rect[2] * 1.3,
                                            minus_effect_rect[3] * 1.3)
            self.screen.blit(pygame.transform.scale(element['minus_button'],
                                                    (minus_effect_rect[2], minus_effect_rect[3])),
                             (minus_effect_rect[0], minus_effect_rect[1]))

            if self.click:
                if sound_volume > 0:
                    sound_volume -= 1
        else:
            self.screen.blit(element['minus_button'], (minus_effect_rect[0], minus_effect_rect[1]))

        if plus_sound_rect.collidepoint((mouse_x, mouse_y)):
            plus_sound_rect = pygame.Rect(plus_sound_rect[0] - plus_sound_rect[2] * 0.15,
                                          plus_sound_rect[1] - plus_sound_rect[3] * 0.15,
                                          plus_sound_rect[2] * 1.3, plus_sound_rect[3] * 1.3)
            self.screen.blit(pygame.transform.scale(element['plus_button'],
                                                    (plus_sound_rect[2], plus_sound_rect[3])),
                             (plus_sound_rect[0], plus_sound_rect[1]))
            if self.click:
                if music_volume < 10:
                    music_volume += 1
        else:
            self.screen.blit(element['plus_button'], (plus_sound_rect[0], plus_sound_rect[1]))

        if plus_effect_rect.collidepoint((mouse_x, mouse_y)):
            plus_effect_rect = pygame.Rect(plus_effect_rect[0] - plus_effect_rect[2] * 0.15,
                                           plus_effect_rect[1] - plus_effect_rect[3] * 0.15,
                                           plus_effect_rect[2] * 1.3,
                                           plus_effect_rect[3] * 1.3)
            self.screen.blit(pygame.transform.scale(element['plus_button'],
                                                    (plus_effect_rect[2], plus_effect_rect[3])),
                             (plus_effect_rect[0], plus_effect_rect[1]))

            if self.click:
                if sound_volume < 10:
                    sound_volume += 1
        else:
            self.screen.blit(element['plus_button'], (plus_effect_rect[0], plus_effect_rect[1]))

        if back_rect.collidepoint((mouse_x, mouse_y)):
            self.play_sound_effect(sound_effect['button_hover'])
            back_rect = pygame.Rect(back_rect[0] - back_rect[2] * 0.05,
                                    back_rect[1] - back_rect[3] * 0.05,
                                    back_rect[2] * 1.1,
                                    back_rect[3] * 1.1)
            self.screen.blit(pygame.transform.scale(element['back_button'],
                                                    (back_rect[2], back_rect[3])),
                             (back_rect[0], back_rect[1]))
            if self.click:
                self.game_state = GameState.MAIN_MENU
        else:
            pygame.mixer.stop()
            self.screen.blit(element['back_button'], (back_rect[0], back_rect[1]))

        pygame.mixer.music.set_volume(music_volume / 10)
        self.music_volume = music_volume / 10
        self.sound_effect_volume = sound_volume / 10
        self.click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_state = GameState.ENDING
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.click = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_state = GameState.MAIN_MENU

    def game_over_screen(self):
        if not self.is_playing_music:
            self.play_music(music['game_over'])
            self.is_playing_music = True

        self.screen.blit(element['game_over'], (0, 0))
        mouse_x, mouse_y = pygame.mouse.get_pos()

        elem = (element['reset_button'].get_width(), element['reset_button'].get_height())
        reset_rect = pygame.Rect(config.WIDTH/2 - elem[0]/2, 375, elem[0], elem[1])
        elem = (element['main_menu_button'].get_width(), element['main_menu_button'].get_height())
        main_menu_rect = pygame.Rect(config.WIDTH/2 - elem[0]/2, 520, elem[0], elem[1])

        if reset_rect.collidepoint((mouse_x, mouse_y)):
            self.play_sound_effect(sound_effect['button_hover'])
            reset_rect = pygame.Rect(reset_rect[0] - reset_rect[2] * 0.05, reset_rect[1] - reset_rect[3] * 0.05,
                                     reset_rect[2] * 1.1, reset_rect[3] * 1.1)
            self.screen.blit(pygame.transform.scale(element['reset_button'], (reset_rect[2], reset_rect[3])),
                             (reset_rect[0], reset_rect[1]))
            if self.click:
                self.game_state = GameState.RUNNING
                self.set_up()
        else:
            self.screen.blit(element['reset_button'], (reset_rect[0], reset_rect[1]))

        if main_menu_rect.collidepoint((mouse_x, mouse_y)):
            self.play_sound_effect(sound_effect['button_hover'])
            main_menu_rect = pygame.Rect(main_menu_rect[0] - main_menu_rect[2] * 0.05,
                                         main_menu_rect[1] - main_menu_rect[3] * 0.05,
                                         main_menu_rect[2] * 1.1,
                                         main_menu_rect[3] * 1.1)
            self.screen.blit(pygame.transform.scale(element['main_menu_button'],
                                                    (main_menu_rect[2], main_menu_rect[3])),
                             (main_menu_rect[0], main_menu_rect[1]))

            if self.click:
                self.game_state = GameState.MAIN_MENU
                self.is_playing_music = False

        else:
            self.screen.blit(element['main_menu_button'], (main_menu_rect[0], main_menu_rect[1]))

        if not reset_rect.collidepoint((mouse_x, mouse_y)) and not main_menu_rect.collidepoint((mouse_x, mouse_y)):
            pygame.mixer.stop()

        self.click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_state = GameState.ENDING
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.click = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_state = GameState.MAIN_MENU
                    self.is_playing_music = False

    def spawn_enemy(self):
        map_width = self.map.get_width_map()
        map_height = self.map.get_height_map()
        y_poz = randint(1, map_height-2)
        x_poz = randint(1, map_width-2)
        if self.map.is_valid_position(x_poz, y_poz):
            enemy = Bat(x_poz * config.TILESIZE, y_poz * config.TILESIZE)
            self.enemy.append(enemy)
            self.objects.append(enemy)

    def draw(self):
        self.map.render_map(self.screen, self.player)
        if self.grid:
            self.draw_grid(self.map.get_camera())

        if self.player.get_direction() == UnitMove.UP:
            self.weapon.render(self.screen, self.map.get_camera(), self.grid, self.player_is_attacking)
            self.player.render(self.screen, self.map.get_camera(), self.grid)
        else:
            self.player.render(self.screen, self.map.get_camera(), self.grid)
            self.weapon.render(self.screen, self.map.get_camera(), self.grid, self.player_is_attacking)

        for obj in self.objects:
            obj.render(self.screen, self.map.get_camera(), self.grid)

        self.player.render_lifes(self.screen)
        self.draw_score()

    def draw_score(self):
        score_font = pygame.font.SysFont(config.TEXT_FONT, config.SCORE_FONT_SIZE)
        text = score_font.render(str(self.score), False, config.WHITE)
        self.screen.blit(text, config.SCORE_POSITION)

    def draw_grid(self, camera):
        map1 = self.map.get_background_map()
        for x in range(0, len(map1[0]) * config.TILESIZE, config.TILESIZE):
            pygame.draw.line(self.screen, config.WHITE, (x - camera[0], 0), (x - camera[0],
                                                                             len(map1) * config.TILESIZE))
        for y in range(0, len(map1) * config.TILESIZE, config.TILESIZE):
            pygame.draw.line(self.screen, config.WHITE, (0, y - camera[1]), (len(map1[0]) * config.TILESIZE,
                                                                             y - camera[1]))

    def check_tiles(self):
        hitbox = self.player.get_hitbox_corners()
        self.player_tiles[0] = self.map.get_tile_back_map(int(hitbox[0][1]//config.TILESIZE),
                                                          int(hitbox[0][0]//config.TILESIZE))
        self.player_tiles[1] = self.map.get_tile_back_map(int(hitbox[1][1]//config.TILESIZE),
                                                          int(hitbox[1][0]//config.TILESIZE))
        self.player_tiles[2] = self.map.get_tile_back_map(int(hitbox[2][1]//config.TILESIZE),
                                                          int(hitbox[2][0]//config.TILESIZE))
        self.player_tiles[3] = self.map.get_tile_back_map(int(hitbox[3][1]//config.TILESIZE),
                                                          int(hitbox[3][0]//config.TILESIZE))

    def player_manager(self):
        if 0 < self.count_time_attacking < config.TIME_ATTACKING:
            self.count_time_attacking += 1
        else:
            self.count_time_attacking = 0
            self.player_is_attacking = False

    def enemy_manager(self):
        for enemy in self.enemy:
            if enemy.contains_look(self.player):
                enemy.move_to_position(self.player.get_position())
                enemy.set_render_animation(enemy.get_attack_animation())
            else:
                enemy.move_to_position(enemy.get_start_position())
                enemy.set_render_animation(enemy.get_walk_animation())

            if enemy.contains(self.player):
                self.player.play_hit_sound(self.sound_effect_volume)
                player_life = self.player.get_lifes()
                if player_life != 0:
                    self.player.set_lifes(player_life - enemy.get_damage())

            if self.player_is_attacking:
                if self.contains(self.weapon, enemy):
                    enemy.play_hit_sound(self.sound_effect_volume)
                    self.enemy.remove(enemy)
                    self.objects.remove(enemy)
                    self.score += enemy.get_score()

    def contains(self, object1, object2):
        object1_hitbox = object1.get_hitbox()
        object2_hitbox = object2.get_hitbox()

        # Check object1 up left corner is in object2 hitbox
        if object1_hitbox[0] <= object2_hitbox[0] <= object1_hitbox[0] + object1_hitbox[2]:
            if object1_hitbox[1] <= object2_hitbox[1] <= object1_hitbox[1] + object1_hitbox[3]:
                return True

        # Check object1 up right corner is in object2 hitbox
        if object1_hitbox[0] <= object2_hitbox[0] <= object1_hitbox[0] + object1_hitbox[2]:
            if object1_hitbox[1] <= object2_hitbox[1] + object2_hitbox[3] <= object1_hitbox[1] + object1_hitbox[3]:
                return True

        # Check object1 down right corner is in object2 hitbox
        if object1_hitbox[0] <= object2_hitbox[0] + object2_hitbox[2] <= object1_hitbox[0] + object1_hitbox[2]:
            if object1_hitbox[1] <= object2_hitbox[1] + object2_hitbox[3] <= object1_hitbox[1] + object1_hitbox[3]:
                return True

        # Check object1 down left corner is in object2 hitbox
        if object1_hitbox[0] <= object2_hitbox[0] + object2_hitbox[2] <= object1_hitbox[0] + object1_hitbox[2]:
            if object1_hitbox[1] <= object2_hitbox[1] <= object1_hitbox[1] + object1_hitbox[3]:
                return True
        return False

    def handle_events(self):

        if self.player.get_lifes() == 0:
            self.game_state = GameState.PLAYER_DEAD
            print(self.is_playing_music)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_state = GameState.ENDING
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_state = GameState.MAIN_MENU
                if event.key == pygame.K_F1:
                    self.grid = not self.grid
                if event.key == pygame.K_F2:
                    players_lifes = self.player.get_lifes()
                    if players_lifes < config.PENGUIN_MAX_LIFE:
                        players_lifes += 1
                        self.player.set_lifes(players_lifes)
                if event.key == pygame.K_F3:
                    self.spawn_enemy()
                if event.key == pygame.K_F4:
                    self.set_up()
                if event.key == pygame.K_SPACE:
                    self.player_is_attacking = True
                    self.weapon.play_swing(self.sound_effect_volume)
                    self.count_time_attacking = 1

        self.check_tiles()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.player.update_position(UnitMove.UP, self.player_tiles)
            self.weapon.set_weapon(UnitMove.UP, self.player.get_position())
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.player.update_position(UnitMove.DOWN, self.player_tiles)
            self.weapon.set_weapon(UnitMove.DOWN, self.player.get_position())
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.player.update_position(UnitMove.RIGHT, self.player_tiles)
            self.weapon.set_weapon(UnitMove.RIGHT, self.player.get_position())
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.player.update_position(UnitMove.LEFT, self.player_tiles)
            self.weapon.set_weapon(UnitMove.LEFT, self.player.get_position())
        else:
            self.player.update_position(UnitMove.NONE, self.player_tiles)
