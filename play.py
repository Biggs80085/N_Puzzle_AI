import pygame
import sys
import model
import ai
import time



pygame.init()
BOARD_SIZE = 3
goal_state = model.Puzzle(boardSize=BOARD_SIZE, shuffle = False)
PATHPUZZLE = []
# UI
size = width, height = 480, 480
screen = pygame.display.set_mode(size)
pygame.display.set_caption('{} Puzzle'.format(BOARD_SIZE**2-1))
FPS = 30

# Fonts
tileFont = pygame.font.SysFont("comicsansms", 72)

# Colors
black = (0,0,0)
borderColor = (92, 90, 86)
tileColor = (255, 253, 246)
fontColor = black

def gameLoop(n = 0, puzzle = None):
    global BOARD_SIZE
    global goal_state
    
    if n != 0:
        BOARD_SIZE = n
        puzzle = model.Puzzle(boardSize=BOARD_SIZE)
    BOARD_SIZE = puzzle.boardSize 
    
    
    goal_state = model.Puzzle(boardSize=BOARD_SIZE, shuffle = False)


    clock = pygame.time.Clock()
    
    
    
    print(puzzle)
    print("Go to the game and choose the type of search you want")
    print("i for IDA star search avec heuristic 1")
    print("j for IDA star search avec heuristic 2")
    print("a for A star search avec heuristic 1")
    print("z for A star search avec heuristic 2")
    print("b for Breadth-first search")
    print("s for shuffle")
    print("h for next move")
    

    while True:
        for event in pygame.event.get():
            handleInput(event, puzzle)
        
        drawPuzzle(puzzle)
        pygame.display.flip()
        clock.tick(FPS)





def handleInput(event, puzzle):
    global PATHPUZZLE
    
    if event.type == pygame.QUIT: sys.exit()
    elif event.type == pygame.KEYDOWN:
        # Shuffle puzzle
        if event.key == pygame.K_s:
            puzzle.shuffle()
        # IDA star search
        # Heuristic 1
        elif event.key == pygame.K_i:
            
            print("IDA star search heuristic 1 in progress ...")
            
            PATHPUZZLE = ai.ida_star(puzzle, goal_state, ai.z_puzzle_heuristic1)
        # Heuristic 2
        elif event.key == pygame.K_j:
            print("IDA star search heuristic 2 in progress ...")
            PATHPUZZLE = ai.ida_star(puzzle, goal_state, ai.z_puzzle_heuristic2)

        # Breadth-first search        
        elif event.key == pygame.K_b:
            print("Breadth-first search in progress ...")
            PATHPUZZLE = ai.bfs(puzzle)


        # A star search
        # Heuristic 1
        elif event.key == pygame.K_a:
            print("A star search heuristic 1 in progress ...")
            PATHPUZZLE = ai.a_star_search(puzzle, goal_state, ai.z_puzzle_heuristic1)  
        # Heuristic 2
        elif event.key == pygame.K_z:
            print("A star search heuristic 2 in progress ...")
            PATHPUZZLE = ai.a_star_search(puzzle, goal_state, ai.z_puzzle_heuristic2)
            

        # Next move   
        elif event.key == pygame.K_h:
            if(len(PATHPUZZLE)>0):
                if(PATHPUZZLE[0].direc != None):
                    puzzle.move(PATHPUZZLE[0].direc)
                PATHPUZZLE.pop(0)
    # Click
    elif event.type == pygame.MOUSEBUTTONUP:
        pos = pygame.mouse.get_pos()
        puzzleCoord = (pos[1]*puzzle.boardSize//height,
                        pos[0]*puzzle.boardSize//width)
        dir = (puzzleCoord[0] - puzzle.blankPos[0],
                puzzleCoord[1] - puzzle.blankPos[1])

        if dir == puzzle.RIGHT:
            puzzle.move(puzzle.RIGHT)
        elif dir == puzzle.LEFT:
            puzzle.move(puzzle.LEFT)
        elif dir == puzzle.DOWN:
            puzzle.move(puzzle.DOWN)
        elif dir == puzzle.UP:
            puzzle.move(puzzle.UP)
        

def readPuzzleFromFile(filename):
    with open(filename, 'r') as file:
        lines = file.read().split('\n')
       
        board = [list(map(int, line.split())) for line in lines]
        p = ''
        for i in board:
            p += '\t'.join(map(str,i))
            p += '\n'
        
        boardSize = len(board)
        blankPos = None
        for i in range(boardSize):
            for j in range(boardSize):
                if board[i][j] == 0:
                    blankPos = (i, j)
                    break
        puzzle = model.Puzzle(boardSize=boardSize)
        puzzle.board = board
        puzzle.blankPos = blankPos
        
    
    return puzzle
    


def drawPuzzle(puzzle):
    screen.fill(black)
    
    for i in range(puzzle.boardSize):
        for j in range(puzzle.boardSize):
            currentTileColor = tileColor
            numberText = str(puzzle[i][j])

            if puzzle[i][j] == 0:
                currentTileColor = borderColor
                numberText = ''

            rect = pygame.Rect(j*width/puzzle.boardSize,
                                i*height/puzzle.boardSize,
                                width/puzzle.boardSize,
                                height/puzzle.boardSize)

            pygame.draw.rect(screen, currentTileColor, rect)
            pygame.draw.rect(screen, borderColor, rect, 1)

            fontImg = tileFont.render(numberText, 1, fontColor)
            screen.blit(fontImg,
                        (j*width/puzzle.boardSize + (width/puzzle.boardSize - fontImg.get_width())/2,
                        i*height/puzzle.boardSize + (height/puzzle.boardSize - fontImg.get_height())/2))


if __name__ =="__main__":
    print("Welcome")
    choix = input("Play with your puzzle in file Y/N:")
    while choix != "Y" and choix != "N":
        choix = input("The value you typed is incorrect please try again:")
        
    if choix == "Y":
        puzzle=readPuzzleFromFile("puzzle")
        gameLoop(puzzle = puzzle)
    elif choix == "N":
        
    
        n = input("Type the value of N from the puzzle NxN:")
    
        while not n.isdigit() or int(n) < 2:
            n = input("The value you typed is incorrect please try again:")
        n = int(n)  
        gameLoop(n = n)
