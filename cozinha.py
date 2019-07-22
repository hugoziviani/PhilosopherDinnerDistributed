from network import *
from garfoClass import *
from filosofoClass import *
from displayClass import *
from latency import *

def garfo_process(identifier, address, port):
    garfo = Garfo(identifier, address, port)
    garfo.start()

def filosofo_process(identifier, fork_left, fork_right, portNear, portFar):
    philosopher = Philosopher(identifier, fork_left, fork_right, portNear, portFar)
    philosopher.start()

def limpemos(garfo, filosofo):
    garfo.terminate()
    filosofo.terminate()
    if(cfg.VERBOSE):
        print('Saindo do Jantar!')


# Fazer a busca por garfos rodando o vetor de servers
    


if __name__ == "__main__":
    filosofo = None
    garfo = None
    try:
        info = listOfPeers()
        selfIp = info[0][1]
        selfPorta = info[0][2]
        selfName = info[0][3]
        garfoPertoIp = info[1][1]
        portaPerto = info[1][2]
        garfoLongeIp = info[2][1]
        portaLonge = info[2][2]
        
        garfo = multiprocessing.Process(target=garfo_process, args=(hostname(), selfIp, selfPorta,))
        filosofo = multiprocessing.Process(target=filosofo_process, args=(selfName, garfoPertoIp, garfoLongeIp, portaPerto, portaLonge,))
        garfo.start()
        filosofo.start()
        
        entry = input()
        print( "==========================================CHEGOU", entry)
        if(entry == cfg.STOPALL):
            print( "==========================================CHEGOU") 
            filosofo.terminate()
            garfo.terminate()
            limpemos(garfo, filosofo)
        
    except KeyboardInterrupt:
        #playS = playC = False
        limpemos(garfo, filosofo)










