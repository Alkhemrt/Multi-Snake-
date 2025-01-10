import pygame
import time
import random

pygame.init()

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (250, 50, 30)
green = (0, 255, 0)
blue = (60, 100, 100)
gray = (169, 169, 169)
color1 = (60, 30, 30)

dis_width = 600
dis_height = 400
dis = pygame.display.set_mode((dis_width,dis_height))
pygame.display.set_caption("Snake but bad")

clock = pygame.time.Clock()

snake_block = 10
snake_speed= 15

font_style = pygame.font.SysFont("fixedsys", 35)
score_font = pygame.font.SysFont("fixedsys", 30)
large_font = pygame.font.SysFont("fixedsys", 50)

def your_score(score, player=1):
    value = score_font.render(f"Player {player} Score: " + str(score), True, black)
    if player == 1:
        dis.blit(value, [10, 10])
    else:
        dis.blit(value, [dis_width - value.get_width() - 10, 10])


def the_snake(block_snake, snake_list, player=1):
    for x in snake_list:
        pygame.draw.rect(dis, green if player == 1 else red, [x[0], x[1], block_snake, block_snake])

def draw_obstacles(obstacles):
    for obs in obstacles:
        pygame.draw.rect(dis, gray, [obs[0], obs[1], snake_block, snake_block])

def message(msg, color, font, x_offset=0, y_offset=0):
    mesg = font.render(msg, True, color)
    dis.blit(mesg, [dis_width / 2 - mesg.get_width() / 2 + x_offset, dis_height / 3 + y_offset])

def generate_obstacles(num_obstacles):
    obstacles = []
    for _ in range(num_obstacles):
        x = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
        y = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
        obstacles.append([x, y])
    return obstacles

def main_menu():
    menu_active = True
    while menu_active:
        dis.fill(black)
        message("Snake but bad", green , large_font, 0, 5)
        message("Press P to Play, C for Multiplayer"
                ", or Q to Quit", white, font_style, 0, 50)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_active = False
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_p:
                    gameloop()
                    menu_active = False
                if event.key == pygame.K_c:
                    co_op_gameloop()
                    menu_active = False

def gameloop():
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2
    x1_change = 0
    y1_change = 0
    snake_list = []
    length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    obstacles = generate_obstacles(10)
    last_obstacle_update = pygame.time.get_ticks()
    obstacle_update_interval = 5000

    while not game_over:

        while game_close:
            dis.fill(color1)
            message("GAME OVER!", red, large_font)
            your_score(length_of_snake - 1)
            message("Press C to Play Again or Q to Quit", white, font_style, 0, 50)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameloop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:

                current_time = pygame.time.get_ticks()
                if current_time - last_obstacle_update > obstacle_update_interval:
                    obstacles = generate_obstacles(10)
                    last_obstacle_update = current_time

                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change

        dis.fill(blue)

        pygame.draw.rect(dis, yellow, [foodx, foody, snake_block, snake_block])
        draw_obstacles(obstacles)

        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]


        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        for obs in obstacles:
            if x1 == obs[0] and y1 == obs[1]:
                game_close = True

        the_snake(snake_block, snake_list)
        your_score(length_of_snake - 1)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            length_of_snake += 1


        clock.tick(snake_speed)

    pygame.quit()
    quit()

def co_op_gameloop():
    game_over = False
    game_close = False

    x1, x2 = dis_width / 4, dis_width * 3 / 4
    y1, y2 = dis_height / 2, dis_height / 2

    x1_change, x2_change = 0, 0
    y1_change, y2_change = 0, 0
    snake_list1, snake_list2 = [], []
    length_of_snake1, length_of_snake2 = 1, 1

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    generate_obstacles(10)
    last_obstacle_update = pygame.time.get_ticks()
    obstacle_update_interval = 10000

    obstacles = generate_obstacles(10)

    while not game_over:

        while game_close:
            dis.fill(color1)
            message("GAME OVER!", red, large_font)
            your_score(length_of_snake1 - 1, 1)
            your_score(length_of_snake2 - 1, 2)
            message("Press C to Play Again or Q to Quit", white, font_style, 0, 50)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        co_op_gameloop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:

                current_time = pygame.time.get_ticks()
                if current_time - last_obstacle_update > obstacle_update_interval:
                    obstacles = generate_obstacles(10)
                    last_obstacle_update = current_time

                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

                if event.key == pygame.K_a:
                    x2_change = -snake_block
                    y2_change = 0
                elif event.key == pygame.K_d:
                    x2_change = snake_block
                    y2_change = 0
                elif event.key == pygame.K_w:
                    y2_change = -snake_block
                    x2_change = 0
                elif event.key == pygame.K_s:
                    y2_change = snake_block
                    x2_change = 0

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            dis.fill(color1)
            message("Player 2 wins!", red, large_font)
            pygame.display.update()
            time.sleep(2)
            main_menu()
        if x2 >= dis_width or x2 < 0 or y2 >= dis_height or y2 < 0:
            dis.fill(color1)
            message("Player 1 wins!",green, large_font)
            pygame.display.update()
            time.sleep(2)
            main_menu()


        x1 += x1_change
        y1 += y1_change
        x2 += x2_change
        y2 += y2_change

        dis.fill(blue)

        pygame.draw.rect(dis, yellow, [foodx, foody, snake_block, snake_block])
        draw_obstacles(obstacles)

        snake_head1 = [x1, y1]
        snake_head2 = [x2, y2]
        snake_list1.append(snake_head1)
        snake_list2.append(snake_head2)

        if len(snake_list1) > length_of_snake1:
            del snake_list1[0]
        if len(snake_list2) > length_of_snake2:
            del snake_list2[0]

        for x in snake_list1[:-1]:
            if x == snake_head1:
                dis.fill(color1)
                message("Player 2 wins!",red, large_font)
                pygame.display.update()
                time.sleep(2)
                main_menu()
        for x in snake_list2[:-1]:
            if x == snake_head2:
                dis.fill(color1)
                message("Player 1 wins!", green, large_font)
                pygame.display.update()
                time.sleep(2)
                main_menu()

        for obs in obstacles:
            if x1 == obs[0] and y1 == obs[1]:
                dis.fill(color1)
                message("Player 2 wins!", red, large_font)
                pygame.display.update()
                time.sleep(2)
                main_menu()
            if x2 == obs[0] and y2 == obs[1]:
                dis.fill(color1)
                message("Player 1 wins!", green, large_font)
                pygame.display.update()
                time.sleep(2)
                main_menu()

        the_snake(snake_block, snake_list1, 1)
        the_snake(snake_block, snake_list2, 2)
        your_score(length_of_snake1 - 1, 1)
        your_score(length_of_snake2 - 1, 2)

        if length_of_snake1 >= 16:
            dis.fill(color1)
            message("Player 1 wins!", green, large_font)
            pygame.display.update()
            time.sleep(2)
            main_menu()
        elif length_of_snake2 >= 16:
            dis.fill(color1)
            message("Player 2 wins!", red, large_font)
            pygame.display.update()
            time.sleep(2)
            main_menu()

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            length_of_snake1 += 1
        if x2 == foodx and y2 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            length_of_snake2 += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()


main_menu()