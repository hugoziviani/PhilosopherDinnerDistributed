import socket
import cfg
import os

class SClientBC:
    def __init__(self):
        self.remote_host = self.remote_port = None
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            print('[CBC] - Cliente Broadcast Up!')
        except socket.error as exp:
            print('Falha na criacao do socket!!', exp)

    def connect(self, remote_host='', remote_port=5000):
        self.remote_host, self.remote_port = remote_host, remote_port
        #self.socket.connect((self.remote_host, self.remote_port))
        self.socket.bind((self.remote_host, self.remote_port))
        print('[CBC] - Cliente: '+ selfIp() +' na porta: '+ str(self.remote_port))

    def send(self, data):
        try:
            self.socket.send(data)
        except:
            print('[CBC] - Data fora do spectro')

    def receive(self, size = 1024):
        try:
            return self.socket.recv(size)
        except:
            print('[CBC]-Data não compatível')
            self.close()

    def close(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()

def hostname():
    return socket.gethostname()

def selfIp():
    ip = os.popen('hostname -I').read().replace(' \n', '')
    return ip






