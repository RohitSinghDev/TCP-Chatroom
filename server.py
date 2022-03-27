from concurrent.futures import thread
from email import message
from operator import index
import threading
import socket
from tracemalloc import start
from warnings import catch_warnings

from sklearn.multioutput import ClassifierChain
host = "127.0.0.1"#local host
port = 55555

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host,port))
server.listen()


# 3 methods :
# broadcast method, handle method for client connections, receive method that combines all methods to main method


clients = []
nicknames = [] #nicknames for clients

#broadcast function - sends message to all clients
def broadcast(message):
    for client in clients:
        client.send(message)

#get , process and broadcast message
# each client will be executing this func
def handle(client):
    while True:
        try:
            

            msg = message = client.recv(1024)#receive message from a client 

            if msg.decode("ascii").startswith("KICK"):
                if nicknames[clients.index(client)] == "admin":
                    name_to_kick = msg.decode("ascii")[5:]
                    kick_user(name_to_kick)
                else:
                    client.send("command was refused".encode("ascii"))

            elif msg.decode("ascii").startswith("BAN"):
                if nicknames[clients.index(client)] == "admin":
                    name_to_ban = msg.decode("ascii")[4:]
                    kick_user(name_to_ban)
                    with open("bans.txt","a") as f :
                        f.write(f"{name_to_ban}\n")
                    print(f"{name_to_ban} was banned")
                else:
                    client.send("command was refused ".encode("ascii"))                
            else:
                broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f"{nickname} left the chat".encode("ascii"))
            nicknames.remove(nickname)
            break

# combines all above function
def receive():
    while True:
        client,address = server.accept()#accepting all connections, all clients connecting
        print(f"connected with {str(address)}")
        client.send("NICK".encode("ascii"))#if cleint recevives this , he need to enter nickname
        nickname = client.recv(1024).decode("ascii")

        with open("bans.txt","r") as f:
            bans = f.readlines()

        if nickname+"\n" in bans:#refuse connection if name of client in bans.txt
            client.send("BAN".encode("ascii"))
            client.close()
            continue

        #password for client admin
        if nickname == "admin":
            client.send("PASS".encode("ascii"))
            password = client.recv(1024).decode("ascii")

            if password != "adminpass":#password for admin
                client.send("REFUSE".encode("ascii"))
                client.close()
                continue


        nicknames.append(nickname)
        clients.append(client)

        print(f"nickname of the client is {nickname}")
        broadcast(f"{nickname} joined the chat".encode("ascii"))
        client.send("connected to server".encode("ascii"))

        #one thread for each client
        #to handle and interact with one client we need seperate threads
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

def kick_user(name):
    if name in nicknames:
        name_index = nicknames.index(name)
        client_to_kick = clients[name_index]
        clients.remove(client_to_kick)
        client_to_kick.send("you are kicked by admin".encode("ascii"))
        client_to_kick.close()
        nicknames.remove(name)
        broadcast(f"{name} was kicked by an admin!".encode("ascii"))

print("server is listening")
receive()