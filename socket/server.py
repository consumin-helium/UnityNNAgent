'''
Server/Colab side for the socket AI reinforced learning project
'''

# first of all import the socket library
import socket			
import time


'''
HERE WE DEFINE THE STRUCTURE FOR THE PLAYER INPUT


rotate_right = [1,0,0,0,0,0,0,0,0]
rotate_left = [0,1,0,0,0,0,0,0,0] IGNORED FOR NOW
move_forwards = [0,0,1,0,0,0,0,0,0]
move_backwards = [0,0,0,1,0,0,0,0,0]
study = [0,0,0,0,1,0,0,0,0]
upgrade = [0,0,0,0,0,1,0,0,0]
recruit_farmer = [0,0,0,0,0,1,0,0]
recruit_scout = [0,0,0,0,0,0,0,1,0]
idle = [0,0,0,0,0,0,0,0,1]


'''


# next create a socket object
s = socket.socket()		
print ("Socket successfully created")

# reserve a port on your computer in our
# case it is 12345 but it can be anything
port = 8052		

# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests
# coming from other computers on the network
s.bind(('', port))		
print ("socket binded to %s" %(port))

# put the socket into listening mode
s.listen(5)	
print ("socket is listening")		

# a forever loop until we interrupt it or
# an error occurs

# Establish connection with client.
c, addr = s.accept()	
print ('Got connection from', addr )
while True:
    

    print (c.recv(1024).decode())
    time.sleep(.1)

    # now we construct a new dict
    data_package = {'"up"':'"1"','"timestamp"':'"' + str(time.time()) + '"'}

    data_package = str(data_package)
    data_package.replace("'", '"')

 

    # send a thank you message to the client. encoding to send byte type.
    c.send(data_package.encode())

    # Close the connection with the client
    #c.close()

    # Breaking once connection closed
    #break
