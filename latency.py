import shlex
import cfg
import os
from subprocess import Popen, PIPE, STDOUT


def selfIp(ip=''):
    ip = os.popen("hostname -I").read().replace(" \n","")
    return ip
def get_simple_cmd_output(cmd, stderr=STDOUT):
    args = shlex.split(cmd)
    return Popen(args, stdout=PIPE, stderr=stderr).communicate()[0]

def get_ping_time(host):
    host = host.split(':')[0]
    cmd = "fping {host} -C 3 -q".format(host=host)
    # result = str(get_simple_cmd_output(cmd)).replace('\\','').split(':')[-1].split() if x != '-']
    result = str(get_simple_cmd_output(cmd)).replace('\\', '').split(':')[-1].replace("n'", '').replace("-",'').replace("b''", '').split()
    res = [float(x) for x in result]
    if len(res) > 0:
        return "{0:.2f}".format(sum(res) / len(res))
    else:
        return 999999

def listOfPeers():
    if(cfg.VERBOSE):
        print('Mapeando rede, verificando latencia para pedir recurso...')
    vel = []
    hosts = cfg.NODES
    for ip in hosts:
        vel.append([get_ping_time(ip[0]), ip[0], ip[1], ip[2]])
    vel.sort()
    if(cfg.VERBOSE):
        print('Recursos:\n',vel)
    return vel


#print(listOfPeers())
