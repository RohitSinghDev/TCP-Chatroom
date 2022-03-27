# tcp -> connection oriented protocol, suitable for sendable data
# udp -> connection less protocol, faster, video games, skype calls

# we are using internet socket
# protocol -> tcp
# port 80 -> reserved for http
# we are creating our own server, socket that listens for input and then clinet that connects to this socket


from http import client
import socket
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# INTERNET SOCKET, TCP
# SOCK_DGRAM -> UDP

s.bind(("127.0.0.1",55555))
# ip addr of host, server port

s.listen()
# continously listens for input from clients


while True:
    client, address = s.accept()
    # we are accepting every single client, we get client to send the message and address
    print(f"connected to {address}")
    client.send("you are coonected".encode())# encoded in utf-8
    client.close()






