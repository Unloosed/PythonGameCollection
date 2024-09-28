import pygame
import random

def create_display(width, height):
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Snake Game")
    return win

def define_colors():
    return {
        "white": (255, 255, 255),
        "black": (0, 0, 0),
        "red": (213, 50, 80),
        "green": (0, 255, 0),
        "blue": (50, 153, 213)
    }

def create_fonts():
    font_style = pygame.font.SysFont("bahnschrift", 25)
    score_font = pygame.font.SysFont("comicsansms", 35)
    return font_style, score_font

def our_snake(win, color, snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(win, color, [x[0], x[1], snake_block, snake_block])

def message(win, font_style, msg, color, width, height):
    mesg = font_style.render(msg, True, color)
    win.blit(mesg, [width / 6, height / 3])

def generate_food_coordinates(width, height, snake_block):
    food_x = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    food_y = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
    return food_x, food_y

def game_loop():
    width, height = 600, 400
    snake_block = 10
    snake_speed = 15

    pygame.init()
    win = create_display(width, height)
    colors = define_colors()
    font_style, score_font = create_fonts()

    clock = pygame.time.Clock()

    game_over = False
    game_close = False

    x1 = width / 2
    y1 = height / 2

    x1_change = 0
    y1_change = 0

    food_x, food_y = generate_food_coordinates(width, height, snake_block)

    snake_list = []
    length_of_snake = 1

    game_over_message = "You Lost! Press Q-Quit or C-Play Again"

    while not game_over:

        while game_close:
            win.fill(colors["blue"])
            message(win, font_style, game_over_message, colors["red"], width, height)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    x1_change = 0
                    y1_change = -snake_block
                elif event.key == pygame.K_DOWN:
                    x1_change = 0
                    y1_change = snake_block

        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        win.fill(colors["white"])
        pygame.draw.rect(win, colors["green"], [food_x, food_y, snake_block, snake_block])
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        our_snake(win, colors["black"], snake_block, snake_list)
        pygame.display.update()

        if x1 == food_x and y1 == food_y:
            food_x, food_y = generate_food_coordinates(width, height, snake_block)
            length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

def start_snake():
    print("Starting Snake...\n")
    game_loop()

if __name__ == "__main__":
    start_snake()
