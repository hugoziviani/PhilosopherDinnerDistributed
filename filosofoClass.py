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

class Philosopher(Child):
    def __init__(self, identifier, fork_left, fork_right, portNear, portFar):
        self.id = identifier
        self.ip = selfIp()
        self.fork_left = fork_left
        self.fork_right = fork_right
        self.portNear = portNear    # porta perto pedir garfo -- Mesma maquina portas diferentes
        self.portFar = portFar      # porta longe pedir garfo -- remoto portas iguais
        self.run = False
        if(cfg.VERBOSE):
            print('['+str(self.id) +']-' + self.ip + ': Filósofo '+str(self.id)+' criado.')

    def start(self):
        self.run = True
        while self.run:
            self.report_status(pickle.dumps([self.id, 0]))  # PENSANDO, manda pro serv. Display
            time.sleep(random.randint(1, 3))
            self.dine()

    def stop(self):
        self.run = False

    def dine(self):
        if(cfg.VERBOSE):
            print('['+str(self.id) +']-Entrei na funcao comer')
        fork_l = self.fork_left
        fork_r = self.fork_right
        portNear = self.portNear
        portFar = self.portFar
        self.report_status(pickle.dumps([self.id, 1]))  # ESPERANDO - envia msg ao screen
        clientNear = None        
        clientFar = None
        while self.run:
            if(cfg.VERBOSE):
                print('['+str(self.id) +']-Tentando adquirir garfo perto, BLOQUEANDO')
            clientNear = self.acquire_blocking(fork_l, portNear)  # TEM que pegar o garfo esquerdo            
            if(cfg.VERBOSE):
                print('['+str(self.id) +']-Tentando adquirir garfo perto, 100 BLOQUEAR')
            clientFar = self.acquire_non_blocking(fork_r, portFar)  # TENTA pegar o direito            
            disponivel = clientFar[0]#retorna se o garfo tá rolando
            if not disponivel:
                # Se o garfo não foi adquirido
                if(cfg.VERBOSE):
                    print('['+str(self.id) +']- não consegui, vou devolver o garfo...')
                self.liberaGarfo(clientNear)   # Libera o garfo
                fAux = fork_l
                fork_l = fork_r
                fork_r = fAux
                # Troca, para na proxima tentar pegar o garfo oposto primeiro
                pAux = portNear
                portNear = portFar
                portFar = pAux   # Troca, para pedir na porta certa
            else:
                if(cfg.VERBOSE):
                    print('['+str(self.id) +']-Filosofo '+str(self.id)+ ' caiu no ELSE- break')
                break
        if self.run:
            if(cfg.VERBOSE):
                print('['+str(self.id) +']-Filosofo ' + str(self.id) + ' vai reportar status e dormir')
            self.dining() # reporta Status e dorme um cadinho
            if(cfg.VERBOSE):
                print('['+str(self.id) +']-Filosofo ' + str(self.id) + ' tentando devolver o garfo PERTO')
            if (self.liberaGarfo(clientNear)):
                if(cfg.VERBOSE):
                    print('['+str(self.id) +']-Garfo devolvido: ', clientNear[0])
                    print('['+str(self.id) +']-Filosofo ' + str(self.id) + ' tentando devolver o garfo LONGE')
            if (self.liberaGarfo(clientFar)):
                if(cfg.VERBOSE):
                    print('['+str(self.id) +']-Garfo devolvido: ', clientFar[0])     
    # Bloqueia a execucao até o filosofo adiquirir o garfo
    def acquire_blocking(self, garfoIp, porta):
        while self.run:
            if not self.run:
                break                
            try:
                time.sleep(0.2)
                if(cfg.VERBOSE):
                    print('['+str(self.id) +']-Criando client para pedir garfo no IP: ', garfoIp, ' pela porta: ', porta)
                client = SocketClient()
                client.connect(garfoIp, porta)
                if(cfg.VERBOSE):
                    print('['+str(self.id) +']-Pdeindo garfo em no IP: ', garfoIp, ' pela porta: ', porta)
                client.send(pickle.dumps([self.id, 1]))
                data = client.receive()
                if data:
                    response = pickle.loads(data)
                    if(cfg.VERBOSE):
                        print('['+str(self.id) +']-INFORMACOES vindas de: ', garfoIp, ' pela porta: ', porta)
                        print('['+str(self.id) +']-In. dta:\n', response)
                    # response -> [fork_id, philosopher_id, action, result]
                    # action   -> envia 1 para adquirir o garfo, envia 0 para liberar o garfo
                    # result  -> 1 = successo, 0 = falha
                        print('['+str(self.id) +']-Fim. dta\n')
                    if response[1] == self.id and response[2] == 1 and response[3] == 1:
                        if(cfg.VERBOSE):
                            print('['+str(self.id) +']-Retornando cliente - SocketClient()')
                            print('['+str(self.id) +']-Garfo: ', response[0],'Sucesso: ', response[3])
                        client.close()
                        return [response[0], response[3], garfoIp, porta]                        
                client.close()
                return [None, None, garfoIp, porta]
            except KeyboardInterrupt:
                self.run = False
                break            
            except:
                if(cfg.VERBOSE):
                    print('['+str(self.id) +']-Except Pass')
                pass

    # Não bloquei a execucao caso o cliente não consiga o garfo
    def acquire_non_blocking(self, garfoIp, porta):
        if(cfg.VERBOSE):
            print('['+str(self.id) +']-Criando client para pedir garfo no IP: ', garfoIp, ' pela porta: ', porta)
        client = SocketClient()
        client.connect(garfoIp, porta)
        if(cfg.VERBOSE):
            print('['+str(self.id) +']-Pdeindo garfo em no IP: ', garfoIp, ' pela porta: ', porta)
        client.send(pickle.dumps([self.id, 1]))
        data = client.receive()
        if data:
            response = pickle.loads(data)
            if(cfg.VERBOSE):
                print('['+str(self.id) +']-INFORMACOES vindas de: ', garfoIp, ' pela porta: ', porta)
                print('['+str(self.id) +']-In. dta:\n', response)
                # response -> [fork_id, philosopher_id, action, success]
                # action   -> 1 = acquiring the fork, 0 = releasing the fork
                # success  -> 1 = successful, 0 = failure
                print('['+str(self.id) +']-Fim. dta\n')
            if response[1] == self.id and response[2] == 1 and response[3] == 1:
                if(cfg.VERBOSE):
                    print('['+str(self.id) +'Retornando cliente - SocketClient()')
                client.close()
                return [response[0], response[3], garfoIp, porta]
        client.close()
        return [False, None, garfoIp, porta]
    
    def liberaGarfo(self, clientInfo):
        client = SocketClient()
        client.connect(clientInfo[2],clientInfo[3])        
        client.send(pickle.dumps([self.id, 0]))  # Sends [id, 0] to server. 0 being command for releasing the fork
        data = client.receive()
        if data :
            response = pickle.loads(data)
            # response -> [fork_id, philosopher_id, action, success]
            # action   -> 1 = acquiring the fork, 0 = releasing the fork
            # success  -> 1 = successful, 0 = failure
            if response[1] == self.id and response[2] == 0 and response[3] == 1:
                client.close()
                return True
            else:
                pass
    def dining(self):
        if(cfg.VERBOSE):
            print('['+str(self.id) +']-Filosofo ',str(self.id), ' reportando Status')
        self.report_status(pickle.dumps([self.id, 2]))  # COMENDO - reporta status p/ display
        time.sleep(random.randint(3, 6)) # dorme random
        if(cfg.VERBOSE):
            print('['+str(self.id) +']-Filosofo ',str(self.id), ' Fim do sleep, Acordei!')
        

    @staticmethod
    def report_status(msg):
        if(cfg.VERBOSE):
            print('------------REPORTANDO STATUS--------')
        client = DatagramSocketClient()
        client.send(cfg.DISPLAY_IP_SRV, DISPLAY_PORT, msg)
        client.close()
