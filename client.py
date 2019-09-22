import socket
import sys

#reference: https://pymotw.com/2/socket/tcp.html

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

size = 10
oppboard = [["_" for i in range(size)] for j in range(size)]

def printBoard():
    for i in range(size):
        print(oppboard[i])
        print("")
    print("")

def updateBoard(input, coord):
    global oppboard
    try:
        point = int(coord)
    except ValueError:
        print("invalid (not an int)")
    if point < 0:
        print("invalid int (below 00)")
    elif point > 99:
        print("invalid int (above 99)")
    else:
        y = point % 10
        x = int((point - y) / 10)
        if(input[:3] == "hit"):
            oppboard[x][y] = "1"
        elif(input[:4] == "miss"):
            oppboard[x][y] = "0"

#10.152.167.222

# Connect the socket to the port where the server is listening
server_address = ('10.152.150.207', 10000)
print(sys.stderr, 'connecting to %s port %s' % server_address)
sock.connect(server_address)
message = ""
print("send responses in the form 'xx'")
print("example: 54 for row 5 col 4")
while(message != "exit"):

    try:

        # Send data
        message = input()
        #print(sys.stderr, 'sending "%s"' % message)
        print('sending "%s"' % message)
        sock.sendall(message.encode())

        # Look for the response
        amount_received = 0
        amount_expected = len(message)

        while amount_received < amount_expected:
            data = sock.recv(64)
            amount_received += len(data)
            #print(sys.stderr, 'received "%s"' % data.decode())
            print('received "%s"' % data.decode())

        updateBoard(data.decode(), message)
        printBoard()

    finally:
        print("wait your turn")

print(sys.stderr, 'closing socket')
sock.close()