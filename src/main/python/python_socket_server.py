import socket
import pythonRecognitionService_pb2.py

def start_socket(port):
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(('localhost', 8089))
    serversocket.listen(5) # become a server socket, maximum 5 connections

    while True:
        connection, address = serversocket.accept()
        receive_message()
        buf = connection.recv(64)
        connection.recv
        if len(buf) > 0:
            print buf
            break

def receive_message(connection):
    # how long the binary message is
    totallen = connection.recv(4)