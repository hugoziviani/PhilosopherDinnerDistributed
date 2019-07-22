import socket
import abc
import os
from cfg import *
from threading import *



def hostname():
    return socket.gethostname()


# Server Program

class SocketServer(object):
    def __init__(self, host=hostname(), port=PEDIRGARFO_PORT):
        self.host = host
        self.port = port
        self.connection = None
        self.cliente = None
        self.remote_port = None
        self.run = False
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if(VERBOSE):
                print('SocketServer criado')
        except socket.error as exp:
            print('[ERRO] - Failha ao criar o TCP Server', exp)
        try:
            self.socket.bind((self.host, self.port))
            if(VERBOSE):
                print('SocketServer conectado')
        except socket.error as exp:
            print('[ERRO] - Não foi possível conectar ao ' + str(self.host) + ' na porta: ' + str(self.port), exp)
            

    def start(self):
        self.run = True
        self.socket.listen(0)
        if (VERBOSE):
            print('SocketServer Iniciado. Ouvindo pela porta: '+ str(self.port))
        while self.run:
            self.connection, self.cliente = self.socket.accept()
            Thread(target=self.handle_connection, args=(self.connection,)).start()
            
                
    def stop(self):
        self.run = False
       

    @abc.abstractmethod
    def handle_connection(self, connection):
        pass


# Client Program

class SocketClient:
    def __init__(self):
        self.remote_host = self.remote_port = None
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print('Socket Client Up!')
        except socket.error as exp:
            print('Falha ao criar Cliente TCP', exp)

    def connect(self, remote_host=hostname(), remote_port=5000):
        self.remote_host, self.remote_port = remote_host, remote_port
        self.socket.connect((self.remote_host, self.remote_port))
        if (VERBOSE):
            print('Cliente connectado em: ',self.remote_host,' pela porta: ', self.remote_port)
        
        

    def send(self, data):
        if (VERBOSE):
            print('Enviando:', data)
        self.socket.send(data)    

    def receive(self, size=1024):
        var = self.socket.recv(size)
        if (VERBOSE):
            print('Recebendo:', var)
        return var

    def close(self):
        self.socket.close()


# Datagram Server Program

class DatagramServerSocket(object):
    def __init__(self, host=hostname(), port=5000):
        self.host, self.port = host, port
        self.run = False
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error as exp:
            print('Falha ao criar Server UDP!!', exp)
        try:
            self.socket.bind((self.host, self.port))
        except socket.error as exp:
            print('Não foi possível conectar à ' + str(self.host) + ' na porta: ' + str(self.port), exp)

    def start(self):
        self.run = True
        while self.run:
            d = self.receive()
            Thread(target=self.handle_data, args=(d,)).start()

    def stop(self):
        self.run = False

    @abc.abstractmethod
    def handle_data(self, data):
        pass

    def send(self, data, remote_address):
        self.socket.sendto(data, remote_address)

    def receive(self, size=1024):
        return self.socket.recvfrom(size)

    def close(self):
        self.socket.close()


# Datagram Client Program

class DatagramSocketClient:
    def __init__(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error as exp:
            print('Falha ao criar cliente UDP socket object', exp)

    def send(self, remote_host=hostname(), remote_port=5000, data=""):
        self.socket.sendto(data, (remote_host, remote_port))

    def receive(self, size=1024):
        return self.socket.recvfrom(size)[0]

    def close(self):
        self.socket.close()

def selfIp():
    ip = os.popen('hostname -I').read().replace(' \n', '')
    return ip
