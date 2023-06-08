import pygame
from sys import exit
from random import randint, choice

pygame.init()

# Creating Game Window
screen = pygame.display.set_mode((800, 600))

# Caption and Icon
pygame.display.set_caption("NINJA ARROWMASTER")
iconImg = pygame.image.load('ninja.png')
pygame.display.set_icon(iconImg)

background = pygame.image.load('Assets/sky.png').convert()
ground = pygame.image.load('Assets/ground.png').convert()

# tutorial screen

text_font = pygame.font.Font('Assets/font_space_n.otf', 30)
tutorial_font = pygame.font.Font('Assets/ShortBaby-Mg2w.ttf', 40)
tutorial_text1 = tutorial_font.render('1) Use Space-bar to jump.', True, 32)
tutorial_text2 = tutorial_font.render('2) Use Right key to shoot the arrow.', True, 32)
return_button = pygame.image.load('Assets/return_button.png')
return_rect = return_button.get_rect(center=(400, 400))
return_text = text_font.render('RETURN', True, 32)
return_text_rect = return_text.get_rect(center=(400, 400))

# Score
score_var = 0
score_values_list = [0]
# score_max = 0
if len(score_values_list) > 3:
    score_values_list.remove(min(score_values_list))

score_font = pygame.font.Font('Assets/ShortBaby-Mg2w.ttf', 40)


def score_board():
    score_surf = score_font.render(f'Score:{score_var}', True, 32)
    screen.blit(score_surf, (370, 10))


# this is working just call in game_on = 1

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_1 = pygame.image.load('Game/Walking/pw_1.png').convert_alpha()
        player_2 = pygame.image.load('Game/Walking/pw_2.png').convert_alpha()
        player_3 = pygame.image.load('Game/Walking/pw_3.png').convert_alpha()
        player_4 = pygame.image.load('Game/Walking/pw_4.png').convert_alpha()
        player_5 = pygame.image.load('Game/Walking/pw_5.png').convert_alpha()
        player_6 = pygame.image.load('Game/Walking/pw_6.png').convert_alpha()
        player_7 = pygame.image.load('Game/Walking/pw_7.png').convert_alpha()
        player_8 = pygame.image.load('Game/Walking/pw_8.png').convert_alpha()

        self.player_walk = [player_1, player_2, player_3, player_4, player_5, player_6, player_7, player_8]
        self.player_walk_index = 0

        player_b1 = pygame.image.load('Game/Shooting/Bow4.png').convert_alpha()
        player_b2 = pygame.image.load('Game/Shooting/Bow5.png').convert_alpha()
        player_b3 = pygame.image.load('Game/Shooting/Bow6.png').convert_alpha()
        player_b4 = pygame.image.load('Game/Shooting/Bow7.png').convert_alpha()

        self.player_bow = [player_b1, player_b2, player_b3, player_b4]
        self.player_bow_index = 0

        self.jump = pygame.image.load('Game/Walking/pw_1.png').convert_alpha()
        self.image = self.player_walk[self.player_walk_index]

        self.rect = self.image.get_rect(midbottom=(100, 415))
        self.gravity = 0

        self.instantaneous_health = 200
        self.max_health = 1200
        self.health_bar_length = 300
        self.heath_bar_ratio = 4

    def player_jump(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and self.rect.bottom >= 415:
            self.gravity = -25

    def act_gravity(self):
        global arrow_pos_y
        self.gravity += 1
        self.rect.bottom += self.gravity
        arrow_pos_y = self.rect.centery

        if self.rect.bottom >= 415:
            self.rect.bottom = 415
            self.gravity = 0

    def player_anim(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_RIGHT]:
            self.player_bow_index += 0.1
            if self.player_bow_index >= len(self.player_bow):
                self.player_bow_index = 0
            self.image = self.player_bow[int(self.player_bow_index)]

        else:
            if self.rect.bottom < 300:
                self.image = self.jump

            else:
                self.player_walk_index += 0.1
                if self.player_walk_index >= len(self.player_walk):
                    self.player_walk_index = 0
                self.image = self.player_walk[int(self.player_walk_index)]

    def generate_arrow(self):

        return Arrow(self.rect.centerx, arrow_pos_y)

    # def score_board(self):
    #     score_font = pygame.font.Font('Assets/ShortBaby-Mg2w.ttf', 40)
    #     score_surf = score_font.render(f'Score: {score_var}', True, 32)
    #     screen.blit(score_surf, (370, 10))

    def health_decrease(self, amt):
        if self.instantaneous_health > 0:
            self.instantaneous_health -= amt
        if self.instantaneous_health < 0:
            self.instantaneous_health = 0
        pygame.display.update()

    def draw_health_bar(self):
        # colour, (x,y,width,height), margin width
        heart_img = pygame.image.load('Assets/heartImg.png').convert_alpha()
        heart_img_rect = heart_img.get_rect(topright=(30, 16))
        screen.blit(heart_img, heart_img_rect)
        pygame.draw.rect(screen, 'Red', (30, 20, self.health_bar_length, 15))
        pygame.draw.rect(screen, 'Green', (30, 20, self.instantaneous_health / self.heath_bar_ratio, 15))

    def update(self):
        global score_var
        global game_on
        global frames
        self.player_jump()
        self.act_gravity()
        self.player_anim()
        # self.score_board()
        self.draw_health_bar()
        if self.instantaneous_health == 0:
            # frames = 0
            score_values_list.append(score_var)
            self.instantaneous_health = 1200
            game_on = 3


player = Player()
player_group = pygame.sprite.GroupSingle()
player_group.add(Player())


class Arrow(pygame.sprite.Sprite):
    def __init__(self, arr_x, arr_y):
        super().__init__()
        self.image = pygame.image.load('Game/Shooting/arrowimg.png').convert_alpha()
        self.rect = self.image.get_rect(midleft=(arr_x, arr_y))

    def arrow_enemy_sky_hit(self):
        global score_var
        if enemy_sky.rect.collidepoint(self.rect.topright):
            score_var += 2

            if enemy_sky.rect.center == (655, 110):
                enemy_sky.rect.center = choice([(558, 265), (425, 170)])

            elif enemy_sky.rect.center == (558, 265):
                enemy_sky.rect.center = choice([(655, 110), (425, 170)])
            elif enemy_sky.rect.center == (425, 170):
                enemy_sky.rect.center = choice([(655, 110), (558, 265)])
            self.kill()
            light_ball.started_at = frames

    def arrow_enemy_ground_hit(self):
        global score_var
        l = []
        for r in enemy_ground_group.spritedict:
            if r.rect.collidepoint(self.rect.center):
                score_var += 1
                

                self.kill()
                l.append(r)
        for i in l:
            i.kill()

    def update(self):
        self.arrow_enemy_sky_hit()
        self.arrow_enemy_ground_hit()
        self.rect.left += 5

        if self.rect.left >= 1000:
            self.kill()


arrow_group = pygame.sprite.Group()


# arrow=Arrow(player.rect.centerx,player.rect.centery)

class EnemyGround(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        enemy_ground = pygame.image.load('Assets/enemy_fire.png').convert_alpha()

        self.image = enemy_ground
        self.rect = self.image.get_rect(midbottom=(randint(950, 1000), 415))

    def generate_fire_ball(self):

        return FireBall(self.rect.centerx, self.rect.centery)

    def ground_enemy_hit_player(self):
        for p in player_group.spritedict:
            if p.rect.collidepoint(self.rect.center):
                player.health_decrease(20)

    def update(self):
        self.rect.left -= 2
        if self.rect.right <= -50:
            self.kill()
        if (frames / 60) % 2 == 0:
            self.generate_fire_ball()


enemy_ground_group = pygame.sprite.Group()
fire_ball_group = pygame.sprite.Group()


class FireBall(pygame.sprite.Sprite):
    def __init__(self, ball_x, ball_y):
        super().__init__(fire_ball_group)
        fire_ball = pygame.image.load('Assets/fire_ball.png').convert_alpha()
        self.image = fire_ball
        self.rect = self.image.get_rect(center=(ball_x, ball_y))

    def fire_ball_hit_player(self):
        for p in player_group.spritedict:
            if p.rect.collidepoint(self.rect.midright):
                p.health_decrease(10)
                return True
            else:
                return False

    def update(self):
        self.rect.left -= 5
        self.fire_ball_hit_player()
        if self.rect.right <= 0:
            self.kill()
        elif self.fire_ball_hit_player():
            self.kill()


enemy_sky_group = pygame.sprite.Group()


class EnemySky(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(enemy_sky_group)
        self.image = pygame.image.load('Assets/enemy_thunder.png')
        self.rect = self.image.get_rect(center=choice([(655, 110), (558, 265), (425, 200)]))


enemy_sky = EnemySky()

light_ball_path_1 = [(630, 80), (629, 80), (628, 80), (626, 80), (625, 80), (623, 80), (622, 80), (620, 80), (615, 79),
                     (613, 79), (610, 78), (607, 78), (605, 78), (602, 78), (598, 78), (592, 78), (589, 78), (587, 78),
                     (586, 78), (583, 78), (578, 79), (574, 80), (567, 84), (563, 84), (557, 88), (554, 89), (551, 90),
                     (549, 92), (544, 95), (542, 96), (538, 98), (534, 101), (529, 103), (524, 106), (520, 109),
                     (512, 112), (507, 114), (501, 117), (496, 120), (493, 122), (489, 124), (483, 126), (479, 129),
                     (476, 130), (473, 132), (470, 135), (465, 137), (461, 140), (456, 143), (452, 144), (447, 147),
                     (445, 148), (443, 150), (441, 152), (438, 153), (436, 155), (433, 157), (427, 161), (425, 162),
                     (421, 165), (419, 167), (418, 168), (414, 170), (409, 175), (407, 177), (401, 183), (394, 188),
                     (388, 192), (378, 196), (376, 196), (371, 198), (371, 199), (368, 200), (366, 201), (364, 203),
                     (362, 205), (361, 207), (356, 212), (352, 215), (350, 216), (346, 219), (342, 221), (340, 223),
                     (337, 224), (333, 227), (329, 229), (326, 231), (322, 233), (319, 235), (317, 237), (315, 238),
                     (312, 240), (310, 241), (308, 242), (307, 244), (304, 246), (302, 248), (300, 251), (296, 254),
                     (292, 255), (289, 258), (284, 261), (282, 261), (281, 262), (278, 264), (277, 265), (275, 267),
                     (273, 268), (270, 270), (269, 272), (267, 273), (265, 274), (260, 277), (258, 279), (254, 281),
                     (250, 283), (248, 286), (246, 289), (243, 291), (242, 292), (240, 294), (238, 294), (234, 298),
                     (232, 299), (229, 301), (227, 303), (225, 305), (224, 306), (220, 309), (217, 312), (215, 313),
                     (213, 315), (207, 320), (206, 322), (201, 325), (198, 327), (196, 328), (194, 330), (192, 330),
                     (191, 332), (188, 334), (187, 335), (184, 337), (182, 339), (181, 340), (179, 341), (177, 342),
                     (174, 345), (173, 346), (171, 347), (169, 349), (168, 350), (166, 352), (165, 353), (164, 354),
                     (163, 355), (162, 355), (159, 357), (158, 359), (156, 360), (156, 361), (155, 362), (154, 363),
                     (153, 365), (150, 367), (149, 369), (147, 370), (146, 371), (143, 375), (143, 376), (141, 378),
                     (139, 381), (137, 383), (136, 385), (134, 387), (133, 389), (131, 391), (130, 393), (128, 394),
                     (127, 396)]
light_ball_path_2 = [(529, 243), (530, 243), (531, 242), (530, 242), (529, 242), (528, 242), (527, 241), (525, 241),
                     (524, 241), (522, 241), (521, 241), (520, 241), (518, 241), (517, 241), (515, 241), (513, 241),
                     (510, 241), (505, 241), (497, 241), (492, 241), (488, 241), (484, 240), (481, 240), (478, 240),
                     (473, 240), (467, 241), (463, 243), (457, 243), (452, 243), (449, 243), (446, 243), (444, 243),
                     (443, 243), (441, 244), (438, 245), (433, 245), (428, 247), (423, 247), (418, 248), (413, 250),
                     (410, 250), (406, 251), (402, 251), (397, 254), (392, 254), (389, 255), (385, 256), (380, 257),
                     (373, 258), (369, 258), (366, 259), (363, 259), (359, 262), (355, 263), (352, 264), (348, 265),
                     (345, 266), (342, 266), (336, 269), (332, 269), (326, 273), (318, 276), (309, 281), (298, 285),
                     (291, 287), (285, 290), (280, 290), (275, 292), (272, 292), (270, 293), (268, 294), (266, 296),
                     (259, 301), (253, 303), (250, 305), (247, 308), (244, 309), (241, 312), (237, 316), (233, 320),
                     (229, 325), (225, 327), (222, 329), (220, 330), (219, 331), (215, 333), (214, 334), (209, 337),
                     (204, 338), (199, 341), (195, 344), (191, 345), (189, 347), (187, 349), (186, 351), (183, 353),
                     (181, 357), (180, 361), (179, 363), (176, 364), (174, 365), (174, 366), (170, 368), (165, 370),
                     (163, 372), (159, 375), (154, 377), (150, 379), (140, 383), (130, 386), (125, 388), (114, 393),
                     (109, 396), (108, 398), (106, 399), (104, 400), (102, 402), (101, 403), (100, 404), (98, 406),
                     (96, 406), (95, 407), (94, 408), (93, 409), (92, 409)]
light_ball_path_3 = [(394, 143), (391, 145), (390, 146), (388, 147), (385, 150), (383, 150), (382, 150), (381, 150),
                     (380, 150), (379, 151), (378, 151), (372, 154), (371, 155), (371, 156), (370, 156), (367, 157),
                     (366, 157), (365, 157), (364, 158), (361, 160), (361, 160), (358, 164), (357, 165), (355, 166),
                     (353, 168), (351, 169), (349, 170), (348, 171), (346, 171), (345, 171), (343, 172), (341, 173),
                     (340, 174), (337, 176), (333, 179), (330, 181), (328, 182), (325, 182), (324, 185), (322, 186),
                     (320, 186), (316, 189), (316, 189), (308, 195), (301, 200), (298, 202), (294, 204), (292, 206),
                     (289, 207), (288, 208), (286, 209), (285, 210), (285, 211), (284, 212), (283, 212), (281, 214),
                     (280, 215), (276, 217), (275, 219), (273, 220), (271, 223), (269, 224), (267, 226), (264, 229),
                     (263, 231), (258, 235), (256, 237), (254, 239), (253, 240), (252, 244), (250, 247), (247, 249),
                     (246, 253), (245, 254), (242, 255), (240, 260), (238, 262), (236, 264), (236, 264), (235, 267),
                     (233, 270), (232, 271), (229, 273), (227, 275), (225, 277), (222, 281), (221, 281), (218, 284),
                     (215, 286), (210, 289), (208, 291), (206, 292), (200, 297), (197, 301), (192, 306), (190, 309),
                     (186, 312), (184, 313), (184, 314), (183, 315), (181, 317), (179, 319), (176, 321), (174, 325),
                     (171, 326), (169, 329), (168, 331), (165, 334), (164, 336), (161, 339), (161, 340), (158, 344),
                     (156, 346), (155, 346), (154, 348), (153, 349), (148, 354), (145, 358), (144, 360), (142, 361),
                     (139, 365), (138, 367), (136, 368), (135, 369), (133, 371), (132, 373), (130, 374), (128, 376),
                     (125, 380), (123, 382), (120, 384), (119, 386), (116, 388), (114, 391), (112, 393), (110, 394),
                     (109, 396), (108, 396), (107, 396), (106, 397), (105, 398), (105, 400), (104, 400), (103, 402),
                     (103, 404), (101, 405), (101, 407), (100, 408), (98, 410)]
light_ball_group = pygame.sprite.Group()

frames = 0


class LightBall(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__(light_ball_group)
        self.started_at = frames
        thunder_ball = pygame.image.load('Assets/thunder_ball.png').convert_alpha()
        self.image = thunder_ball
        self.rect = self.image.get_rect(center=(x, y))

    def light_ball_hit_player(self):
        for p in player_group.spritedict:
            if p.rect.collidepoint(self.rect.center):
                p.health_decrease(15)
                return True
            else:
                return False
                # continue

    def update(self):
        global frames
        self.light_ball_hit_player()
        if enemy_sky.rect.center == (655, 110):
            self.rect.center = light_ball_path_1[frames - self.started_at]
            if self.rect.centery == 396:
                self.rect.center = (630, 80)
                self.started_at = frames
            elif self.light_ball_hit_player():
                self.rect.center = (630, 80)
                self.started_at = frames
        elif enemy_sky.rect.center == (558, 265):
            self.rect.center = light_ball_path_2[frames - self.started_at]
            if self.rect.centery == 409:
                self.rect.center = (529, 243)
                self.started_at = frames
            elif self.light_ball_hit_player():
                self.rect.center = (529, 243)
                self.started_at = frames
        elif enemy_sky.rect.center == (425, 170):
            self.rect.center = light_ball_path_3[frames - self.started_at]
            if self.rect.centery == 410:
                self.rect.center = (394, 143)
                self.started_at = frames
            elif self.light_ball_hit_player():
                self.rect.center = (394, 143)
                self.started_at = frames


light_ball = LightBall(1000, 1000)

# clock and timers
clock = pygame.time.Clock()
arrow_shoot_delay_time = 800
time_at_last_shot = 0

# enemy ground timer
enemy_ground_timer = pygame.USEREVENT + 1

enemy_ground_timer_var = 8000
if 20 < score_var < 40:
    enemy_ground_timer_var = 6000
elif score_var >= 40:
    enemy_ground_timer_var = 5000
pygame.time.set_timer(enemy_ground_timer, enemy_ground_timer_var)

# Game State
game_on = 0

while True:
    # clock.tick(60)
    while game_on == 0:

        game_start_screen = pygame.image.load('Assets/sky.png').convert()
        game_font = pygame.font.Font('Assets/font_space.ttf', 60)
        text_font = pygame.font.Font('Assets/font_space_n.otf', 30)
        game_start_screen_text = game_font.render('NINJA ARROWMASTER', True, 60)
        game_start_screen_text_rect = game_start_screen_text.get_rect(midtop=(400, 40))
        green_button = pygame.image.load('Assets/Green_button.png').convert_alpha()
        green_button_text = text_font.render('PLAY', True, 32)
        green_button_text_rect = green_button_text.get_rect(center=(250, 250))
        green_rect = green_button.get_rect(center=(250, 250))
        red_button = pygame.image.load('Assets/Red_button.png').convert_alpha()
        red_button_text = text_font.render('TUTORIAL', True, 32)
        red_button_text_rect = red_button_text.get_rect(center=(550, 250))
        red_rect = red_button.get_rect(center=(550, 250))
        player_character = pygame.image.load('Assets/tile324.png')
        enemy_character = pygame.image.load('Assets/enemy_fire.png')

        screen.blit(game_start_screen, (0, 0))
        screen.blit(game_start_screen_text, game_start_screen_text_rect)
        screen.blit(ground, (0, 465))
        screen.blit(red_button, red_rect)
        screen.blit(green_button, green_rect)
        screen.blit(green_button_text, green_button_text_rect)
        screen.blit(red_button_text, red_button_text_rect)
        screen.blit(player_character, (200, 405))
        screen.blit(enemy_character, (400, 390))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                if green_rect.collidepoint(position):
                    game_on = 1
                if red_rect.collidepoint(position):
                    game_on = 2
                # if 175 < event.pos[0] < 325 and 226 < event.pos[1] < 274:
                #     game_on = 1
                # elif 475 < event.pos[0] < 625 and 226 < event.pos[1] < 274:
                #     game_on = 2
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_on = 1

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    if game_on == 1:
        # 60 fps (max)
        clock.tick(60)
        frames += 1
        screen.fill('red')
        screen.blit(background, (0, 0))
        screen.blit(ground, (0, 415))

        score_board()

        player_group.draw(screen)
        player_group.update()

        arrow_group.draw(screen)
        arrow_group.update()

        enemy_ground_group.draw(screen)
        enemy_ground_group.update()

        fire_ball_group.draw(screen)
        fire_ball_group.update()

        enemy_sky_group.draw(screen)
        enemy_sky_group.update()

        light_ball_group.draw(screen)
        light_ball_group.update()

        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            time_now = pygame.time.get_ticks()

            if time_now - time_at_last_shot >= arrow_shoot_delay_time:

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        arrow_group.add(player.generate_arrow())
                        time_at_last_shot = time_now

            if event.type == enemy_ground_timer:
                enemy_ground_group.add(EnemyGround())

        pygame.display.update()

    while game_on == 2:
        screen.blit(game_start_screen, (0, 0))
        screen.blit(game_start_screen_text, game_start_screen_text_rect)
        screen.blit(ground, (0, 465))
        screen.blit(tutorial_text1, (50, 200))
        screen.blit(tutorial_text2, (50, 300))
        screen.blit(return_button, return_rect)
        screen.blit(return_text, return_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                if return_rect.collidepoint(position):
                    game_on = 0

        pygame.display.update()

    while game_on == 3:
        game_over_surface_text = game_font.render('GAME OVER', True, 'Yellow', 40)
        game_over_surface_text_rect = game_over_surface_text.get_rect(midtop=(400, 100))
        your_score = score_font.render(f'Your Score:{score_var}', True, 32)
        your_score_rect = your_score.get_rect(topleft=(200, 250))
        high_score = score_font.render(f'High Score:{max(score_values_list)}', True, 32)
        high_score_rect = high_score.get_rect(topright=(600, 300))
        screen.blit(game_start_screen, (0, 0))
        screen.blit(game_start_screen_text, game_start_screen_text_rect)
        screen.blit(ground, (0, 465))
        screen.blit(game_over_surface_text, game_over_surface_text_rect)
        screen.blit(your_score, your_score_rect)
        screen.blit(high_score, high_score_rect)
        screen.blit(return_button, return_rect)
        screen.blit(return_text, return_text_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                # if 325 < event.pos[0] < 475 and 375 < event.pos[1] < 425:
                if return_rect.collidepoint(position):
                    score_var = 0
                    # frames = 0
                    # player.instantaneous_health = 1200
                    game_on = 0
                    pygame.display.update()

    pygame.display.update()
    pygame.display.flip()
