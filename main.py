import pygame
import random


def update_grid(n, is_shine, tutorial):
    if is_shine:
        update_shine(n)
    else:
        fill_world()
        for i in money_positions:
            draw_coin(i, world)
        draw_world()
    if tutorial:
        draw_tutorial(world)


def fill_world():
    world.fill("#cdebff")
    if is_grid:
        grid()


def grid():
    for i in range(0, height, 50):
        pygame.draw.line(world, "#a1b8c7", (0, i), (width, i), 3)
    for i in range(0, width, 100):
        pygame.draw.line(world, "#a1b8c7", (i, 0), (i, height), 3)


def update_shine(n):
    fill_world()
    for i in range(len(money_positions)):
        if n < money_positions[i]:
            draw_coin(money_positions[i], world)
    draw_world()
    columns_help(n)


def move_screen(pos_x, pos_y, n, is_shine):
    for i in range(40):
        for j in range(len(column_positions)):
            column_positions[j][0] -= 5
        fill_world()
        for j in range(len(money_positions)):
            draw_coin(money_positions[j], world)
        draw_world()
        if is_shine is True:
            columns_help(n)
        screen.blit(world, (0, 0))
        draw_energy()
        money(screen)
        screen.blit(picture, (pos_x, pos_y - pic_height))
        pos_x -= 5
        pygame.display.flip()
        clock.tick(80)
    return pos_x


def columns_help(position):
    yy = []
    for k in range(len(column_positions)):
        if k < position:
            yy.append(0)
        else:
            yy.append(column_positions[k][1])
    n = len(yy)
    ans = [[] for _ in range(n)]
    dp = [0] * n
    dp[0] = 0
    ans[0].append(0)
    dp[1] = abs(yy[0] - yy[1])
    ans[1] = ans[0].copy()
    ans[1].append(1)
    for i in range(2, n):
        if abs(yy[i - 2] - yy[i]) * 3 + dp[i - 2] < dp[i - 1] + abs(yy[i - 1] - yy[i]):
            dp[i] = abs(yy[i - 2] - yy[i]) * 3 + dp[i - 2]
            ans[i] = ans[i - 2].copy()
            ans[i].append(i)
        else:
            dp[i] = dp[i - 1] + abs(yy[i - 1] - yy[i])
            ans[i] = ans[i - 1].copy()
            ans[i].append(i)
    for i in ans[-1]:
        if i > position:
            shine(i, world)


def money_update(surface):
    pygame.draw.polygon(surface, "#cdebff", ((250, 5), (325, 5), (325, 80), (250, 80)))
    pygame.draw.line(world, "#a1b8c7", (300, 0), (300, 100), 3)


def money(surface):
    pygame.draw.circle(surface, "#fffc33", (220, 50), 30)
    pygame.draw.circle(surface, "#fffc33", (220, 50), 30, 5)
    pygame.draw.circle(surface, "#000000", (220, 50), 30, 3)
    pygame.draw.circle(surface, "#000000", (220, 50), 25, 3)
    font = pygame.font.SysFont('serif', 50)
    text1 = font.render(str(my_money), True, "#000000")
    surface.blit(text1, (260, 20))
    font = pygame.font.SysFont('serif', 30)
    text1 = font.render("1", True, "#000000")
    surface.blit(text1, (213, 33))
    pygame.draw.circle(surface, "#000000", (339, 50), 15, 3)
    pygame.draw.circle(surface, "#000000", (511, 50), 15, 3)
    if my_money < 3:
        pygame.draw.polygon(surface, "#f0bcff", ((340, 35), (510, 35), (510, 63), (340, 63)))
        pygame.draw.polygon(surface, "#000000", ((340, 35), (510, 35), (510, 63), (340, 63)), 2)
        pygame.draw.circle(surface, "#f0bcff", (339, 50), 13)
        pygame.draw.circle(surface, "#f0bcff", (511, 50), 13)
    else:
        pygame.draw.polygon(surface, "#6dff69", ((340, 35), (510, 35), (510, 63), (340, 63)))
        pygame.draw.polygon(surface, "#000000", ((340, 35), (510, 35), (510, 63), (340, 63)), 2)
        pygame.draw.circle(surface, "#6dff69", (339, 50), 13)
        pygame.draw.circle(surface, "#6dff69", (511, 50), 13)
    font_size = 20
    font = pygame.font.SysFont('serif', font_size)
    text = font.render("получить подсказку", True, "#000000")
    surface.blit(text, (340, 38))
    pygame.draw.polygon(surface, "#6dff69", ((540, 35), (580, 35), (580, 63), (540, 63)))
    pygame.draw.polygon(surface, "#000000", ((540, 35), (580, 35), (580, 63), (540, 63)), 2)
    font_size = 20
    font = pygame.font.SysFont('serif', font_size)
    text = font.render("grid", True, "#000000")
    surface.blit(text, (544, 38))


def energy(x1, y1, x2, y2):
    global my_energy
    if x2 - x1 > 300:
        my_energy -= 3 * abs(y1 - y2)
    else:
        my_energy -= abs(y1 - y2)


def draw_energy():
    font = pygame.font.SysFont('serif', 50)
    text1 = font.render(str(my_energy), True, "#000000")
    screen.blit(text1, (60, 20))
    pygame.draw.polygon(screen, "#fffb00", ((50, 10), (20, 50), (35, 50), (20, 80), (55, 40), (40, 40)))
    pygame.draw.polygon(screen, "#000000", ((50, 10), (20, 50), (35, 50), (20, 80), (55, 40), (40, 40)), 3)


def ideal_energy():
    yy = []
    for k in column_positions:
        yy.append(k[1])
    n = len(yy)
    dp = [0] * n
    dp[0] = 0
    dp[1] = abs(yy[0] - yy[1])
    for i in range(2, n):
        if abs(yy[i - 2] - yy[i]) * 3 + dp[i - 2] < dp[i - 1] + abs(yy[i - 1] - yy[i]):
            dp[i] = abs(yy[i - 2] - yy[i]) * 3 + dp[i - 2]
        else:
            dp[i] = dp[i - 1] + abs(yy[i - 1] - yy[i])
    return 2500 - dp[n - 1]


def shine(n, surface):
    x = column_positions[n][0]
    y = column_positions[n][1]
    pygame.draw.polygon(surface, "#ff00f6", ((x + 17, height + 10), (x + 17, y + 73), (x - 3, y + 73),
                                             (x - 3, y - 3), (x + 143, y - 3), (x + 143, y + 73), (x + 123, y + 73),
                                             (x + 123, height + 10)), 3)

    pygame.draw.polygon(surface, "#f599f0", ((x + 14, height + 10), (x + 14, y + 76), (x - 6, y + 76),
                                             (x - 6, y - 6), (x + 146, y - 6), (x + 146, y + 76), (x + 126, y + 76),
                                             (x + 126, height + 10)), 3)
    pygame.draw.polygon(surface, "#f0bcff", ((x + 11, height + 10), (x + 11, y + 79), (x - 9, y + 79),
                                             (x - 9, y - 9), (x + 149, y - 9), (x + 149, y + 79), (x + 129, y + 79),
                                             (x + 129, height + 10)), 3)


def draw_tutorial(surface):
    font = pygame.font.SysFont('serif', 25)
    pygame.draw.polygon(surface, "white", ((600, 20), (1170, 20), (1170, 350), (600, 350)))
    pygame.draw.polygon(surface, "black", ((600, 20), (1170, 20), (1170, 350), (600, 350)), 3)
    pygame.draw.polygon(surface, "white", ((600, 380), (1170, 380), (1170, 470), (600, 470)))
    pygame.draw.polygon(surface, "black", ((600, 380), (1170, 380), (1170, 470), (600, 470)), 3)
    txt = ["Чтобы попасть с одной платформы на другую", "достаточно просто нажать на нее. Прыгать можно",
           "на соседнюю платформу и через одну. При прыжке", "на соседнюю вы потратите |y2–y1| энергии, если",
           "вы прыгаете через платформу то 3·|y3–y1| единиц", "энергии. (y-высота платформы). Изначально у вас",
           "2500 единиц энергии, цель - потратить наименьшее", "количество энергии и добраться до финиша. При",
           "отклонение вашего результата от идеального более", "чем на 25%, уровень придеться пройти заново."]
    for i in range(len(txt)):
        text = font.render(txt[i], True, "#000000")
        surface.blit(text, (620, (i+1)*30))
    font = pygame.font.SysFont('serif', 24)
    txt1 = ["Попробуй перепрыгнуть на платформу, нажмите", "на кнопку чтобы получить подсказку и понять",
            "куда прыгать, а после можете приступать к уровням"]
    for i in range(len(txt1)):
        text = font.render(txt1[i], True, "#000000")
        surface.blit(text, (620, 385+i*25))
    font = pygame.font.SysFont('serif', 15)
    pygame.draw.line(surface, "black", (510, 70), (530, 80), 3)
    text14 = font.render("одна подсказка стоит 3 монеты", True, "#000000")
    surface.blit(text14, (380, 82))


def jump(start_x, start_y, finish_x, finish_y, n):
    global current_energy
    # самые высокие позиции в прыжке
    if finish_x - start_x <= 200:
        center_y = max(min(start_y, finish_y) - (pic_height // 3), 0)
    else:
        center_y = max(min(start_y, finish_y, column_positions[n+1][1]-pic_height) - (pic_height // 3), 0)
    center_x = (start_x + finish_x) // 2
    b = center_y
    d = center_x
    jump_sound.play()
    if (start_x - d) ** 2 != 0:
        a = (start_y - b) / ((start_x - d) ** 2)
    else:
        a = (start_y - b) / ((start_x - d) ** 2 + 0.1)
    new_pic_size = pic_height
    for k in range(start_x, d):
        # завершение программы при закрытие экрана
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                exit(0)
        # расчет позиций
        new_pic_size = max(new_pic_size - 0.2, 10)
        y = a * ((start_x - d) ** 2) + b
        start_x += 1
        screen.blit(world, (0, 0))
        pic_resized = pygame.transform.smoothscale(picture, (pic_width, new_pic_size))
        draw_energy()
        money(screen)
        screen.blit(pic_resized, (start_x, y))
        clock.tick(200)
        pygame.display.flip()
    # переменные для формулы прыжка
    if ((finish_x - (finish_x - start_x) * 2) - d) ** 2 != 0:
        a = (finish_y - b) / (((finish_x - (finish_x - start_x) * 2) - d) ** 2)
    else:
        a = (finish_y - b + 0.1) / (((finish_x - (finish_x - start_x) * 2) - d) ** 2 + 0.1)
    for k in range(center_x, finish_x):
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                exit(0)
        # расчет позиций
        y = a * ((center_x - d) ** 2) + b
        center_x += 1
        new_pic_size = min(new_pic_size + 0.2, pic_height)

        screen.blit(world, (0, 0))
        pic_resized = pygame.transform.smoothscale(picture, (pic_width, new_pic_size))
        draw_energy()
        money(screen)
        screen.blit(pic_resized, (center_x, y))
        clock.tick(200)
        pygame.display.flip()
    fall_sound.play()


def draw_mini_button(x, y, txt):
    pygame.draw.circle(screen, "black", (x + 53, y + 37), 38)
    pygame.draw.circle(screen, "black", (x + 300, y + 37), 38)
    pygame.draw.polygon(screen, "black", ((x + 53, y), (x + 300, y), (x + 300, y + 74), (x + 53, y + 74)), 3)
    pygame.draw.circle(screen, "#6dff69", (x + 53, y + 37), 35)
    pygame.draw.circle(screen, "#6dff69", (x + 300, y + 37), 35)
    pygame.draw.polygon(screen, "#6dff69", ((x + 53, y + 2), (x + 300, y + 2), (x + 300, y + 72), (x + 53, y + 72)))
    font_size = 38
    font = pygame.font.SysFont('serif', font_size)
    text = font.render(txt, True, "#000000")
    screen.blit(text, (x + font_size // 4 * 3, y + font_size // 4))


def draw_column(x, y):
    pygame.draw.polygon(world, "#32ab00", ((x + 20, height + 10), (x + 20, y + 70), (x, y + 70), (x, y), (x + 140, y),
                                           (x + 140, y + 70), (x + 120, y + 70), (x + 120, height + 10)))
    pygame.draw.polygon(world, "#4bff00", ((x + 30, y + 70), (x + 30, y), (x + 70, y), (x + 70, y + 70)))
    pygame.draw.polygon(world, "#4bff00", ((x + 75, y + 70), (x + 75, y + 10), (x + 85, y + 10), (x + 85, y + 70)))
    pygame.draw.polygon(world, "#4bff00",
                        ((x + 40, height + 10), (x + 40, y + 70), (x + 80, y + 70), (x + 80, height + 10)))
    pygame.draw.polygon(world, "#4bff00",
                        ((x + 85, height + 10), (x + 85, y + 70), (x + 95, y + 70), (x + 95, height + 10)))
    pygame.draw.polygon(world, "#4bff00", ((x, y + 5), (x, y), (x + 140, y), (x + 140, y + 5)))
    pygame.draw.polygon(world, "#000000", ((x + 20, height + 10), (x + 20, y + 70), (x, y + 70), (x, y),
                                           (x + 140, y), (x + 140, y + 70), (x + 20, y + 70), (x + 120, y + 70),
                                           [x + 120, height + 10]), 3)


def draw_world():
    for x in range(0, len(column_positions)):
        draw_column(column_positions[x][0], column_positions[x][1])


def draw_button(x, y, txt, surface):
    pygame.draw.circle(surface, "black", (x + 53, y + 52), 53)
    pygame.draw.circle(surface, "black", (x + 400, y + 52), 53)
    pygame.draw.polygon(surface, "black", ((x + 53, y), (x + 400, y), (x + 400, y + 104), (x + 53, y + 104)), 3)
    pygame.draw.circle(surface, "#6dff69", (x + 53, y + 52), 50)
    pygame.draw.circle(surface, "#6dff69", (x + 400, y + 52), 50)
    pygame.draw.polygon(surface, "#6dff69", ((x + 53, y + 2), (x + 400, y + 2), (x + 400, y + 102), (x + 53, y + 102)))
    font_size = 80
    font = pygame.font.SysFont('serif', font_size)
    text = font.render(txt, True, "#000000")
    surface.blit(text, (x + button_width // 2 - (len(txt)) * font_size // 4.3, y))


def draw_locked_button(x, y):
    pygame.draw.circle(screen, "black", (x, y + 52), 53)
    pygame.draw.circle(screen, "black", (x + 400, y + 52), 53)
    pygame.draw.polygon(screen, "black", ((x, y), (x + 400, y), (x + 400, y + 104), (x, y + 104)), 3)
    pygame.draw.circle(screen, "#a15259", (x, y + 52), 50)
    pygame.draw.circle(screen, "#a15259", (x + 400, y + 52), 50)
    pygame.draw.polygon(screen, "#a15259", ((x, y + 2), (x + 400, y + 2), (x + 400, y + 102), (x, y + 102)))
    screen.blit(lock, (x + 130, y - 15))


def draw_opened_button(x, y, txt):
    pygame.draw.circle(screen, "black", (x, y + 52), 53)
    pygame.draw.circle(screen, "black", (x + 400, y + 52), 53)
    pygame.draw.polygon(screen, "black", ((x, y), (x + 400, y), (x + 400, y + 104), (x, y + 104)), 3)
    pygame.draw.circle(screen, "#6dff69", (x, y + 52), 50)
    pygame.draw.circle(screen, "#6dff69", (x + 400, y + 52), 50)
    pygame.draw.polygon(screen, "#6dff69", ((x, y + 2), (x + 400, y + 2), (x + 400, y + 102), (x, y + 102)))
    font_size = 80
    font = pygame.font.SysFont('serif', font_size)
    text = font.render(txt, True, "#000000")
    screen.blit(text, (x + button_width // 2 - (len(txt)) * font_size // 4, y))


def draw_buttons(opened, locked):
    font = pygame.font.SysFont('serif', 30)
    text14 = font.render("выберите уровень который вы хотели бы пройти", True, "#000000")
    screen.blit(text14, (300, 10 + screen_position))
    gap = 120
    y = 100
    for i in range(1, opened + 1):
        draw_opened_button(400, y + screen_position, "Level " + str(i))
        y += gap
    for i in range(opened + 1, locked + opened + 1):
        draw_locked_button(400, y + screen_position)
        y += gap


def menu(txt, surface):
    surface.fill("#cdebff")
    pygame.draw.circle(surface, "white", (600, 300), 400)
    pygame.draw.circle(surface, "black", (600, 300), 400, 3)
    font_size = 60
    font = pygame.font.SysFont('serif', font_size)
    text1 = font.render(txt, True, "#000000")
    surface.blit(text1, (width // 2 - ((len(txt) - 2) * font_size // 4), height // 3.5))
    draw_button((width - button_width) // 2, height - 3 * button_height, "да", surface)
    draw_button((width - button_width) // 2, height - 2 * button_height, "нет", surface)


def draw_coin(n, surface):
    pygame.draw.circle(surface, "#fffc33", (column_positions[n][0] + 70, column_positions[n][1] - 40), 30)
    pygame.draw.circle(surface, "#fffc33", (column_positions[n][0] + 70, column_positions[n][1] - 40), 30, 5)
    pygame.draw.circle(surface, "#000000", (column_positions[n][0] + 70, column_positions[n][1] - 40), 30, 3)
    pygame.draw.circle(surface, "#000000", (column_positions[n][0] + 70, column_positions[n][1] - 40), 25, 3)
    font = pygame.font.SysFont('serif', 30)
    text1 = font.render("1", True, "#000000")
    surface.blit(text1, (column_positions[n][0] + 63, column_positions[n][1] - 56))


def delete_coin(n, surface):
    pygame.draw.circle(surface, "#cdebff", (column_positions[n][0] + 70, column_positions[n][1] - 40), 31)
    x = (column_positions[n][0] + 101) - (column_positions[n][0] + 101) % 100
    if x >= column_positions[n][0] + 39:
        pygame.draw.line(surface, "#a1b8c7", (x, column_positions[n][1] - 71),
                         (x, column_positions[n][1] - 2), 3)
    y = (column_positions[n][1] - 9) - (column_positions[n][1] - 9) % 150
    if y >= column_positions[n][1] - 71:
        pygame.draw.line(surface, "#a1b8c7", (column_positions[n][0] + 39, y),
                         (column_positions[n][0] + 101, y), 3)
    y = (column_positions[n][1] - 9) - (column_positions[n][1] - 9) % 50
    if y >= column_positions[n][1] - 71:
        pygame.draw.line(surface, "#a1b8c7", (column_positions[n][0] + 39, y),
                         (column_positions[n][0] + 101, y), 3)


pygame.init()
pygame.font.init()
size = width, height = 1200, 600
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)
running = True
pygame.mixer.music.load("mixkit-beautiful-dream-493.mp3")
pygame.mixer.music.play(loops=-1, start=0.0, fade_ms=3000)
pygame.mixer.music.set_volume(0.3)
jump_sound = pygame.mixer.Sound("archivo (4).mp3")
jump_sound.set_volume(0.3)
fall_sound = pygame.mixer.Sound("archivo (2).mp3")
fall_sound.set_volume(0.5)
coin_sound = pygame.mixer.Sound("coin.wav")
coin_sound.set_volume(1)

is_grid = True
# подготовка картинки уровня
column_positions = [[130, 250], [330, 360]]
world = pygame.Surface((1200, 600))
fill_world()
draw_world()
my_energy = 2500
my_money = 5

# подготовка картинки персонажа
picture = pygame.image.load('snoopy1.1-fotor-bg-remover-20250503132254.png').convert_alpha()
pic_width = 140
pic_height = 150
picture = pygame.transform.scale(picture, (pic_width, pic_height))

# цикл 1 хотите ли играть?
button_height = 110
button_width = 460


def step1():
    global running
    menu_1 = pygame.Surface((1200, 600))
    menu("хотите начать игру?", menu_1)
    while running is True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if ((width - button_width) // 2 <= event.pos[0] <= (width - button_width) // 2 + button_width and
                        (height - 3 * button_height) <= event.pos[1] <= (height - 3 * button_height + button_height)):
                    step2()
                elif ((width - button_width) // 2 <= event.pos[0] <= (width - button_width) // 2 + button_width and
                      (height - 2 * button_height) <= event.pos[1] <= (height - 2 * button_height + button_height)):
                    running = False
        screen.blit(menu_1, (0, 0))
        pygame.display.flip()


# цикл 2 хотите ли научиться играть?
def step2():
    menu_2 = pygame.Surface((1200, 600))
    menu("хотите пройти обучение?", menu_2)
    global running
    while running is True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if ((width - button_width) // 2 <= event.pos[0] <= (width - button_width) // 2 + button_width and
                        (height - 3 * button_height) <= event.pos[1] <= (height - 3 * button_height + button_height)):
                    step3()
                elif ((width - button_width) // 2 <= event.pos[0] <= (width - button_width) // 2 + button_width and
                      (height - 2 * button_height) <= event.pos[1] <= (height - 2 * button_height + button_height)):
                    step4()
        screen.blit(menu_2, (0, 0))
        pygame.display.flip()


# цикл 3 обучение
def step3():
    global running, my_money, is_grid
    is_shine = False
    current_position = 0
    column_width = 140
    draw_tutorial(world)
    money(world)
    pic_position_x = column_positions[0][0]
    pic_position_y = column_positions[0][1] - pic_height
    while running is True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # нажатие на столбик
                if (column_positions[1][0] <= event.pos[0] <= column_positions[1][0] + column_width and
                        column_positions[1][1] <= event.pos[1] <= height):
                    jump(pic_position_x, pic_position_y, column_positions[1][0],
                         column_positions[1][1] - column_width, current_position)
                    energy(pic_position_x, pic_position_y + pic_height, column_positions[1][0],
                           column_positions[1][1])
                    pic_position_x, pic_position_y = column_positions[1][0], column_positions[1][1] - 150
                    current_position += 1
                # нажатие на кнопку продолжить
                elif (current_position == 1 and 670 <= event.pos[0] <= 670 + button_width
                      and 480 <= event.pos[1] <= 480 + button_height):
                    step4()
                # нажатие на кнопку подсказка  335 525 35 63 - координаты кнопки
                elif 335 <= event.pos[0] <= 525 and 35 <= event.pos[1] <= 63:
                    is_shine = True
                    shine(1, world)
                    my_money -= 3
                    money_update(world)
                # (540, 35), (580, 35), (580, 63), (540, 63) это не доделано
                elif 540 <= event.pos[0] <= 580 and 35 <= event.pos[1] <= 63:
                    if is_grid:
                        is_grid = False
                    else:
                        is_grid = True
                    update_grid(0, is_shine, True)
        screen.blit(world, (0, 0))
        draw_energy()
        money(world)
        if current_position == 1:
            draw_button(670, 480, "начать игру", screen)
        screen.blit(picture, (pic_position_x, pic_position_y))
        clock.tick(20)
        pygame.display.flip()


# цикл 4 выбор уровня
open_levels = 10
locked_levels = 0
lock = pygame.image.load('locked_lock-Photoroom.png').convert_alpha()
lock = pygame.transform.scale(lock, (140, 120))
screen_position = 0


def step4():
    global running, screen_position
    btn_position_1 = 345
    btn_position_2 = 855
    level_btm_height = 100
    level_btm_gap = 120
    while running is True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit(0)
            elif event.type == pygame.MOUSEWHEEL:
                screen_position = min(screen_position + event.y * 10, 0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if btn_position_1 <= event.pos[0] <= btn_position_2:
                    for y in range(level_btm_height + screen_position, width + screen_position, level_btm_gap):
                        if y <= event.pos[1] <= y + level_btm_height:
                            if (y - screen_position - level_btm_height) // level_btm_gap + 1 <= open_levels:
                                step5((y - screen_position - level_btm_height) // level_btm_gap + 1, "new_level")
        screen.fill("#cdebff")
        draw_buttons(open_levels, locked_levels)
        pygame.display.flip()


# цикл 5 отрисовка уровня игры
money_positions = []


def step5(n, txt):
    global running, world, column_positions, my_money, my_energy, money_positions, is_grid
    is_shine = False
    my_energy = 2500
    if txt == "new_level":
        column_positions = []
        fill_world()
        for i in range(n + 2):
            column_positions.append([30 + 200 * i, random.randint(150, 400)])
            if random.randint(1, 2) == 2 and i != 0:
                draw_coin(i, world)
                money_positions.append(i)
    elif txt == "old_level":
        fill_world()
        if column_positions[1][0] < 30:
            shift = 30 - column_positions[0][0]
            for i in range(len(column_positions)):
                column_positions[i][0] += shift
        for i in money_positions:
            draw_coin(i, world)
    current_position = 0
    draw_world()
    pic_position_x = column_positions[0][0]
    pic_position_y = column_positions[0][1] - pic_height
    while running is True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # реакция на нажатие на колону
                for i in range(current_position + 1, current_position + 3):
                    # проверка что колона в допустимом радиусе прыжка
                    if (i < len(column_positions) and column_positions[i][0] <= event.pos[0] <=
                            column_positions[i][0] + pic_width) and column_positions[i][1] <= event.pos[1] <= height:
                        jump(pic_position_x, pic_position_y, column_positions[i][0],
                             column_positions[i][1] - pic_height, current_position)
                        energy(pic_position_x, pic_position_y + pic_height, column_positions[i][0],
                               column_positions[i][1])
                        pic_position_x, pic_position_y = column_positions[i][0], column_positions[i][1] - pic_height
                        current_position = i
                        if current_position in money_positions:
                            my_money += 1
                            coin_sound.play()
                            delete_coin(current_position, world)
                            money_positions.pop(money_positions.index(current_position))
                        if is_shine is True:
                            update_shine(current_position)
                # нажатие на кнопку подсказка  335 525 35 63 - координаты кнопки
                if 335 <= event.pos[0] <= 525 and 35 <= event.pos[1] <= 63 and my_money >= 3 and is_shine is False:
                    my_money -= 3
                    money_update(world)
                    columns_help(current_position)
                    is_shine = True
                # (540, 35), (580, 35), (580, 63), (540, 63) это не доделано
                elif 540 <= event.pos[0] <= 580 and 35 <= event.pos[1] <= 63:
                    if is_grid:
                        is_grid = False
                    else:
                        is_grid = True
                    update_grid(current_position, is_shine, False)
        screen.blit(world, (0, 0))
        draw_energy()
        money(screen)
        if column_positions[current_position][0] >= 40 and len(column_positions) - current_position >= 5:
            pic_position_x = move_screen(column_positions[current_position][0], column_positions[current_position][1],
                                         current_position, is_shine)
        if current_position == n + 1:
            step6(n)
        screen.blit(picture, (pic_position_x, pic_position_y))
        clock.tick(20)
        pygame.display.flip()


# завершение уровня
pic1_width = 270
pic1_height = 270
happy_picture = pygame.image.load('image-fotor-bg-remover-2025050314428.png').convert_alpha()
happy_picture = pygame.transform.scale(happy_picture, (pic1_width, pic1_height))
sad_picture = pygame.image.load('sad_snoopy.png').convert_alpha()
sad_picture = pygame.transform.scale(sad_picture, (pic1_width, pic1_height))


# цикл 6 завершение уровня
def step6(n):
    global running, open_levels, locked_levels
    radius = 0
    mini_btn_x = 550
    mini_btn_y = 340
    mini_btn_width = 300
    mini_btn_height = 70
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if (mini_btn_x <= event.pos[0] <= mini_btn_x + mini_btn_width and mini_btn_y <= event.pos[1] <=
                        mini_btn_y + mini_btn_height and ideal_energy() * 0.75 <= my_energy <= ideal_energy()):
                    open_levels = min(max(open_levels, n + 1), 10)
                    locked_levels = max(0, 10 - open_levels)
                    step4()
                elif (mini_btn_x <= event.pos[0] <= mini_btn_x + mini_btn_width and mini_btn_y <= event.pos[1] <=
                      mini_btn_y + mini_btn_height):
                    step5(n, "old_level")
        screen.blit(world, (0, 0))
        pygame.draw.circle(screen, "white", (width // 2, height // 2), radius)
        if radius < 360:
            radius += 10
        else:
            font = pygame.font.SysFont('serif', 60)
            text1 = font.render("ваша энергия: " + str(my_energy), True, "#000000")
            text2 = font.render("идеальное количество", True, "#000000")
            text3 = font.render("энергии: " + str(ideal_energy()), True, "#000000")
            screen.blit(text1, (360, 100))
            screen.blit(text2, (320, 200))
            screen.blit(text3, (420, 260))
            if ideal_energy() * 0.75 <= my_energy <= ideal_energy():
                draw_mini_button(mini_btn_x, mini_btn_y, "продолжить игру")
                screen.blit(happy_picture, (350, height - pic1_height))
            else:
                draw_mini_button(mini_btn_x, mini_btn_y, "пройти игру снова")
                screen.blit(sad_picture, (350, height - pic1_height))
        pygame.display.flip()
        clock.tick(60)


step1()
pygame.quit()

