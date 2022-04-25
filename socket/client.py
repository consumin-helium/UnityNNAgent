'''
Client/Unity side for the socket AI reinforced learning project
'''

# Import socket module
import socket			

# Create a socket object
s = socket.socket()		

# Define the port on which you want to connect
port = 1234			


# connect to the server on local computer
s.connect(("localhost", port))

s.send('Input data'.encode())

# receive data from the server and decoding to get the string.
print (s.recv(1024).decode())
# close the connection
s.close()	
	
