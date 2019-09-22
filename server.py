import socket
import sys
import numpy as np

filename = "own_board.txt"

with open(filename) as f:
    data = f.readlines()


#reference: https://pymotw.com/2/socket/tcp.html

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
    print(sys.stderr, 'waiting for a connection')
    connection, client_address = sock.accept()

    try:
        print(sys.stderr, 'connection from', client_address)
        print("test")

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(16)
            #print(sys.stderr, 'received "%s"' % data)
            print(data)
            print(type(data))
            print("data")
            point = int(data.decode())

            if data.decode() == "Test.":
                print("success")
            if data:
                print(sys.stderr, 'sending data back to the client')
                connection.sendall(data)
            else:
                print(sys.stderr, 'no more data from', client_address)
                break

    finally:
        # Clean up the connection
        connection.close()