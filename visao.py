from network import *
from garfoClass import *
from filosofoClass import *
from displayClass import *
from latency import *

def display_process(number_of_philosophers, ipToDisplay, portToDisplay):
    display_module = StatusDisplayModule(number_of_philosophers, ipToDisplay, portToDisplay)
    display_module.start()

def iniciaDisplay():
    try:
        names = cfg.NAMES
        d = multiprocessing.Process(target=display_process, args=(names, cfg.DISPLAY_IP_SRV, cfg.DISPLAY_PORT,))
        d.deamon = True
        d.start()
    except KeyboardInterrupt:
        print('Fechando Display')
        d.stop()

if __name__ == "__main__":
    try:
        iniciaDisplay()
    except KeyboardInterrupt:
        print('Display-Out!')
