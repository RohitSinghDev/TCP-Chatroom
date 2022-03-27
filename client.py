from email import message
from http import client
import socket
import threading

nickname = input("choose a nickname: ")
if nickname == "admin":
    password = input("password for admin: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1",55555))


stop_thread = False

#recieve data constantly from server
def receive():
    while True:
        global stop_thread
        if stop_thread:
            break#if admin password was wrong , connection disconnected
        try:
            message = client.recv(1024).decode("ascii")
            if message=="NICK":
                client.send(nickname.encode("ascii"))
                next_message  = client.recv(1024).decode("ascii")
                if next_message == "PASS":#recevived form server
                    client.send(password.encode("ascii"))
                    if client.recv(1024).decode("ascii") == "REFUSE":
                        print("connection was refused, wrong password")
                        stop_thread = True
                elif next_message =="BAN":
                    print("connection refused because of ban!")
                    client.close()
                    stop_thread = True

                


            else:
                print(message)
        except:
            print("an error occurred")
            client.close()
            break

#
def write():
    while True:
        if stop_thread:
            break #breaking if not admin
        message = f"{nickname}:{input('')}"
        if message[len(nickname)+2:].startswith("/"):
            #check if a command is run
            #username: /whatever
            if nickname=='admin':
                #only admin can make this commands
                if message[len(nickname)+2:].startswith("/kick"):#if kick command is given
                    client.send(f"KICK {message[len(nickname)+2+6:]}").encode("ascii")
                    #KICk message send to server
                elif message[len(nickname)+2:].startswith("/ban"):
                    #ban message send to server
                    client.send(f"BAN {message[len(nickname)+2+5:]}".encode("ascii"))
                
            else:
                print("only admin can run these commands")
        
        else:
            client.send(message.encode("ascii"))

        client.send(message.encode("ascii"))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()