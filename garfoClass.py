import multiprocessing
import time
import datetime
import random
import pickle
import abc
import sys
import cfg
from network import *

class Child(object):
    @abc.abstractmethod
    def stop(self):
        pass
    
class Garfo(SocketServer, Child):
    def __init__(self, identifier, host, port):
        self.identifier = identifier
        self.sendoUsado = False
        self.quemEstaUsando = None
        super(Garfo, self).__init__(host, port)
        if (VERBOSE):
            print('[' + str(self.identifier) + ']-Garfo '+str(self.identifier)+' criado.')

    def start(self):
        self.run = True
        super(Garfo, self).start() #Chama a handle_connection
        if(cfg.VERBOSE):
            print('[' + str(self.identifier) + ']-Garfo '+str(self.identifier)+' Up.')
        

    def stop(self):
        self.run = False
        if(cfg.VERBOSE):
            print('[' + str(self.identifier) + ']-Garfo '+str(self.identifier)+' Down.')
        super(Garfo, self).stop()

    def handle_connection(self, connection):
        while self.run:
            if not self.run:
                break
            try:
                data = connection.recv(1024)               
                if data:
                    request = pickle.loads(data)  # request -> [philosopher_id, action]
                    if(cfg.VERBOSE):
                        print('[' + str(self.identifier) + ']-Filósofo ', request[0],' quer:', request[1], '####')
                    # If the request action is acquiring the fork
                    if request[1] == 1:
                        if self.sendoUsado:  # Não Disponível
                            # Send [fork_id, philosopher_id, action, success]
                            # action  = 1 for acquiring fork
                            # success = 0 for failure
                            if(cfg.VERBOSE):
                                print ('[' + str(self.identifier) + ']-Garfo em uso')
                            connection.send(pickle.dumps([self.identifier, request[0], 1, 0]))
                            break
                        else:  # Disponível
                            self.sendoUsado = True
                            self.quemEstaUsando = request[0]  # Guarda quem tá usando o garfo
                            # Send [fork_id, philosopher_id, action, success]
                            # action  = 1 for acquiring fork
                            # success = 1 for success
                            if(cfg.VERBOSE):
                                print ('[' + str(self.identifier) + ']-Garfo disponível, pode pegar. Filósofo: ', request[0], ' - Está usando')
                            connection.send(pickle.dumps([self.identifier, self.quemEstaUsando, 1, 1]))
                            break
                    # Entregar o garfo
                    elif request[1] == 0:
                        # Fork has to be dirty/being used
                        # Release request can only be made by the philosopher holding the fork
                        if self.sendoUsado and self.quemEstaUsando == request[0]:
                            last_user = self.quemEstaUsando
                            self.sendoUsado = False
                            self.quemEstaUsando = None
                            # Send [fork_id, philosopher_id, action, success]
                            # action  = 0 devolver o garfo
                            # success = 1 for success
                            if(cfg.VERBOSE):
                                print ('[' + str(self.identifier) + ']-Garfo devolvido')
                            connection.send(pickle.dumps([self.identifier, last_user, 0, 1]))
                            break
                        else:
                            # Send [fork_id, philosopher_id, action, success]
                            # action  = 0 falha na entrega do garfo
                            # success = 0 for failure
                            if(cfg.VERBOSE):
                                print ('[' + str(self.identifier) + ']-Garfo não devolvido')
                            connection.send(pickle.dumps([self.identifier, request[0], 0, 0]))
                            break
            except:
                if(cfg.VERBOSE):
                    print('[' + str(self.identifier) + ']-Caiu no except -->', exp)
                break
        connection.close()
        if(cfg.VERBOSE):
            print('[' + str(self.identifier) + ']-Saiu - fechou conexão')
