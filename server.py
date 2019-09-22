import socket
import sys

#reference: https://pymotw.com/2/socket/tcp.html

size = 10

board = [["a" for i in range(size)] for j in range(size)]

f = open( "own_board.txt", "r" )
a = []
for line in f:
    #print(line)
    a.append(line)

for i in range(size):
    for j in range(size):
        board[i][j] = a[i][j]

shipC = 5
shipB = 4
shipR = 3
shipS = 3
shipD = 2
shipTotal = 17

response = ""

# C5 B4 R3 S3 D1 D1
def check(ship):
    global shipC
    global shipB
    global shipR
    global shipS
    global shipD
    global shipTotal
    global response
    if ship == "C":
        shipC = shipC - 1
        shipTotal = shipTotal - 1
        if shipC <= 0:
            print("carrier sunk")
            response = response + " - carrier sunk"

    elif ship == "B":
        shipB = shipB - 1
        shipTotal = shipTotal - 1
        if shipB <= 0:
            print("battleship sunk")
            response = response + " - battleship sunk"

    elif ship == "R":
        shipR = shipR - 1
        shipTotal = shipTotal - 1
        if shipR <= 0:
            print("cruiser sunk")
            response = response + " - cruiser sunk"

    elif ship == "S":
        shipS = shipS - 1
        shipTotal = shipTotal - 1
        if shipS <= 0:
            print("submarine sunk")
            response = response + " - submarine sunk"

    elif ship == "D":
        shipD = shipD - 1
        shipTotal = shipTotal - 1
        print("destroyer sunk")
        if shipD == 1:
            response = response + " - destroyer 1 sunk"
        elif shipD == 0:
            response = response + " - destroyer 2 sunk"
    else:
        print("invalid ship check")
        response = "invalid in ship check"

    if shipTotal <= 0:
        print("GAME OVER")
        response = response + " - GAME OVER"

def printBoard():
    for i in range(size):
        print(board[i])
        print("")
    print("")

def attack(x, y):
    global board
    global response
    if(board[x][y] == "_"):
        print("miss")
        response = "miss"
        board[x][y] = "x"
    elif(board[x][y] == "x"):
        print("already a miss")
        response = "already a miss"
    elif(board[x][y] == "X"):
        print("already a hit")
        response = "already a hit"
    else:
        print("HIT")
        response = "hit"
        check(board[x][y])
        board[x][y] = "X"
    printBoard()



# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('10.152.150.207', 10000)
print(sys.stderr, 'starting up on %s port %s' % server_address)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    #print(sys.stderr, 'waiting for a connection')
    connection, client_address = sock.accept()

    try:
        #print(sys.stderr, 'connection from', client_address)
        print("test")

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(16)
            if data.decode() == "":
                trash = 1
            else:
                #print(sys.stderr, 'received "%s"' % data)
                #print(data)
                #print(type(data))
                spoint = data.decode()
                try:
                    point = int(spoint)
                except ValueError:
                    print("invalid (not an int)")
                    response = "invalid (not an int)"
                if point < 0:
                    print("invalid int (below 00)")
                    response = "invalid int (below 00)"
                elif point > 99:
                    print("invalid int (above 99)")
                    response = "invalid int (above 99)"
                else:
                    y = point%10
                    x = int((point - y)/10)

                    print("(", x, ", ", y, ")")
                    attack(x, y)

            if data:
                #print(sys.stderr, 'sending data back to the client')
                connection.sendall(response.encode())
            else:
                #print(sys.stderr, 'no more data from', client_address)
                break

    finally:
        # Clean up the connection
        connection.close()