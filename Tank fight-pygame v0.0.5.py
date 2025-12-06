"""
A try of develop a game
by Charles
version: 0.0.5
NEW: fix some bugs
optimize fire shell, both player's and enemy's
now the shell is only one, not a curve
add volume function, so player can change the volume
add loading screen, though cannot see because the program loading is fast
"""
# Initializing
import pygame, sys, random, json
pygame.init()

# Level 1 to 5, from easy to hard
# the easier it is, the less accurate enemy shoots
try:
    with open('gamesetting.json', 'r+') as f:
        data = json.load(f)
        
except FileNotFoundError:
    data = {'hard_level' : 2, 'volume' : 20}
    with open('gamesetting.json', 'w+') as f:
        json.dump(data, f)

hard_level = data['hard_level']
volume = data['volume']

# Settings
"""
img_origin = pygame.image.load('xxx')
icon = pygame.image.load('xxx')
pygame.display.set_icon(icon)
"""
W, H = 800, 600
window = pygame.display.set_mode((W, H))
pygame.display.set_caption('Tank Fight')
clock = pygame.time.Clock()
FPS = 60
ground_h = 20
fire_sound = pygame.mixer.Sound('发射.wav')
explode_sound = pygame.mixer.Sound('爆炸.mp3')
fire_sound.set_volume(round(volume / 100, 1))
explode_sound.set_volume(round(volume / 100, 1))


# Tank settings
tank_h = 20
tank_w = 40
turret_w = 5
wheel_w = 5
turret_mode_max = 14
tankOrigin_x = 0.9 * W
tankOrigin_y = H - ground_h - tank_h - wheel_w


# Colors
green = (0, 255, 0)
dark_green = (34, 177, 76)
blue = (0, 0, 255)
red = (255, 0, 0)
dark_red = (170, 0, 0)
yellow = (200, 200, 0)
light_yellow = (255, 255, 0)
black = (0, 0, 0)
white = (255, 255, 255)
grey = (130, 130, 130)


# Using font from system
font_small = pygame.font.SysFont("comicsansms", 20)
font_medium = pygame.font.SysFont("comicsansms", 30)
font_big = pygame.font.SysFont("comicsansms", 55)


"""
####################
####################
Game basic functions
####################
####################
"""


def message_to_screen(msg, color, y=0, size='medium', x=0):
    if size == 'big':
        text = font_big.render(msg, True, color)
    elif size == 'medium':
        text = font_medium.render(msg, True, color)
    elif size == 'small':
        text = font_small.render(msg, True, color)

    text_wide, text_height = text.get_size()
    window.blit(text, ((W / 2 - text_wide / 2) + x, H / 2 - text_height / 2 - y))


# loading screen
window.fill('white')
message_to_screen('loading...', white)
pygame.display.update()


def close(a=0):
    pygame.quit()
    sys.exit(a)


def button(color, bx, by, bw, bh, text, action=None):
    pygame.draw.rect(window, color, (bx - 0.5 * bw, by - 0.5 * bh, bw, bh))
    text1 = font_small.render(text, True, black)
    tw, th = text1.get_size()
    tx = bx - 0.5 * tw
    ty = by - 0.5 * th
    window.blit(text1, (tx, ty))
    if action == 'Start':
        game_loop()
    elif action == 'Controls':
        game_controls()
    elif action == 'Quit':
        pygame.quit()
        sys.exit()
    elif action == 'Manu':
        game_intro()

    pygame.display.update()


def button_check(button_x, button_y, button_w, button_h, mx, my):
    check_x1 = button_x - button_w / 2
    check_x2 = button_x + button_w / 2
    check_y1 = button_y - button_h / 2
    check_y2 = button_y + button_h / 2
    if check_x1 <= mx <= check_x2 and check_y1 <= my <= check_y2:
        return True
    else:
        return False


def game_intro():
    intro = True
    window.fill(white)
    bottum_x1 = W / 4
    bottum_x2 = W / 2
    bottum_x3 = 3*W / 4
    bottum_y = 500
    bottum_w = 100
    bottum_h = 50
    message_to_screen('Welcome to Tank Fight!', green, 200, 'big')
    message_to_screen('You and your enemy will fire one by one!', black, 120, 'medium')
    message_to_screen('Being destroyed will lose the game!', black, 70, 'medium')
    message_to_screen('Beat your enemy!', black, 20, 'medium')
    button(dark_green, bottum_x1, bottum_y, bottum_w, bottum_h, "Start")
    button(yellow, bottum_x2, bottum_y, bottum_w, bottum_h, "Controls")
    button(dark_red, bottum_x3, bottum_y, bottum_w, bottum_h, "Quit")
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()

            mx, my = pygame.mouse.get_pos()
            #Start
            if button_check(bottum_x1, bottum_y, bottum_w, bottum_h, mx, my):
                button(green, bottum_x1, bottum_y, bottum_w, bottum_h, "Start")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    button(green, bottum_x1, bottum_y, bottum_w, bottum_h, "Start", 'Start')
            else:
                button(dark_green, bottum_x1, bottum_y, bottum_w, bottum_h, "Start")
            #Controls
            if button_check(bottum_x2, bottum_y, bottum_w, bottum_h, mx, my):
                button(light_yellow, bottum_x2, bottum_y, bottum_w, bottum_h, "Controls")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    button(light_yellow, bottum_x2, bottum_y, bottum_w, bottum_h, "Controls", 'Controls')
            else:
                button(yellow, bottum_x2, bottum_y, bottum_w, bottum_h, "Controls")
            #Quit
            if button_check(bottum_x3, bottum_y, bottum_w, bottum_h, mx, my):
                button(red, bottum_x3, bottum_y, bottum_w, bottum_h, "Quit")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    button(red, bottum_x3, bottum_y, bottum_w, bottum_h, "Quit", 'Quit')
            else:
                button(dark_red, bottum_x3, bottum_y, bottum_w, bottum_h, "Quit")

            pygame.display.update()

        clock.tick(30)


def game_over(p_score):
    gameOver = True
    window.fill(white)
    bottum_x1 = W / 4
    bottum_x2 = W / 2
    bottum_x3 = 3*W / 4
    bottum_y = 500
    bottum_w = 100
    bottum_h = 50
    message_to_screen('Game over!', green, 200, 'big')
    message_to_screen('You died!', black, 120, 'medium')
    message_to_screen('Try again!', black, 20, 'medium')
    message_to_screen('Your score:' + str(p_score), black, 70, 'medium')
    button(dark_green, bottum_x1, bottum_y, bottum_w, bottum_h, "Try again")
    button(yellow, bottum_x2, bottum_y, bottum_w, bottum_h, "Controls")
    button(dark_red, bottum_x3, bottum_y, bottum_w, bottum_h, "Quit")
    while gameOver:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()

            mx, my = pygame.mouse.get_pos()
            #Start
            if button_check(bottum_x1, bottum_y, bottum_w, bottum_h, mx, my):
                button(green, bottum_x1, bottum_y, bottum_w, bottum_h, "Try again")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    button(green, bottum_x1, bottum_y, bottum_w, bottum_h, "Try again", 'Start')
            else:
                button(dark_green, bottum_x1, bottum_y, bottum_w, bottum_h, "Try again")
            #Controls
            if button_check(bottum_x2, bottum_y, bottum_w, bottum_h, mx, my):
                button(light_yellow, bottum_x2, bottum_y, bottum_w, bottum_h, "Controls")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    button(light_yellow, bottum_x2, bottum_y, bottum_w, bottum_h, "Controls", 'Controls')
            else:
                button(yellow, bottum_x2, bottum_y, bottum_w, bottum_h, "Controls")
            #Quit
            if button_check(bottum_x3, bottum_y, bottum_w, bottum_h, mx, my):
                button(red, bottum_x3, bottum_y, bottum_w, bottum_h, "Quit")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    button(red, bottum_x3, bottum_y, bottum_w, bottum_h, "Quit", 'Quit')
            else:
                button(dark_red, bottum_x3, bottum_y, bottum_w, bottum_h, "Quit")

            pygame.display.update()

        clock.tick(30)


def win(p_score):
    Win = True
    window.fill(white)
    bottum_x1 = W / 4
    bottum_x2 = W / 2
    bottum_x3 = 3*W / 4
    bottum_y = 500
    bottum_w = 100
    bottum_h = 50
    message_to_screen('You win!', green, 200, 'big')
    message_to_screen('Congradulations!', black, 120, 'medium')
    message_to_screen('Your score:' + str(p_score), black, 70, 'medium')
    button(dark_green, bottum_x1, bottum_y, bottum_w, bottum_h, "Play again")
    button(yellow, bottum_x2, bottum_y, bottum_w, bottum_h, "Controls")
    button(dark_red, bottum_x3, bottum_y, bottum_w, bottum_h, "Quit")
    while Win:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()

            mx, my = pygame.mouse.get_pos()
            #Start
            if button_check(bottum_x1, bottum_y, bottum_w, bottum_h, mx, my):
                button(green, bottum_x1, bottum_y, bottum_w, bottum_h, "Play again")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    button(green, bottum_x1, bottum_y, bottum_w, bottum_h, "Play again", 'Start')
            else:
                button(dark_green, bottum_x1, bottum_y, bottum_w, bottum_h, "Play again")
            #Controls
            if button_check(bottum_x2, bottum_y, bottum_w, bottum_h, mx, my):
                button(light_yellow, bottum_x2, bottum_y, bottum_w, bottum_h, "Controls")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    button(light_yellow, bottum_x2, bottum_y, bottum_w, bottum_h, "Controls", 'Controls')
            else:
                button(yellow, bottum_x2, bottum_y, bottum_w, bottum_h, "Controls")
            #Quit
            if button_check(bottum_x3, bottum_y, bottum_w, bottum_h, mx, my):
                button(red, bottum_x3, bottum_y, bottum_w, bottum_h, "Quit")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    button(red, bottum_x3, bottum_y, bottum_w, bottum_h, "Quit", 'Quit')
            else:
                button(dark_red, bottum_x3, bottum_y, bottum_w, bottum_h, "Quit")

            pygame.display.update()

        clock.tick(30)


def game_controls():
    with open('gamesetting.json', 'r+') as f:
        data = json.load(f)
        hardLevel = data['hard_level']
        volume = data['volume']

    gcon = True
    window.fill(white)
    bottum_x2 = W / 2
    bottum_y = 500
    bottum_w = 100
    bottum_h = 50
    def show():
        message_to_screen('Game controls', green, 250, 'big')
        message_to_screen('Pause:"escape"', black, 170, 'medium')
        message_to_screen('Fire:"space"', black, 120, 'medium')
        message_to_screen('Move tank: left and right arrows', black, 70, 'medium')
        message_to_screen('Move turret: ad', black, 20, 'medium')
        message_to_screen('Power control: ws', black, -30, 'medium')
        message_to_screen('Author: Charlse', grey, -260, 'small')

    show()
    button(light_yellow, bottum_x2, bottum_y, bottum_w, bottum_h, "Manu")
    hard_level_text = font_medium.render('Hard level: ' + str(hardLevel) + '    up and down arrows',
                                         True, black)
    hard_level_text_wide, hard_level_text_height = hard_level_text.get_size()
    window.blit(hard_level_text, (W / 2 - hard_level_text_wide / 2,
                                  (hard_level_text_height / 2) + H / 2 + 30))
    volume_text = font_medium.render('volume: ' + str(volume) + '    "w" and "s"',
                                     True, black)
    volume_text_wide, volume_text_height = volume_text.get_size()
    window.blit(volume_text, (W / 2 - volume_text_wide / 2,
                                  (volume_text_height / 2) + H / 2 + 80))
    pygame.display.update()
    while gcon:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                data = {'hard_level' : hard_level, 'volume' : volume}
                with open('gamesetting.json', 'w+') as f:
                    json.dump(data, f)

                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and not hardLevel >= 5:
                    hardLevel += 1
                elif event.key == pygame.K_DOWN and not hardLevel <= 1:
                    hardLevel -= 1
                if event.key == pygame.K_w and not volume >= 100:
                    volume += 10
                if event.key == pygame.K_s and not volume <= 0:
                    volume -= 10

                window.fill(white)
                hard_level_text = font_medium.render('Hard level: ' + str(hardLevel) + '    up and down arrows',
                                                     True, black)
                hard_level_text_wide, hard_level_text_height = hard_level_text.get_size()
                window.blit(hard_level_text, (W / 2 - hard_level_text_wide / 2,
                                              (hard_level_text_height / 2) + H / 2 + 30))
                volume_text = font_medium.render('volume: ' + str(volume) + '    "w" and "s"',
                                                 True, black)
                volume_text_wide, volume_text_height = volume_text.get_size()
                window.blit(volume_text, (W / 2 - volume_text_wide / 2,
                                          (volume_text_height / 2) + H / 2 + 80))
                show()
                pygame.display.update()

            mx, my = pygame.mouse.get_pos()
            # Manu
            if button_check(bottum_x2, bottum_y, bottum_w, bottum_h, mx, my):
                button(light_yellow, bottum_x2, bottum_y, bottum_w, bottum_h, "Manu")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    data = {'hard_level' : hardLevel, 'volume' : volume}
                    with open('gamesetting.json', 'w+') as f:
                        json.dump(data, f)

                    button(light_yellow, bottum_x2, bottum_y, bottum_w, bottum_h, "Manu", 'Manu')

                pygame.display.update()

            else:
                button(yellow, bottum_x2, bottum_y, bottum_w, bottum_h, "Manu")
                pygame.display.update()

        clock.tick(FPS)


def pause():
    Pause = True
    message_to_screen('Pause', (0, 0, 0), 25, 'big')
    message_to_screen('"q"to quit, "c"to continue, "r" to restart', 'grey', -40, 'small')
    pygame.display.update()
    while Pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    close()
                elif event.key == pygame.K_c or event.key == pygame.K_ESCAPE:
                    Pause = False
                elif event.key == pygame.K_r:
                    game_loop()


        clock.tick(FPS)


def score(score):
    score_text = font_small.render('Score:' + str(score), True, black)
    score_text_wide, score_text_height = score_text.get_size()
    window.blit(score_text, (W / 2 - score_text_wide / 2, (score_text_height / 2) + 20))


def barrier(x, h, w):
    pygame.draw.rect(window, black, [x, H - h, w, h])


"""
#####################
#####################
Tanks
#####################
#####################
"""


def tank(x, y, turret_mode = 4):
    x = int(x)
    y = int(y)
    # main part of tank
    pygame.draw.circle(window, black, (x, y), int(tank_h / 2))
    pygame.draw.rect(window, grey, (x - tank_h, y, tank_w, tank_h))
    # possible turret position
    turret_endpos = [(x-27, y-2),
                     (x-26.5, y-3.5), 
                     (x-26, y-5),
                     (x-25.5, y-6.5),
                     (x-25, y-8),
                     (x-24.5, y-9),
                     (x-24, y-10),
                     (x-23.5, y-11),
                     (x-23, y-12),
                     (x-22.5, y-12.5),
                     (x-22, y-13),
                     (x-21, y-13.5),
                     (x-19, y-14.5),
                     (x-17, y-15),
                     (x-15, y-15.5),
                     ]
    pygame.draw.line(window, black, (x, y), turret_endpos[turret_mode], turret_w)
    # wheels
    for x1 in range(0, 31, 5):
        pygame.draw.circle(window, black, (x1 - 15 + x, y + 20), wheel_w)

    return turret_endpos[turret_mode]


def enemy_tank(x, y, turret_mode = turret_mode_max):
    x = int(x)
    y = int(y)
    pygame.draw.circle(window, black, (x, y), int(tank_h / 2))
    pygame.draw.rect(window, grey, (x - tank_h, y, tank_w, tank_h))
    turret_endpos = [(x + 27, y - 2),
                     (x + 26.5, y - 3.5),
                     (x + 26, y - 5),
                     (x + 25.5, y - 6.5),
                     (x + 25, y - 8),
                     (x + 24.5, y - 9),
                     (x + 24, y - 10),
                     (x + 23.5, y - 11),
                     (x + 23, y - 12),
                     (x + 22.5, y - 12.5),
                     (x + 22, y - 13),
                     (x + 21, y - 13.5),
                     (x + 19, y - 14.5),
                     (x + 17, y - 15),
                     (x + 15, y - 15.5),
                     ]
    pygame.draw.line(window, black, (x, y), turret_endpos[turret_mode], turret_w)
    for x1 in range(0, 31, 5):
        pygame.draw.circle(window, black, (x1 - 15 + x, y + 20), wheel_w)

    return turret_endpos[turret_mode]


def fireShell(xy, tankx, tanky, tur_Pos, power_level, barrier_x, barrier_y,
              barrier_h, barrier_w, e_tank_x, e_tank_y, p_h, e_h, Score):
    pygame.mixer.Sound.play(fire_sound)
    fire = True
    damage = 0
    startingShell = list(xy)
    def show(p_h, e_h, Score, power_level, barrier_x, barrier_y, barrier_w):
        window.fill(white)
        health_bars(p_h, e_h)
        score(Score)
        power(power_level)
        barrier(barrier_x, H - barrier_y, barrier_w)
        pygame.draw.rect(window, green, (0, H - ground_h, W, ground_h))


    while fire:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause()

        show(p_h, e_h, Score, power_level, barrier_x, barrier_y, barrier_w)
        turPos = tank(tankx, tanky, tur_Pos)
        enemy_turPos = enemy_tank(e_tank_x, e_tank_y, turret_mode_max)
        # 轨迹
        pygame.draw.circle(window, blue, (startingShell[0], startingShell[1]), 5)
        pygame.display.update()
        # 每个点的x坐标间隔取决于炮管发射角度，并且随着飞行越来越密
        # 乘数越大，最高点越小
        startingShell[0] -= (turret_mode_max +1 - tur_Pos) * 15
        # y=x**2     相对于炮管的x坐标的平方。炮管角度越高，曲线越高
        # 第一个乘数代表整体大小
        startingShell[1] += 10*((((startingShell[0]) - xy[0])*0.01 / (power_level / 100))**2 - (
                tur_Pos+tur_Pos/(turret_mode_max + 1 - tur_Pos)))*0.1
        # Check whether hit the barrier
        check_x_1 = startingShell[0] <= barrier_x + barrier_w
        check_x_2 = startingShell[0] >= barrier_x
        check_y_1 = startingShell[1] <= H - ground_h
        check_y_2 = startingShell[1] >= barrier_y
        if startingShell[1] > H - ground_h:
            show(p_h, e_h, Score, power_level, barrier_x, barrier_y, barrier_w)
            turPos = tank(tankx, tanky, tur_Pos)
            enemy_turPos = enemy_tank(e_tank_x, e_tank_y, turret_mode_max)
            pygame.display.update()
            hit_x = startingShell[0] * H / startingShell[1]
            hit_y = H - ground_h
            explosion(hit_x, hit_y, 40)
            fire = False
            if e_tank_x + 15 > hit_x > e_tank_x - 15:
                damage = 20
        elif check_x_1 and check_x_2 and check_y_1 and check_y_2:
            show(p_h, e_h, Score, power_level, barrier_x, barrier_y, barrier_w)
            turPos = tank(tankx, tanky, tur_Pos)
            enemy_turPos = enemy_tank(e_tank_x, e_tank_y, turret_mode_max)
            pygame.display.update()
            hit_x = startingShell[0]
            hit_y = startingShell[1]
            explosion(hit_x, hit_y, 40)
            fire = False

        clock.tick(FPS)

    return damage


def e_fireShell(xy, tankx, tanky, tur_Pos, power_level, barrier_x, barrier_y,
                barrier_h, barrier_w, player_x, player_y, p_h, e_h, Score, hardLevel):
    damage = 0
    currentPower = 0
    power_found = False
    # find the proper power to hit the target
    while not power_found:
        currentPower += 2
        if currentPower > 100:
            power_found = True
        fire = True
        startingShell = list(xy)
        while fire:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pause()

            startingShell[0] += ((turret_mode_max +1  - tur_Pos) * 15)
            startingShell[1] += (10*(((startingShell[0] - xy[0])*0.01 / (currentPower / 100))**2 - (
                    tur_Pos+tur_Pos/(turret_mode_max + 1 - tur_Pos)))*0.1)
            check_x_1 = startingShell[0] <= barrier_x + barrier_w
            check_x_2 = startingShell[0] >= barrier_x
            check_y_1 = startingShell[1] <= H - ground_h
            check_y_2 = startingShell[1] >= barrier_y
            if startingShell[1] > H - ground_h:
                hit_x = startingShell[0] * H / startingShell[1]
                hit_y = H - ground_h
                if player_x + 15 > hit_x > player_x - 15:
                    power_found = True
                fire = False
            elif check_x_1 and check_x_2 and check_y_1 and check_y_2:
                hit_x = startingShell[0]
                hit_y = startingShell[1]
                fire = False


    # fire to the target
    pygame.mixer.Sound.play(fire_sound)
    fire = True
    startingShell = list(xy)
    gun_power = random.randrange(int(currentPower * (0.7 + hardLevel / 20)),
                                 int(currentPower * (1.3 - hardLevel / 20)))
    def show(barrier_x, barrier_y, barrier_w, ground_h, p_h, e_h, power_level, Score):
        window.fill(white)
        barrier(barrier_x, H - barrier_y, barrier_w)
        pygame.draw.rect(window, green, (0, H - ground_h, W, ground_h))
        health_bars(p_h, e_h)
        power(power_level)
        score(Score)


    while fire:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause()

        show(barrier_x, barrier_y, barrier_w, ground_h, p_h, e_h, power_level, Score)
        pygame.draw.circle(window, blue, (startingShell[0], startingShell[1]), 5)
        turPos = tank(player_x, player_y, tur_Pos)
        enemy_turPos = enemy_tank(tankx, tanky, turret_mode_max)
        pygame.display.update()

        startingShell[0] += ((turret_mode_max + 1 - tur_Pos) * 15)
        startingShell[1] += (10 * (((startingShell[0] - xy[0]) * 0.01 / (gun_power / 100)) ** 2 - (
                    tur_Pos + tur_Pos / (turret_mode_max + 1 - tur_Pos))) * 0.1)
        check_x_1 = startingShell[0] <= barrier_x + barrier_w
        check_x_2 = startingShell[0] >= barrier_x
        check_y_1 = startingShell[1] <= H - ground_h
        check_y_2 = startingShell[1] >= barrier_y
        if startingShell[1] > H - ground_h:
            show(barrier_x, barrier_y, barrier_w, ground_h, p_h, e_h, power_level, Score)
            turPos = tank(player_x, player_y, tur_Pos)
            enemy_turPos = enemy_tank(tankx, tanky, turret_mode_max)
            pygame.display.update()
            hit_x = startingShell[0] * H / startingShell[1]
            hit_y = H - ground_h
            fire = False
            if player_x + 15 > hit_x > player_x - 15:
                damage = 20
                explosion(hit_x, hit_y, 40)
            else:
                explosion(hit_x, hit_y, 40)
        elif check_x_1 and check_x_2 and check_y_1 and check_y_2:
            show(barrier_x, barrier_y, barrier_w, ground_h, p_h, e_h, power_level, Score)
            turPos = tank(player_x, player_y, tur_Pos)
            enemy_turPos = enemy_tank(tankx, tanky, turret_mode_max)
            pygame.display.update()
            hit_x = startingShell[0]
            hit_y = startingShell[1]
            explosion(hit_x, hit_y, 40)
            fire = False

        clock.tick(FPS)

    return damage


def explosion(x, y, size):
    pygame.mixer.Sound.play(explode_sound)
    explode = True
    while explode:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause()

        # explode
        startPoint = x, y
        colorChoices = [red, dark_red, yellow, light_yellow]
        magnitude = 1
        while magnitude < size:
            explode_bit_x = x + random.randrange(-1 * magnitude, magnitude)
            explode_bit_y = y + random.randrange(-1 * magnitude, magnitude)
            pygame.draw.circle(window, colorChoices[random.randrange(0, 4)],
                               (explode_bit_x, explode_bit_y), random.randrange(1, 3))
            magnitude += 1
            pygame.display.update()
            clock.tick(120)

        explode = False



def power(level):
    message_to_screen('Power: ' + str(level) + '%', black, H / 2 - 20, 'small')


def health_bars(player_health, enemy_health):
    if player_health >= 75:
        player_color = green
    elif player_health >= 50:
        player_color = yellow
    else:
        player_color = red

    if enemy_health >= 75:
        enemy_color = green
    elif enemy_health >= 50:
        enemy_color = yellow
    else:
        enemy_color = red

    pygame.draw.rect(window, player_color, (W - 120, 25, player_health, 25))
    pygame.draw.rect(window, enemy_color, (20, 25, enemy_health, 25))
    ph_text = font_small.render(str(player_health), True, black)
    eh_text = font_small.render(str(enemy_health), True, black)
    ph_text_w, ph_text_h = ph_text.get_size()
    eh_text_w, eh_text_h = eh_text.get_size()
    window.blit(eh_text, (20 + enemy_health / 2 - eh_text_w / 2, 25))
    window.blit(ph_text, (W - 120 + player_health / 2 - ph_text_w / 2, 25))


"""
###################
###################
Game loop
###################
###################
"""


def game_loop():
    window.fill('white')
    tank_x = tankOrigin_x
    tank_y = tankOrigin_y
    turret_mode = 4
    enemy_tank_x = 0.1*W
    enemy_tank_y = tankOrigin_y
    fire_power = 50
    damage = 0
    barrier_w = 50
    barrier_x = W / 2 + random.randint(int(-0.15*W), int(0.15*W))
    barrier_h = random.randrange(int(0.1*H), int(0.4*H))
    with open('gamesetting.json', 'r+') as f:
        data = json.load(f)
        hard_level = data['hard_level']
        volume = data['volume']

    player_health = 100
    enemy_health = 100
    player_score = 0
    fire_sound.set_volume(round(volume / 100, 1))
    explode_sound.set_volume(round(volume / 100, 1))
    def show(player_score, player_health, enemy_health, barrier_x, barrier_h, barrier_w, ground_h, fire_power):
        window.fill(white)
        score(player_score)
        health_bars(player_health, enemy_health)
        barrier(barrier_x, barrier_h, barrier_w)
        pygame.draw.rect(window, green, (0, H - ground_h, W, ground_h))
        power(fire_power)
        
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause()
                elif event.key == pygame.K_SPACE:
                    # player fire
                    damage = fireShell(turPos, tank_x, tank_y, turret_mode, fire_power, barrier_x, 
                                       H - barrier_h, barrier_h, barrier_w, enemy_tank_x, enemy_tank_y, player_health,
                                       enemy_health, player_score)
                    enemy_health -= damage

                    player_score += damage / 10
                    show(player_score, player_health, enemy_health, barrier_x, barrier_h, barrier_w, ground_h, fire_power)
                    turPos = tank(tank_x, tank_y, turret_mode)
                    enemy_turPos = enemy_tank(enemy_tank_x, enemy_tank_y, turret_mode_max)
                    pygame.display.update()

                    if enemy_health < 1:
                        win(player_score)

                    # enemy movement
                    possibleMovement = ['f', 'r']
                    moveIndex = random.randrange(0, 2)

                    for x in range(random.randrange(0, 20)):
                        if W * 0.3 > enemy_tank_x and possibleMovement[moveIndex] == 'f' :
                            enemy_tank_x += 5
                        if enemy_tank_x > W * 0.03 and possibleMovement[moveIndex] == 'r' :
                            enemy_tank_x -= 5

                        if not W * 0.3 > enemy_tank_x:
                            enemy_tank_x = W * 0.3
                        elif not enemy_tank_x > W * 0.03 :
                            enemy_tank_x = W * 0.03

                        show(player_score, player_health, enemy_health, barrier_x, barrier_h, barrier_w, ground_h, fire_power)
                        turPos = tank(tank_x, tank_y, turret_mode)
                        enemy_turPos = enemy_tank(enemy_tank_x, enemy_tank_y, turret_mode_max)
                        pygame.display.update()
                        clock.tick(FPS)

                    # enemy fire
                    damage = e_fireShell(enemy_turPos, enemy_tank_x, enemy_tank_y, turret_mode_max,
                                         fire_power, barrier_x, H - barrier_h, barrier_h, barrier_w, tank_x, tank_y, player_health,
                                         enemy_health, player_score, hard_level)
                    player_health -= damage
                    player_score -= damage / 10

                    show(player_score, player_health, enemy_health, barrier_x, barrier_h, barrier_w, ground_h, fire_power)
                    turPos = tank(tank_x, tank_y, turret_mode)
                    enemy_turPos = enemy_tank(enemy_tank_x, enemy_tank_y, turret_mode_max)
                    pygame.display.update()

                    if player_health < 1:
                        game_over(player_score)

        # Player's tank
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s] and fire_power > 1 :
            fire_power -= 1
        elif keys[pygame.K_w] and fire_power <= 100 :
            fire_power += 1
        if keys[pygame.K_LEFT] and tank_x > 0 and tank_x - (tank_w / 2) > barrier_x + barrier_w:
            tank_x -= 300 * dt
        elif keys[pygame.K_RIGHT] and tank_x + tank_w / 2 < W :
            tank_x += 300 * dt
        if keys[pygame.K_a] and turret_mode >= 0 :
            turret_mode -= 1
        elif keys[pygame.K_d] and turret_mode <= turret_mode_max :
            turret_mode +=1

        if turret_mode <= 0:
            turret_mode = 0
        elif turret_mode > turret_mode_max:
            turret_mode = turret_mode_max
        if fire_power < 1 :
            fire_power = 1
        elif fire_power >100:
            fire_power = 100

        # refersh screen
        pygame.display.update()
        show(player_score, player_health, enemy_health, barrier_x, barrier_h, barrier_w, ground_h, fire_power)
        turPos = tank(tank_x, tank_y, turret_mode)
        enemy_turPos = enemy_tank(enemy_tank_x, enemy_tank_y, turret_mode_max)
        dt = clock.tick(FPS) / 1000


game_intro()
