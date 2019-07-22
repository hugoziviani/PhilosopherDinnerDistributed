from cbc import *
from sbc import *
from _thread import *
from cozinha import *
import threading
import time
import pickle
import subprocess
import os
import signal


def sobeServer(startS):
    if(cfg.VERBOSE):
        print('Subindo Thread Server BC')
    #global runS
    runS = startS
    s = SServerBC()
    s.connect('', cfg.BCASTPORT)
    while runS:
        message = input()
        start = verifyInput(message)
        #verifica input, se tiver o protocolo eu chamo o start
        msg = ('['+hostname()+']-'+selfIp()+ ': '+message)
        s.send(pickle.dumps([start, msg]))
        #startS = start #Sair!!
        if not startS:
            if(cfg.VERBOSE):
                print('[SBC]-Saindo do BC')
            break
        

def verifyInput(message):
    if(cfg.VERBOSE):
        if(cfg.VERBOSE):
            print( 'MSG do input:', message)
    if(message == cfg.STARTALL):
        return True
    elif(message == cfg.STOPALL):
        return False
    else:
        None

def sobeClient(startC, wayPath):
    filosofo = []
    garfo = []
    #scenary = []
    if(cfg.VERBOSE):
        print('Subindo Thread Cliente BC')
    #global runC
    runC = startC
    c = SClientBC()
    c.connect('', cfg.BCASTPORT)
    while runC:
        info = c.receive()
        msg = pickle.loads(info)
        if msg[0] == True:
            if(cfg.VERBOSE):
                print('VERDADE:', msg)
            scenaryProcess = startOpenScenary(wayPath)
        if msg[0] == False:
            if(cfg.VERBOSE):
                print('MENTIRA:', msg)
            scenaryProcess.communicate(cfg.STOPALL)
            playS = playC = False
            
        if msg[0] == None:
            if(cfg.VERBOSE):
                print('NADA DISSO BAGUERA', msg)
        if not runC:
            if(cfg.VERBOSE):
                print('[CBC]-Saindo do BC')
            break

def startOpenScenary (wayPath):
    scenaryProcess = subprocess.Popen(wayPath, shell = True)
    return scenaryProcess

def stopCloseScenary (process):
    playS = playC = False
    tC.stop()
    tS.stop()
    print('Saida do Processo:',out)
    
#time.sleep(3)
#playS = playC = False
#tC.join()
#tS.join()
#print('Saindo do BC')

if __name__ == "__main__":
    tC = []
    tS = []
    global scenaryProcess
    scenaryProcess = []
    wayPath = cfg.WAYPATH_TO_KITCHEN
    try:
        global playS, playC
        playS = playC = True
        tS = threading.Thread(target=sobeServer, args = (playS,))
        tC = threading.Thread(target=sobeClient, args = (playC, wayPath))
        tC.start()
        tS.start()
        
    except KeyboardInterrupt:
        playS = playC = False
        tC.terminate()
        tS.terminate()
        






