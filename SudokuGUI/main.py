import pygame
import sys

from pygame.constants import K_SPACE
from pygame.draw import line
from pygame.rect import Rect

pygame.init()

board = [
    [0, 0, 0, 0, 0, 0, 0, 9, 0],
    [0, 0, 4, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 5, 7, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 8, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 7, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 6, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1]
]



class Grid:
    def __init__(self, rows, cols, width, height, surface):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.surface = surface
        self.gap = width // self.rows
        self.cubes = [[Cube(r, c, 60, 60, board[r][c]) for c in range(9)] for r in range(9)]

    def draw_cube_lines(self, row, col):
        thick = 1

        if row % 3 == 0 and row != 0:
            thick = 4

    def draw_lines(self):
        for i in range(9):
            thick = 1

            if i % 3 == 0 and i != 0:
                thick = 4

            # draw horizontal lines
            pygame.draw.line(self.surface, (0, 0, 0), (0, i * self.gap), (self.width, i * self.gap), thick)
            # draw vertical lines
            pygame.draw.line(self.surface, (0, 0, 0), (i * self.gap, 0), (i * self.gap, self.height), thick)

    # create board lines
    def draw_board(self):

        self.draw_cubes()
        self.draw_lines()

    def draw_cubes(self):
        for r in range(9):
            for c in range(9):
                self.cubes[r][c].draw_cube(self.surface)

    def find_empty(self, puzzle):
        for r in range(9):
            for c in range(9):
                if puzzle[r][c].value == 0:
                    return (r, c)

        return None

    def highlight_elements(self, elements, element, case):

        fnt = pygame.font.SysFont("comicsans", 30)

        for i in range(len(elements)):
            text = fnt.render(str(elements[i].value), 1, (0, 0, 0))
            self.surface.fill((255, 255, 51), elements[i].rect)
            self.draw_lines()
            self.surface.blit(text, (elements[i].col * 60 + (60 / 2 - text.get_width() / 2),
                                     elements[i].row * 60 + (60 / 2 - text.get_height() / 2)))

        element.redraw_cube(self.surface, case)

    def de_highlight_elements(self, elements, element):

        fnt = pygame.font.SysFont("comicsans", 30)

        for i in range(len(elements)):
            text = fnt.render(str(elements[i].value), 1, (0, 0, 0))
            self.surface.fill((255, 255, 255), elements[i].rect)
            self.draw_lines()
            self.surface.blit(text, (elements[i].col * 60 + (60 / 2 - text.get_width() / 2),
                                     elements[i].row * 60 + (60 / 2 - text.get_height() / 2)))

        # element.redraw_cube(self.surface, None)

    def row_values(self, row, puzzle):
        return [puzzle[row][c].value for c in range(9)]

    def col_values(self, col, puzzle):
        return [puzzle[r][col].value for r in range(9)]

    def is_valid(self, row, col, guess, puzzle):

        row_vals = self.row_values(row, puzzle)
        if guess in row_vals:
            return False

        # check validity for col

        col_vals = self.col_values(col, puzzle)
        if guess in col_vals:
            return False

        # check validity for sub-dimensions
        row_start = (row // 3) * 3
        col_start = (col // 3) * 3

        for r in range(row_start, row_start + 3):
            for c in range(col_start, col_start + 3):
                if puzzle[r][c].value == guess:
                    return False

        return True

    def solve_sudoku(self, surface, puzzle):
        # find available cube
        coords = self.find_empty(puzzle)

        # board does not have empty cube
        if coords == None:
            return True

        row, col = coords

        # guess value for picked board cube
        for guess in range(1, 10):
            if self.is_valid(row, col, guess, puzzle):
                puzzle[row][col].set_value(guess)
                self.highlight_elements([puzzle[row][c] for c in range(9)], puzzle[row][col], True)
                self.highlight_elements([puzzle[r][col] for r in range(9)], puzzle[row][col], True)
                pygame.display.update()
                pygame.time.delay(100)
                self.de_highlight_elements([puzzle[row][c] for c in range(9)], puzzle[row][col])
                self.de_highlight_elements([puzzle[r][col] for r in range(9)], puzzle[row][col])

                if self.solve_sudoku(surface, puzzle):
                    return True

                puzzle[row][col].set_value(0)
                self.highlight_elements([puzzle[row][c] for c in range(9)], puzzle[row][col], False)
                self.highlight_elements([puzzle[r][col] for r in range(9)], puzzle[row][col], False)
                pygame.display.update()
                pygame.time.delay(100)
                self.de_highlight_elements([puzzle[row][c] for c in range(9)], puzzle[row][col])
                self.de_highlight_elements([puzzle[r][col] for r in range(9)], puzzle[row][col])

        return False


class Cube:
    def __init__(self, row, col, width, height, value):
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.value = value
        self.rect = None

    def draw_cube(self, surface):
        gap = 540 / 9
        x = self.col * gap
        y = self.row * gap

        fnt = pygame.font.SysFont("comicsans", 30)
        text = fnt.render(str(self.value), 1, (0, 0, 0))
        self.rect = pygame.draw.rect(surface, (255, 255, 255), (x, y, gap, gap))

        surface.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))

    def redraw_cube(self, surface, success):
        gap = 540 / 9
        x = self.col * gap
        y = self.row * gap

        bg_color = (60, 255, 100)

        if not success:
            bg_color = (255, 100, 60)

        surface.fill(bg_color, self.rect)

        fnt = pygame.font.SysFont("comicsans", 30)
        text = fnt.render(str(self.value), 1, (0, 0, 0))
        surface.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))

    def set_value(self, value):
        self.value = value


def main():
    width = 540
    height = 540
    # create screen

    screen = pygame.display.set_mode((width, height))

    pygame.display.set_caption("Sudoku Game Solver")

    grid = Grid(9, 9, width, height, screen)

    grid.draw_board()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == K_SPACE:
                    grid.solve_sudoku(screen, grid.cubes)
        pygame.display.update()


main()
pygame.quit()