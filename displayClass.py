import multiprocessing
import time
import datetime
import random
import pickle
import abc

from network import *

class Child(object):
    @abc.abstractmethod
    def stop(self):
        pass

class StatusDisplayModule(DatagramServerSocket, Child):
    def __init__(self, name_of_philosophers, ipToDisplay, portToDisplay):
        self.ipToDisplay = ipToDisplay
        self.portToDisplay = portToDisplay
        self.num = len (name_of_philosophers)
        self.name_of_philosophers = name_of_philosophers
        self.headers = ['Hora Atual']
        self.divider_line = '----------------------'
        self.display_format = '{: >20} '
        for i in range(len(name_of_philosophers)):
            self.headers.append(name_of_philosophers[i])
            if i != (len(name_of_philosophers) - 1):
                self.display_format += "{: >20} "
            else:
                self.display_format += "{: >20}"
            self.divider_line += "----------------------"
        print("\n\nDining Philosophers Problem: By Sagun Pandey and Shelby LeBlanc\n\nInproved by Hugo Ziviani\n\n")
        print(self.display_format.format(*self.headers))
        print(self.divider_line)
        super(StatusDisplayModule, self).__init__(self.ipToDisplay, self.portToDisplay)

    def start(self):
        super(StatusDisplayModule, self).start()

    def stop(self):
        super(StatusDisplayModule, self).stop()
        super(StatusDisplayModule, self).close()

    def handle_data(self, data):
        state = []

        response = pickle.loads(data[0])
        process_id = response[0]
        status_type = response[1]

        status = ""
        if status_type == 0:
            status = "Pensando"
        elif status_type == 1:
            status = "Esperando"
        elif status_type == 2:
            status = "Comendo"

        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        state.append(current_time)

        for i in range(self.num):
            if self.name_of_philosophers[i] == process_id:
                state.append(status)
            else:
                state.append("--------")

        print(self.display_format.format(*state))
