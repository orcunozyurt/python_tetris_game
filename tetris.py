from random import randint
import sys
import select
import math

BRICK = "*"
SPACE = " "
NEWLINE = "\n"



def concatenate(generator):
    return ''.join(list(generator))


def percentage(numerator, denominator):
    value = float(numerator)*100/float(denominator)
    return math.ceil(value*100)/100


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def reverse_rows(matrix):
    return [list(reversed(row)) for row in matrix]


def rotate_90_clockwise(matrix):
    # return [list(reversed(row)) for row in zip(*matrix)]
    return reverse_rows(transpose(matrix))


def rotate_90_counter_clockwise(matrix):
    return transpose(reverse_rows(matrix))


def paint_cell(cell):
    return BRICK if cell == 1 else SPACE


class TBlock(object):
    """
    Tetris blocks available are defined here!!
    """
    

    def __init__(self, top=None, left=None):
        """
        Definition of the blocks
        name_of_the_block = [[matrix rows of block],width,height]
        """
        matrix_horizontal_block=[[[1,1,1,1]],4,1]  
        matrix_l_block=[[[0,1],[0,1],[1,1]],2,3]
        matrix_l2_block=[[[1,0],[1,0],[1,1]],2,3]
        matrix_z_block=[[[0,1],[1,1],[1,0]],2,3]
        matrix_square_block=[[[1,1],[1,1]],2,2]
        
        # Add the blocks in a tuple 
        
        matrix_tuple=(matrix_horizontal_block,matrix_l_block,matrix_l2_block,matrix_z_block,matrix_square_block,)
       
        # Block will be randomly picked from matrix_tuple
        picker_int = randint(0,4)
        
        matrix_picked = matrix_tuple[picker_int]
        self.top = top
        self.left = left
        self.height =matrix_picked[2]
        self.width = matrix_picked[1]
        self.matrix = matrix_picked[0]
            
        

    def rotate_clockwise(self):
        self.matrix = rotate_90_clockwise(self.matrix)

    def rotate_counter_clockwise(self):
        self.matrix = rotate_90_counter_clockwise(self.matrix)


class Board(object):
    """
    Board is structured here
    """

    def __init__(self, height=20, width=20):
        self.height = height
        self.width = width
        self.matrix = [
            [1] + [0 for _ in range(width)] + [1]
            for __ in range(height)] + [[1 for _ in range(width + 2)]]

    def __str__(self):
        """
        Defining what to draw on board
        """
        string = concatenate(paint_cell(cell) for cell in self.matrix[0])
        for row in self.matrix[1:-1]:
            string += NEWLINE
            string += concatenate(paint_cell(cell) for cell in row)
        string += NEWLINE
        string += concatenate(paint_cell(cell) for cell in self.matrix[-1])
        return string

    def can_fit(self, block, row, col):
        """
        Checks the availability of the move
        """
        try:
            return all(c + self.matrix[row + ri][col + ci] in (0, 1)
                       for ri, r in enumerate(block.matrix)
                       for ci, c in enumerate(r))
        except IndexError:
            return False

    def place(self, block, y, x):
        for ri, r in enumerate(block.matrix):
            for ci, c in enumerate(r):
                self.matrix[y + ri][x + ci] += c
        block.top = y
        block.left = x

    def remove(self, block, y, x):
        for ri, r in enumerate(block.matrix):
            for ci, c in enumerate(r):
                self.matrix[y + ri][x + ci] -= c
        block.top = y
        block.left = x

    @property
    def filled_percentage(self):
        filled = 0
        total = 0
        for row in self.matrix[:-1]:
            for cell in row[1:-1]:
                if cell > 0:
                    filled += 1
                total += 1
        return percentage(filled, total)


def move_right(board, block):
    board.remove(block, block.top, block.left)
    if board.can_fit(block, block.top, block.left+1):
        board.place(block, block.top, block.left+1)
    else:
        print "Out of board! Please make a valid move."
        board.place(block, block.top, block.left)


def move_left(board, block):
    board.remove(block, block.top, block.left)
    if board.can_fit(block, block.top, block.left-1):
        board.place(block, block.top, block.left-1)
    else:
        print "Out of board! Please make a valid move."
        board.place(block, block.top, block.left)


def rotate_clockwise(board, block):
    board.remove(block, block.top, block.left)
    block.rotate_clockwise()
    if board.can_fit(block, block.top, block.left):
        board.place(block, block.top, block.left)
    else:
        print "Out of board! Please make a valid move."
        block.rotate_counter_clockwise()
        board.place(block, block.top, block.left)


def rotate_counter_clockwise(board, block):
    board.remove(block, block.top, block.left)
    block.rotate_counter_clockwise()
    if board.can_fit(block, block.top, block.left):
        board.place(block, block.top, block.left)
    else:
        print "Out of board! Please make a valid move."
        block.rotate_clockwise()
        board.place(block, block.top, block.left)


def move_down(board, block):
    board.remove(block, block.top, block.left)
    if board.can_fit(block, block.top+1, block.left):
        board.place(block, block.top+1, block.left)
    else:
        board.place(block, block.top, block.left)
        raise Exception


def place_on_top(board, block):
    top = 0
    left = randint(1, board.width-block.width)
    if board.can_fit(block, top, left):
        board.place(block, top, left)
    else:
        raise Exception




if __name__ == '__main__':
   
    h = 20
    w = 20
    prompt = """
        Enter
        a followed by Enter for moving left,
        d followed by Enter for moving right,
        w followed by Enter for counter clockwise,
        s followed by Enter for clockwise
        and just Enter for staying in same column.
        Press any key when you
        are ready to start
        """
    raw_input(prompt)

    board = Board(h, w)
    block = TBlock()
    place_on_top(board, block)
    print board
    x = raw_input('Enter a for moving left, d for moving right, w for counterclockwise, s for clockwise and any other for staying in same column: ')
    while x != 'EOF':
        try:
            move_down(board, block)
        except:
            block = TBlock()
            try:
                place_on_top(board, block)
            except:
                print "GAME OVER"
                print "You scored %s/10000" % int(
                    board.filled_percentage * 100)
                break
        if x is not None:
            if x == 'a':
                move_left(board, block)
            elif x == 'd':
                move_right(board, block)
            elif x == 'w':
                rotate_counter_clockwise(board, block)
            elif x == 's':
                rotate_clockwise(board, block)
        print board
        x = raw_input('Enter a for moving left, d for moving right, w for counterclockwise, s for clockwise and any other for staying in same column: ')
