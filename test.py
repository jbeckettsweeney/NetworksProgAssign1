import numpy as np

size = 10

board = [["a" for i in range(size)] for j in range(size)]
board[1][1] = "b"
print(board[0][0])
print(board[1][1])

f = open( "own_board.txt", "r" )
a = []
for line in f:
    print(line)
    a.append(line)

for i in range(size):
    for j in range(size):
        board[i][j] = a[i][j]

print(board)
if(board[0][6] != "_"):
    print("hit")
else:
    print("miss")
