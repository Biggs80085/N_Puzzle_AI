import numpy as np
from collections import deque
from math import inf
from time import perf_counter_ns
import time
import sys
import matplotlib.pyplot as plt
import numpy as np

NANO_TO_SEC = 1000000000
STARTTIME = 0
TIMER = -1
LENFRONTIER = []


# Heuristic 1

def z_puzzle_heuristic1(puzzle, goal_state):
    # Initialize the variable that will contain the result of the heuristic
    result = 0
    # For each row and column of the puzzle
    for i in range(puzzle.boardSize):
        for j in range(puzzle.boardSize):
            # If the puzzle square does not match the goal state puzzle square and is not empty
            if puzzle.board[i][j] != goal_state.board[i][j] and puzzle.board[i][j] != 0:
                result += 1
    return result






# Heuristic 2

def manhattan_distance(tile, goal_pos):
  # Calculate the Manhattan distance between the current position of the tile
  # and its goal position
  dx = abs(tile[0] - goal_pos[0])
  dy = abs(tile[1] - goal_pos[1])
  return dx + dy

def z_puzzle_heuristic2(puzzle, goal_state):
  # Calculate the heuristic value for the current state of the puzzle
  heuristic_value = 0
  for i in range(puzzle.boardSize):
    for j in range(puzzle.boardSize):
      tile = puzzle.board[i][j]
      if tile != 0:
        # Find the goal position for the current tile
        goal_pos = np.argwhere(np.array(goal_state.board) == tile)[0]

        # Add the Manhattan distance between the current position and the goal position
        # to the heuristic value
        heuristic_value += manhattan_distance((i, j), goal_pos)
  return heuristic_value








# Calculate f(x) = g(x) + h(x)

def sumG(puzzle):
    return puzzle.cost + puzzle.heuristic








# Sort Frontier

def sortFrontier(lists):
    # Initialize the list that will contain the sorted elements
    frontier = []
    # For each element in the input list
    for i in range(len(lists)):
        # Initialize the minimum with the first element of the list
        min = lists[0]
        for l in lists:
            # If the current element is lower than the current minimum
            if sumG(l) < sumG(min):
                min = l
        lists.remove(min)
        # Add the minimum to the sorted list
        frontier.append(min)
    return frontier



# Return Max Value

def maxValue(lists):
    maxV = 0

    for i in range(len(lists)):
        if maxV < lists[i]:
            maxV = lists[i]
    return maxV








# Path from start_state to goal_state

def reconstruct_path(came_from, current):
    # Initialize the path with the current node
    path = [current]
    # While the current node has a predecessor
    while current in came_from:
        # Set the current node to its predecessor
        current = came_from[current]
        # Insert the current node at the beginning of the path
        path.insert(0, current)
    return path









# Breadth-first search

def bfs(puzzle, timer = -1):
    global STARTTIME
    global TIMER
    global LENFRONTIER
    STARTTIME = time.time()
    TIMER = timer

    LENFRONTIER = [];
    
    # If the puzzle is already solved, return it
    if puzzle.checkWin()==True:
        return puzzle
    # Start the timer
    t1 = perf_counter_ns()
    # Initialize the queue with the initial puzzle
    frontier = deque([puzzle])
    # Initialize the list of explored nodes
    explored = []
    # Initialize the dictionary that will store the predecessor of each node
    came_from = {}

    # While there are still nodes to explore
    while True:

        if TIMER != -1:
            elapsed_time = time.time() - STARTTIME
            if elapsed_time > TIMER:
                return []
        
        # If the queue is empty, return failure
        if not frontier:
            return None  # Failure
        LENFRONTIER.append(len(frontier))
        node = frontier.popleft()
        explored.append(node)
        # Get the list of possible moves from the current node
        moves = node.get_moves()
        for move in moves :
            child = move
            # If the child node has not been explored or added to the queue yet
            if child.checkPuzzleList(explored) and child.checkPuzzleList(frontier):
                came_from[child] = node
                # If the child node is the goal state
                if child.checkWin()==True:
                    # Reconstruct the path from the start node to the child node
                    path = reconstruct_path(came_from, child)
                    # Calculate the elapsed time
                    tDelta = (perf_counter_ns()-t1)/NANO_TO_SEC
                    print("The max value of frontier : ",maxValue(LENFRONTIER))
                    print("Took {} seconds to find a solution of {} moves".format(tDelta, len(path)-1))
                    return path
                    
                frontier.append(child)










# A Star search

def a_star_search(puzzle, goal_state, heuristicFunction, timer = -1):
    global STARTTIME
    global TIMER
    global LENFRONTIER
    STARTTIME = time.time()
    TIMER = timer

    LENFRONTIER = [];
    
    # If the puzzle is already solved, return it
    if puzzle.checkWin()==True:
        return puzzle
    # Start the timer
    t1 = perf_counter_ns()
    # Initialize the dictionary that will store the predecessor of each node
    came_from = {}
    # Initialize the queue with the initial puzzle
    frontier = deque([puzzle])
    # Initialize the list of explored nodes
    explored = []
    # Set the heuristic value of the initial puzzle
    frontier[0].setHeuristic(heuristicFunction(frontier[0], goal_state))

    # While there are still nodes to explore
    while True:

        if TIMER != -1:
            elapsed_time = time.time() - STARTTIME
            if elapsed_time > TIMER:
                return []
    
        # If the queue is empty, return failure
        if not frontier:
            return None
        LENFRONTIER.append(len(frontier))
        node = frontier[0]
        del frontier[0]
        explored.append(node)

        # If the current node is the goal state
        if node.checkWin()==True:
            # Reconstruct the path from the start node to the current node
            path = reconstruct_path(came_from, node)
            # Calculate the elapsed time
            tDelta = (perf_counter_ns()-t1)/NANO_TO_SEC
            print("The max value of frontier : ",maxValue(LENFRONTIER))
            print("Took {} seconds to find a solution of {} moves".format(tDelta, len(path)-1))
            return path
        
        # Get the list of possible moves from the current node
        moves = node.get_moves()

        # For each possible move
        for move in moves :
            child = move
            # Set the cost of the child node to the cost of the current node plus
            child.setCost(node.cost+1)
            # Set the heuristic value of the child node
            child.setHeuristic(heuristicFunction(child, goal_state))
            
            # If the child node is not in the explored list
            if child.checkPuzzleList(explored):
                # If the child node is not in the frontier queue
                if child.checkPuzzleList(frontier):
                    came_from[child] = node
                    frontier.append(child)
                    
                # If the child node is already in the frontier queue
                else:
                    # Find the element in the queue with the same puzzle state
                    elm = child.findPuzzle(frontier)

                    # If the cost of the child node is lower than the cost of the element
                    if(sumG(elm) > sumG(child)):
                        frontier.remove(elm)
                        came_from[child] = node
                        frontier.append(child)
                # Sort the frontier queue according to the cost of the nodes
                frontier = sortFrontier(frontier)








# IDA Star search

def ida_star(puzzle, goal_state, heuristicFunction, timer = -1):
    global STARTTIME
    global TIMER
    global LENFRONTIER
    STARTTIME = time.time()
    TIMER = timer
    LENFRONTIER = []
    # Set the initial bound to the heuristic value of the initial puzzle
    bound = heuristicFunction(puzzle, goal_state)
    
    # Set the heuristic value of the initial puzzle
    puzzle.setHeuristic(heuristicFunction(puzzle, goal_state))
    
    # Set the path to the initial puzzle
    path = [puzzle]
    LENFRONTIER.append(len(path))
    # Start the timer
    t1 = perf_counter_ns()
    
    # While the solution has not been found
    while True:
        
        # Call the search function with the current path, cost, bound, and heuristic function
        t = search(path, 0, bound, goal_state, heuristicFunction)

        # If the search function returns "FOUND", return the path
        if t == "FOUND":
            tDelta = (perf_counter_ns()-t1)/NANO_TO_SEC
            print("The max value of frontier : ",maxValue(LENFRONTIER))
            print("Took {} seconds to find a solution of {} moves".format(tDelta, len(path)-1))
            return path
        if t == inf:
            return "NOT_FOUND"
        if t == "KILL":
            return []
        
        bound = t

def search(path, cost, bound, goal_state, heuristicFunction):

    global LENFRONTIER
    
    if TIMER != -1:
        elapsed_time = time.time() - STARTTIME
        if elapsed_time > TIMER:
            return "KILL"
    

    try:
        # Set the current node to the last element in the path
        node = path[-1]

        # Set the cost of the current node to the given cost
        node.setCost(cost)
    
        # Calculate the value of f for the current node
        f = sumG(node)
    
        # If f is greater than the bound, return f
        if f > bound:
            return f

        # If the current node is a goal state, return "FOUND"
        if node.checkWin()==True:
            return "FOUND"

        # Set the minimum value to infinity
        min_val = inf

        # Get the possible moves from the current node
        moves = node.get_moves()

        # For each possible move
        for move in moves:
            if move not in path:
                child = move

                # Set the cost of the child node to the cost of the current node plus 1
                child.setCost(node.cost+1)

                # Set the heuristic value of the child node
                child.setHeuristic(heuristicFunction(child, goal_state))
                path.append(child)
                LENFRONTIER.append(len(path))
                # Call the search function with the updated path, cost, bound, and heuristic function
                t = search(path, child.cost, bound, goal_state, heuristicFunction)

                # If the search function returns "FOUND", return "FOUND"
                if t == "FOUND":
                    return "FOUND"

                # If the value returned by the search function is lower than the minimum value
                if t < min_val:
                    min_val = t
                path.pop()
        return min_val
    except:
        pass







# Loading ...
# Bideractional search

def bidirectional_search(start_state, goal_state):
    # initialize the search fronts
    forward_front = {start_state}
    backward_front = {goal_state}
    
    # initialize the paths
    forward_path = {start_state: None}
    backward_path = {goal_state: None}
    
    while forward_front and backward_front:
        # search the forward front
        if len(forward_front) <= len(backward_front):
            next_front = set()
            for state in forward_front:
                for neighbor in state.get_moves():
                    if neighbor in backward_path:
                        # the paths have met, so we can construct the path from start to end
                        path = []
                        while state is not None:
                            path.append(state)
                            state = forward_path[state]
                        path.reverse()
                        state = neighbor
                        while state is not None:
                            path.append(state)
                            state = backward_path[state]
                        return path
                    if neighbor not in forward_path:
                        forward_path[neighbor] = state
                        next_front.add(neighbor)
            forward_front = next_front
        
        # search the backward front
        if len(backward_front) <= len(forward_front):
            next_front = set()
            for state in backward_front:
                for neighbor in state.get_moves():
                    if neighbor in forward_path:
                        # the paths have met, so we can construct the path from start to end
                        path = []
                        while state is not None:
                            path.append(state)
                            state = backward_path[state]
                        path.reverse()
                        state = neighbor
                        while state is not None:
                            path.append(state)
                            state = forward_path[state]
                        return path
                    if neighbor not in backward_path:
                        backward_path[neighbor] = state
                        next_front.add(neighbor)
            backward_front = next_front
    
    # the search fronts have converged and no path was found
    return None




                    


