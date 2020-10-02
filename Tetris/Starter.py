from tkinter import Canvas, Label, Tk, StringVar, Button, LEFT
from random import choice, randint

class GameCanvas(Canvas):
    def clean_line(self, box_to_delete):
        for box in box_to_delete:
            self.delete(box)
        self.update()
    def drop_box(self, boxes_to_drop):
        for box in boxes_to_drop:
            self.move(box, 0, Tetris.BOX_SIZE)
        self.update()
    def completed_lines(self, y_coords):
        cleaned_lines = 0
        y_coords =sorted(y_coords)
        for y in y_coords:
            if sum(1 for box in self.find_withtag('game') if self.coords(box)[3] == y) == \
                ((Tetris.GAME_WIDTH - 20) // Tetris.BOX_SIZE):
                self.clean_line([box 
                                for box in self.find_withtag('game') 
                                if self.coords(box)[3] == y])
                self.drop_box([box 
                                for box in self.find_withtag('game') 
                                if self .coords(box)[3] < y])
                cleaned_lines += 1
        return cleaned_lines
    
    def game_board(self):
        board = [[0] * ((Tetris.GAME_WIDTH - 20) // Tetris.BOX_SIZE)\
                for _ in range(Tetris.Game_HEIGHT //  Tetris.BOX_SIZE)]
        for box in self.find_withtag('game'):
            x, y, _, _ = self.coords(box)
            board[int(y // Tetris.BOX_SIZE)][int(x // Tetris.BOX_SIZE)] = 1
        return board
    def boxes(self):
        return self.find_withtag('game') == self.find_withtag(fill='blue')

class Shape():
    def __init__(self, coords = None):
        if not coords:
            self.__coords = choice(Tetris.SHAPES)
        else:
            self.__coords = coords
    
    @property
    def coords(self):
        return self.__coords

    def rotate(self):
        self.__coords = self.__rotate()
    def rotate_directions(self):
        rotated = self.__rotate()
        directions = [(rotated[i][0] - self.__coords[i][0],
                       rotated[i][0] - self.__coords[i][0]) for i in range(len(self.__coords))]

        return directions

    @property
    def matrix(self):
        return[[1 if (j, i) in self.__coords else 0 \
            for i in range(max(self.__coords, key=lambda x: x[0])[0] + 1)] \
            for i in range(max(self.__coords, key=lambda x: x[1])[1] + 1)]
    
    def drop(self, board, offset):
        off_x, off_y = offset
        last_level = len(board) - len(self.matrix)
        for level in range(off_y, last_level):
            for i in range(len(self.matrix)):
                for j in range(len(self.matrix[0])):
                    if board[level+i][off_x+j] == 1 and self.matrix[i][j] == 1:
                        return level -1
        return last_level
    
    def __rotate(self):
        max_x = max(self.__coords, key=lambda x: x[0])[0]
        new_original = (max_x, 0)

        rotated = [(new_original[0] - coord[1]
                    new_original[1] - coord[0]) for coord in self.__coords]
                
        min_x = min(rotated, key=lambda x: x[0][0])