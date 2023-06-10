import pygame
import numpy
import random
import time

pygame.init()

screen_width = 840
screen_height = 600

title = "2048"

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption(title)

def move_LR():
    for i in range(len(box_frame)):
        new_list = [elem for elem in box_frame[i] if elem != 0]
        if LEFT == 1:
            for j in range(len(new_list)-1):
                if new_list[j] == new_list[j+1]:
                    new_list[j] *= 2
                    new_list[j+1] = 0
            new_list = [elem for elem in new_list if elem != 0]
            while len(new_list) < 4:
                new_list.append(0)
        elif RIGHT == 1:
            for j in range(len(new_list)-1):
                if new_list[j] == new_list[j+1]:
                    new_list[j+1] *= 2
                    new_list[j] = 0
            new_list = [elem for elem in new_list if elem != 0]
            while len(new_list) < 4:
                zero_list = [0 for _ in range(4 - len(new_list))]
                new_list = zero_list + new_list
        box_frame[i] = new_list
    spawn()
        
def move_UD():
    global box_frame
    box_frame_vertical = numpy.transpose(box_frame)
    for i in range(len(box_frame)):
        new_list_vertical = [elem for elem in box_frame_vertical[i] if elem != 0]
        if UP == 1:
            for j in range(len(new_list_vertical)-1):
                if new_list_vertical[j] == new_list_vertical[j+1]:
                    new_list_vertical[j] *= 2
                    new_list_vertical[j+1] = 0
            new_list_vertical = [elem for elem in new_list_vertical if elem != 0]
            while len(new_list_vertical) < 4:
                new_list_vertical.append(0)
            box_frame_vertical[i] = new_list_vertical
            box_frame = numpy.transpose(box_frame_vertical)
        elif DOWN == 1:
            for j in range(len(new_list_vertical)-1):
                if new_list_vertical[j] == new_list_vertical[j+1]:
                    new_list_vertical[j+1] *= 2
                    new_list_vertical[j] = 0
            new_list_vertical = [elem for elem in new_list_vertical if elem != 0]
            while len(new_list_vertical) < 4:
                zero_list = [0 for _ in range(4 - len(new_list_vertical))]
                new_list_vertical = zero_list + new_list_vertical
            box_frame_vertical[i] = new_list_vertical
    box_frame = numpy.transpose(box_frame_vertical)
    spawn()
    
def spawn():
    global running
    empty_cells = []
    for i in range(len(box_frame)):
        for j in range(len(box_frame[i])):
            if box_frame[i][j] == 0:
                empty_cells.append((i, j))
    
    if len(empty_cells) > 0:
        random_index = random.randrange(len(empty_cells))
        random_x, random_y = empty_cells[random_index]
        if random.random() > 0.9:
            box_frame[random_x][random_y] = 4
        else:
            box_frame[random_x][random_y] = 2
    else:
        game_over = game_font.render('GAME OVER', True, (0,0,0))
        screen.blit(game_over, (200,200))
        time.sleep(10)
        running = False

def draw_box():
    for i in range(len(box_frame)):
        for j in range(len(box_frame[0])):
            pygame.draw.rect(screen, BOX_FRAME, (screen_x + box_gap * (j+1) + box_width * j, screen_y + box_gap * (i+1) + box_height * i,box_width,box_height))
            
            txt_number = game_font.render(str(box_frame[i][j]),True,(0,0,0))
            if box_frame[i][j] != 0:
                screen.blit(txt_number, (screen_x + box_gap * (j+1) + box_width * j + box_width // 2 - 8, screen_y + box_gap * (i+1) + box_height * i + box_height // 2 - 8))

box_frame = [
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0]
]

spawn()
spawn()

box_width = 80
box_height = 80
box_gap = 16

# 색깔 변수
BG = 255,248,220
GAME_FRAME = 245,222,179
BOX_FRAME = 188,143,143

# 넓이 변수
game_frame_width = 400
game_frame_height = 400

# 키보드 변수
UP = None
DOWN = None
LEFT = None
RIGHT = None

screen_x = screen_width // 2 - game_frame_width // 2
screen_y = screen_height // 2 - game_frame_height // 2

game_font = pygame.font.SysFont("arialrounded", 15)

clock = pygame.time.Clock()

running = True
while running:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                UP = 1
                move_UD()
                UP = None
            elif event.key == pygame.K_DOWN:
                DOWN = 1
                move_UD()
                DOWN = None
            elif event.key == pygame.K_LEFT:
                LEFT = 1
                move_LR()
                LEFT = None
            elif event.key == pygame.K_RIGHT:
                RIGHT = 1
                move_LR()
                RIGHT = None

    screen.fill(BG)
    
    # GAME_FRAME
    pygame.draw.rect(screen, GAME_FRAME, (screen_x,screen_y,game_frame_width,game_frame_height), 0)
    # BOX_FRAME
    draw_box()
    pygame.display.update()

pygame.quit()
