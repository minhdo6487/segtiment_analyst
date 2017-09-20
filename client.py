# Python program to implement client side of chat room.
import socket
import time
from thread import *
from threading import Thread
 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 8000

count = 0

print """ Trying to connect to partner """

 
while count == 0:
    try:
        server.connect(("localhost", port))
        count += 1
    except:
        pass

print "You are connected successfully !!!"


def listen():
    global server
    while True:
        data = server.recv(1024)
        print ("localhost:" + "> " + str(data))

def send():
    global server
    while True:
        msg = raw_input("> ")
        server.send(msg)

if __name__ == '__main__':
    Thread(target = listen).start()
    Thread(target = send).start()    