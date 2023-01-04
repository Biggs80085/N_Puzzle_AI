from random import choice
from copy import deepcopy
class Puzzle:

    UP = (1,0)
    DOWN = (-1,0)
    LEFT = (0,1)
    RIGHT = (0,-1)
    DIRECTIONS = [UP,DOWN,LEFT,RIGHT]
    
    def __init__(self, boardSize = 3, shuffle = True):
        self.boardSize = boardSize
        self.board = [[0]*boardSize for i in range(boardSize)]
        self.blankPos = (boardSize-1, boardSize-1)
        self.cost = 0
        self.heuristic = 0
        self.direc = None
        for i in range(boardSize):
            for j in range(boardSize):
                self.board[i][j] = i * boardSize + j + 1
        
        # 0 represents blank square, init in bottom right corner of board
        self.board[self.blankPos[0]][self.blankPos[1]] = 0

        if shuffle:
            self.shuffle()

            
        

    def __str__(self):
        outStr = ''
        for i in self.board:
            outStr += '\t'.join(map(str,i))
            outStr += '\n'
        return outStr

    def __getitem__(self, key):
        return self.board[key]


    def shuffle(self):
        nShuffles = 1000

        for i in range(nShuffles):
            dir = choice(self.DIRECTIONS)
            self.move(dir)


    def move(self, dir):
        newBlankPos = (self.blankPos[0] + dir[0], self.blankPos[1] + dir[1])

        if newBlankPos[0] < 0 or newBlankPos[0] >= self.boardSize \
            or newBlankPos[1] < 0 or newBlankPos[1] >= self.boardSize:
            return False

        self.board[self.blankPos[0]][self.blankPos[1]] = self.board[newBlankPos[0]][newBlankPos[1]]
        self.board[newBlankPos[0]][newBlankPos[1]] = 0
        self.blankPos = newBlankPos
        return True

    # Check if is a goal state
    def checkWin(self):
        for i in range(self.boardSize):
            for j in range(self.boardSize):
                if self.board[i][j] != i * self.boardSize + j + 1 and self.board[i][j] != 0:
                    return False

        return True

    # Check if the puzzle is in the list
    def checkPuzzleList(self, lists):
        for l in lists:
            if(self.board == l.board):
                return False

        return True

    # Find the puzzle in the list and return it
    def findPuzzle(self, lists):
        for l in lists:
            if(self.board == l.board):
                return l

        return None



    def _swap(self, x1, y1, x2, y2 ):
         puzzle_copy = deepcopy(self)
         puzzle_copy[x1][y1], puzzle_copy[x2][y2] = puzzle_copy[x2][y2], puzzle_copy[x1][y1]
         puzzle_copy.direc = (x2-x1, y2-y1)
         return puzzle_copy


    def _get_coordinates(self, tile, position=None):
        
        # Returns the i, j coordinates for a given tile
        
        if not position:
            position = self.board

        for i in range(self.boardSize):
            for j in range(self.boardSize):
                if position[i][j] == tile:
                    return i, j

        return RuntimeError('Invalid tile value')

    def get_moves(self):
        
        # Returns a list of all the possible moves
        
        moves = []
        i, j = self._get_coordinates(0)  # blank space

        if i > 0:
            moves.append(self._swap(i, j, i - 1, j))  # move up

        if j < self.boardSize - 1:
            moves.append (self._swap(i, j, i, j + 1))  # move right
            
        if j > 0:
            moves.append (self._swap(i, j, i, j - 1))  # move left
            
        if i < self.boardSize - 1:
            moves.append (self._swap(i, j, i + 1, j))  # move down
            
        return moves


    def setCost(self,c):
        self.cost = c

    def setHeuristic(self, h):
        self.heuristic = h


