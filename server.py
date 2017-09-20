# Python program to implement server side of chat room.
import socket
import select
import sys
from thread import *
from threading import Thread
from segtiment_analyst import Splitter, POSTagger
from dictionaty_tagger import DictionaryTagger, measure_score
import os


path_yaml = '/home/minhdo/segtiment_analyst/data_segtiment/'
positive_dir = 'positive.yaml'
negative_dir = 'negative.yaml'
inc_dir = 'inc.yaml'
dec_dir = 'dec.yaml'
inv_dir = 'inv.yaml'



"""The first argument AF_INET is the address domain of the
socket. This is used when we have an Internet Domain with
any two hosts The second argument is the type of socket.
SOCK_STREAM means that data or characters are read in
a continuous flow."""
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


port = 8000
 
"""
binds the server to an entered IP address and at the
specified port number.
The client must be aware of these parameters
"""
server.bind( ("", port) )
 
"""
listens for 100 active connections. This number can be
increased as per convenience.
"""
server.listen(5)
 

print "Waiting for conection ..."

client, addr = server.accept()

def listen():
    global server
    global client,addr
    while True:
        data = client.recv(1024)
        print (str(addr[0]) + "> " + str(data))
        print ("here is receiving from client").center(40, "#")

        text = str(data)
        splitter = Splitter()
        postagger = POSTagger()

        splitted_sentences = splitter.split(text.decode('utf-8'))
        pos_tagged_sentences = postagger.pos_tag(splitted_sentences)

        # print pos_tagged_sentences

        dicttagger = DictionaryTagger([
                                            os.path.join(path_yaml, positive_dir),
                                            os.path.join(path_yaml, negative_dir),
                                            os.path.join(path_yaml, inc_dir),
                                            os.path.join(path_yaml, dec_dir),
                                            os.path.join(path_yaml, inv_dir),

                                        ]
                                    )

        dict_tagged_sentences = dicttagger.tag(pos_tagged_sentences)
        score = measure_score.sentiment_score(dict_tagged_sentences)
        if score > 0:
            print ( "what you says is : {} \n    => it's positive sentence".format(text , measure_score.sentiment_score(dict_tagged_sentences))  )
        elif score < 0:
            print ( "what you says is : {} \n    => it's negative sentence".format(text , measure_score.sentiment_score(dict_tagged_sentences))  )    
        else:
            print ( "what you says is : {} \n    => it's neutral sentence".format(text , measure_score.sentiment_score(dict_tagged_sentences))  )    


def send():
    global server
    global client,addr
    while True:
        msg = raw_input("> ")
        client.send(msg)

if __name__ == '__main__':
    Thread(target = listen).start()
    Thread(target = send).start()

''' Start the receiving and sending thread '''
# list_of_clients = []
 
# def clientthread(conn, addr):
 
#     # sends a message to the client whose user object is conn
#     conn.send("Welcome to this chatroom!")
 
#     while True:
#             try:
#                 message = conn.recv(2048)
#                 if message:
 
#                     """prints the message and address of the
#                     user who just sent the message on the server
#                     terminal"""
#                     print "<" + addr[0] + "> " + message
 
#                     # Calls broadcast function to send message to all
#                     message_to_send = "<" + addr[0] + "> " + message
#                     broadcast(message_to_send, conn)
 
#                 else:
#                     """message may have no content if the connection
#                     is broken, in this case we remove the connection"""
#                     remove(conn)
 
#             except:
#                 continue
 
# """Using the below function, we broadcast the message to all
# clients who's object is not the same as the one sending
# the message """
# def broadcast(message, connection):
#     for clients in list_of_clients:
#         if clients!=connection:
#             try:
#                 clients.send(message)
#             except:
#                 clients.close()
 
#                 # if the link is broken, we remove the client
#                 remove(clients)
 
# """The following function simply removes the object
# from the list that was created at the beginning of 
# the program"""
# def remove(connection):
#     if connection in list_of_clients:
#         list_of_clients.remove(connection)
 
# while True:
 
#     """Accepts a connection request and stores two parameters, 
#     conn which is a socket object for that user, and addr 
#     which contains the IP address of the client that just 
#     connected"""
#     conn, addr = server.accept()
 
#     """Maintains a list of clients for ease of broadcasting
#     a message to all available people in the chatroom"""
#     list_of_clients.append(conn)
 
#     # prints the address of the user that just connected
#     print addr[0] + " connected"
 
#     # creates and individual thread for every user 
#     # that connects
#     start_new_thread(clientthread,(conn,addr))    
 
# conn.close()
# server.close()