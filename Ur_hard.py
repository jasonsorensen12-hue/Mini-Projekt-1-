import pygame
import math
from datetime import datetime

pygame.init()
screen = pygame.display.set_mode((640, 480))
screen.fill((255, 255, 255))

screen_width = 640
screen_height = 480
s_length = 180
m_length = 170
h_length = 120
game = False
angle_bop = -90     # extra hand starts pointing up
bop_speed = 1.5     # degrees per loop
x = 0               # tip of the extra hand
y = 0
button = (590, 50)
button_radius = 25
clock = pygame.time.Clock()
font = pygame.font.Font(None, 28)
numbers = [12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
click = []
press = []
# background color per level
colors = [(255,255,255), (0,255,255), (0,255,128), (128,255,0), (255,255,0),
          (255,165,0), (255,80,0), (255,0,0), (255,0,255)]
bop_speedups = []   # len(bop_speedups) is the level
color = colors[0]
while True:
    screen.fill((color))
    if game == True:
        screen.fill((150, 255, 150), ((260+len(bop_speedups)*10, 40), (120-len(bop_speedups)*20, 25)), special_flags=pygame.BLEND_MULT)  # see-through green hit box
    now = datetime.now()
    milliseconds = now.hour * 3_600_000 + now.minute * 60_000 + now.second * 1000 + now.microsecond // 1000  # since midnight
    start = (screen_width/2, screen_height/2)  # clock center

    pygame.draw.circle(screen, (0,0,0), start, 205, 5)

    # start button: green while the game runs
    if game == True:
        pygame.draw.circle(screen, (0,180,0), button, button_radius)
    else:
        pygame.draw.circle(screen, (0,0,0), button, button_radius, 3)

    # hands: (milliseconds per turn, length, width)
    hands = [(60_000, s_length, 2),
             (3_600_000, m_length, 5),
             (43_200_000, h_length, 7)]
    for turn, length, width in hands:
        angle = milliseconds % turn / turn * 360 + 270
        end_x = start[0] + length * math.cos(math.radians(angle))
        end_y = start[1] + length * math.sin(math.radians(angle))
        pygame.draw.line(screen, (0,0,0), start, (end_x, end_y), width)

    # extra hand, not tied to the time
    if game == True:
        angle_bop += bop_speed
        x = start[0] + 195 * math.cos(math.radians(angle_bop))
        y = start[1] + 195 * math.sin(math.radians(angle_bop))
        pygame.draw.line(screen, (0,0,0), start, (x, y), 4)

    # ticks: (count, length, width, outer end)
    ticks = [(60, 5, 3, 195),     # seconds: floats 5 px inside the rim
             (12, 25, 4, 200)]    # hours
    for count, length, width, outer in ticks:
        for i in range(count):
            angle = i * 360 / count + 270
            tick_x = start[0] + (outer - length) * math.cos(math.radians(angle))
            tick_y = start[1] + (outer - length) * math.sin(math.radians(angle))
            end_x = start[0] + outer * math.cos(math.radians(angle))
            end_y = start[1] + outer * math.sin(math.radians(angle))
            pygame.draw.line(screen, (0,0,0), (tick_x, tick_y), (end_x, end_y), width)

    # hour numbers
    for i in range(12):
        angle = i * 30 + 270
        number_x = start[0] + (200 - 50) * math.cos(math.radians(angle))
        number_y = start[1] + (200 - 50) * math.sin(math.radians(angle))
        text = font.render(str(numbers[i]), True, (0,0,0))
        text_rect = text.get_rect(center=(number_x, number_y))
        screen.blit(text, text_rect)

    pygame.display.flip()
    clock.tick(240)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            # start button: 1st click starts, 2nd stops
            if pos[0] >= 565 and pos[0] <= 615 and pos[1] >= 25 and pos[1] <= 75:
                click.append(pos)
                if len(click) >= 2:
                    game = False
                    click = []
                else:
                    game = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # hit box: 59 to 1 mark
            if game == True and x >= 260+(len(bop_speedups)*10) and x <= 380-(len(bop_speedups)*10) and y >= 40 and y <= 65:
                press.append((x, y))
                if len(press) >= 3:  # 3rd hit: 1.3x faster, next level
                    bop_speed = bop_speed * 1.3
                    press = []
                    bop_speedups.append(bop_speed)
                    if len(bop_speedups) < len(colors):  # stays magenta after level 8
                        color = colors[len(bop_speedups)]
                print("hit")
            else:  # miss: reset
                print("miss")
                color = (255,255,255)
                bop_speed = 1.5
                game = False
                click = []
                print("You made it to: Level",len(bop_speedups))
                bop_speedups = []
                press = []

