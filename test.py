import play
import time
import model
import ai
import threading

TIMER = 6
N = 30

startPuzzle = []
goalPuzzle = []

for i in range(N):
    startPuzzle.append(model.Puzzle(boardSize = (i+2)))
    goalPuzzle.append(model.Puzzle(boardSize = (i+2), shuffle = False))

print("----------------------------------------")
print("Breadth-first search execution")
count= 0
while True:  
    path = ai.bfs(startPuzzle[count], TIMER)
    
    if len(path) > 0:
        """for p in path:
            print(p)"""
        count += 1
    else:
        break    
    
print("Breadth-first search has reached N =",count+1)
print("Breadth-first search finish")
print("----------------------------------------")

print("A star search heuristic 1 execution")
count = 0
while True:   
    path = ai.a_star_search(startPuzzle[count], goalPuzzle[count], ai.z_puzzle_heuristic1, TIMER)
    if len(path) > 0:
        """for p in path:
            print(p)"""
        count += 1
    else:
        break    
    
print("A star search heuristic 1 has reached N =", count+1)
print("A star search heuristic 1 finish")
print("----------------------------------------")

print("A star search heuristic 2 execution")
count = 0
while True:   
    path = ai.a_star_search(startPuzzle[count], goalPuzzle[count], ai.z_puzzle_heuristic2, TIMER)
    if len(path) > 0:
        """for p in path:
            print(p)"""
        count += 1
    else:
        break    
    
print("A star search heuristic 2 has reached N =", count+1)
print("A star search heuristic 2 finish")
print("----------------------------------------")

print("IDA star search heuristic 1 execution")
count = 0
while True:   
    path = ai.ida_star(startPuzzle[count], goalPuzzle[count], ai.z_puzzle_heuristic1, TIMER)
    if len(path) > 0:
        """for p in path:
            print(p)"""
        count += 1
    else:
        break    
    
print("IDA star search heuristic 1 has reached N =", count+1)
print("IDA star search heuristic 1 finish")
print("----------------------------------------")

print("IDA star search heuristic 2 execution")
count = 0
while True:   
    path = ai.ida_star(startPuzzle[count], goalPuzzle[count], ai.z_puzzle_heuristic2, TIMER)
    if len(path) > 0:
        """for p in path:
            print(p)"""
        count += 1
    else:
        break    
    
print("IDA star search heuristic 2 has reached N =", count+1)
print("IDA star search heuristic 2 finish")



        
