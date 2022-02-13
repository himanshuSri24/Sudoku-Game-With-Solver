import sys

import pygame
import requests  # API to get solvable sudoku boards

pygame.font.init()
pygame.display.init()
pygame.init()

# Constants
WIDTH, HEIGHT = 550, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
IP_COLOR = (128, 128, 128)
BG_COLOR = (0, 204, 255)
BUFFER, X_BUFFER, Y_BUFFER = 5, 16, 3

# Global Variables
pygame.display.set_caption("Sudoku Version 1.0")
response = requests.get("https://sugoku.herokuapp.com/board?difficulty=easy")
board = response.json()['board']
og_board = [[board[x][y] for y in range(len(board[0]))] for x in range(len(board))]
OG_FONT = pygame.font.SysFont('comicsans', 35)
OG_FONT_SMALL = pygame.font.SysFont('comicsans', 20)
OG_FONT_SMALL_2 = pygame.font.SysFont('comicsans', 20)
OG_FONT_BIG = pygame.font.SysFont('comicsans', 50)


# Fill the initial values in the sudoku


def fill_given_values():
    for i in range(0, len(board[0])):
        for j in range(0, len(board[0])):
            if 0 < og_board[i][j] < 10:
                value = OG_FONT.render(str(og_board[i][j]), True, BLACK)
                WIN.blit(value, ((j + 1) * 50 + X_BUFFER, (i + 1) * 50 + Y_BUFFER))
    pygame.display.update()


# Draw the board, or to say, the grid
def fill_ip_values():
    for i in range(0, len(board[0])):
        for j in range(0, len(board[0])):
            if 0 < board[i][j] < 10:
                value = OG_FONT.render(str(board[i][j]), True, IP_COLOR)
                WIN.blit(value, ((j + 1) * 50 + X_BUFFER, (i + 1) * 50 + Y_BUFFER))


def draw_board():
    heading = OG_FONT_SMALL.render("Sudoku Game With Solver", True, BLACK)
    help1 = OG_FONT_SMALL_2.render("Click on box and enter no.", True, BLACK)
    help2 = OG_FONT_SMALL_2.render("Enter 0 to clear cell", True, BLACK)
    help3 = OG_FONT_SMALL_2.render("Click ENTER to check your answer", True, BLACK)
    WIN.fill(BG_COLOR)
    WIN.blit(heading, (WIDTH // 2 - heading.get_width() // 2, 7))
    footer = OG_FONT_SMALL.render("Press SPACEBAR to solve automatically", True, BLACK)
    WIN.blit(help1, (20, 510))
    WIN.blit(help2, (WIDTH - help2.get_width() - 20, 510))
    WIN.blit(help3, (WIDTH // 2 - help3.get_width() // 2, 540))
    WIN.blit(footer, (WIDTH // 2 - footer.get_width() // 2, HEIGHT - 30))
    draw_borders()
    fill_ip_values()
    fill_given_values()
    pygame.display.update()


def draw_borders():
    for i in range(0, 10):
        if i % 3 == 0:
            pygame.draw.line(WIN, BLACK, (50 + 50 * i, 50), (50 + 50 * i, 500), 3)
            pygame.draw.line(WIN, BLACK, (50, 50 + 50 * i), (500, 50 + 50 * i), 3)
        pygame.draw.line(WIN, BLACK, (50 + 50 * i, 50), (50 + 50 * i, 500), 1)
        pygame.draw.line(WIN, BLACK, (50, 50 + 50 * i), (500, 50 + 50 * i), 1)


def insert_value(position):
    j, i = position[0] - 1, position[1] - 1
    # print(i, j)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                # Either the place we enter a value has a fixed val
                # or there is no value, so we just render the current value as text and input it
                # Or maybe there was a value already entered by user, so remove it, then fill new value
                if og_board[i][j] != 0:
                    # print(og_board[i][j])
                    return
                if event.key == 48:
                    # print("0 Pressed")
                    board[i][j] = event.key - 48
                    pygame.draw.rect(WIN, BG_COLOR,
                                     pygame.Rect((i + 1) * 50 + BUFFER, (j + 1) * 50 + BUFFER, 50 - BUFFER, 50
                                                 - BUFFER))
                    draw_board()
                    pygame.display.update()
                if 0 < event.key - 48 < 10:
                    # print("Some number pressed")
                    # print("Original Value : ", og_board[i][j])
                    board[i][j] = event.key - 48
                    # print("New value : ", og_board[i][j])
                    pygame.draw.rect(WIN, BG_COLOR,
                                     pygame.Rect((i + 1) * 50 + BUFFER, (j + 1) * 50 + BUFFER, 50 - BUFFER, 50
                                                 - BUFFER))
                    new_value = OG_FONT.render(str(event.key - 48), True, IP_COLOR)
                    WIN.blit(new_value, ((j + 1) * 50 + X_BUFFER, (i + 1) * 50 + Y_BUFFER))
                    draw_board()
                    pygame.display.update()
                    return
                return


#
# def draw_selection(position):
#     j, i = position[0]//50, position[1]//50
#     start_x, start_y = 50*i, 50*j
#     draw_board()
#     pygame.draw.line(WIN, RED, (start_x, start_y), (start_x, start_y + 50), 3)
#     pygame.draw.line(WIN, RED, (start_x, start_y), (start_x + 50, start_y), 3)
#     pygame.display.update()


def isEmpty(num):
    if num == 0:
        return True
    return False


def isValid(position, num):
    # Check row
    for i in range(0, len(og_board[0])):
        if og_board[position[0]][i] == num:
            return False

    # Check column
    for i in range(0, len(og_board[0])):
        if og_board[i][position[1]] == num:
            return False

    x = position[0] // 3 * 3
    y = position[1] // 3 * 3

    for i in range(0, 3):
        for j in range(0, 3):
            if og_board[x + i][y + j] == num:
                return False
    return True


solved = 0


def isValidUser(position, num):
    # Check row
    for i in range(0, len(board[0])):
        if board[position[0]][i] == 0:
            # print(" 0 ", position)
            return False
        if i == position[1]:
            continue
        if i != position[1] and board[position[0]][i] == num:
            # print(" row ", i, " ")
            return False

    # Check column
    for i in range(0, len(board[0])):
        if board[i][position[1]] == 0:
            return False
        if i == position[0]:
            continue
        if board[i][position[1]] == num:
            # print(" column ", i, " ")
            return False

    x = position[0] // 3 * 3
    y = position[1] // 3 * 3

    for i in range(0, 3):
        for j in range(0, 3):
            if board[x + i][y + j] == 0:
                return False
            if x + i == position[0] and y + j == position[1]:
                continue
            if board[x + i][y + j] == num:
                # print(" grid ", i, " ", j)
                return False
    return True


def sudoku_solver():
    for i in range(0, len(og_board[0])):
        for j in range(0, len(og_board[0])):
            if isEmpty(og_board[i][j]):
                for k in range(1, 10):
                    if isValid((i, j), k):
                        og_board[i][j] = k
                        pygame.draw.rect(WIN, BG_COLOR, (
                            (j + 1) * 50 + BUFFER, (i + 1) * 50 + BUFFER, 50 - 2 * BUFFER, 50 - 2 * BUFFER))
                        value = OG_FONT.render(str(k), True, (0, 0, 0))
                        WIN.blit(value, ((j + 1) * 50 + 15, (i + 1) * 50))
                        pygame.display.update()
                        pygame.time.delay(2)

                        sudoku_solver()

                        # Exit condition
                        global solved
                        if solved == 1:
                            return

                        og_board[i][j] = 0
                        pygame.draw.rect(WIN, BG_COLOR, (
                            (j + 1) * 50 + BUFFER, (i + 1) * 50 + BUFFER, 50 - 2 * BUFFER, 50 - 2 * BUFFER))
                        pygame.display.update()
                        # pygame.time.delay(10)
                return
    solved = 1


# Main function
def displayEndGame(winner_text):
    winner = OG_FONT_SMALL.render(winner_text, True, RED)
    WIN.fill(BG_COLOR)
    WIN.blit(winner, (WIDTH // 2 - winner.get_width() // 2, HEIGHT // 2 - winner.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(5000)
    pygame.quit()
    sys.exit()


def main():
    draw_board()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                position = pygame.mouse.get_pos()
                #  draw_selection(position)
                insert_value((position[0] // 50, position[1] // 50))
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    sudoku_solver()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    winner_text = "You WIN!!!"
                    if solved == 1:
                        winner_text = "You used our algo, so I guess you won!"
                    else:
                        for i in range(0, 9):
                            for j in range(0, 9):
                                pos = (i, j)
                                #  print(" og ", og_board[i][j], end=" ")
                                if not isValidUser(pos, board[i][j]):
                                    winner_text = "You LOSE :("
                                    break
                            if winner_text == "You LOSE :(":
                                break
                            # print("")
                    displayEndGame(winner_text)


main()

if __name__ == "__main__":
    main()
