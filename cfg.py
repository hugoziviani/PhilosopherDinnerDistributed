NODES = [['10.8.40.41',  4000, 'Georgina'],
         ['10.8.40.91',  4001, 'Victoria'],
         ['10.8.40.5',   4002, 'Lenna'],
         ['10.8.40.109', 4003, 'Noemia'],
         ['10.8.40.112', 4004, 'Milena']]

NAMES = ['Georgina', 'Victoria', 'Lenna','Noemia', 'Milena']

PORT = 5151
NCNX = 5
VERIFICANODESTIME = 0.5
BCASTPORT = 6767
BCASTSRVRECIVEDATAPORT = 44444 #porta que o srv. BC recebe msg
TIMESRVSENDMSG = 0.5
STARTALL = '#ntrar'
STOPALL = '$air'

#============== JANTAR ==============================================#
VERBOSE = 1 			#Não printar as coisas
PEDIRGARFO_PORT = 9090 		#porta de pedir garfo
WAYPATH_TO_KITCHEN = "xterm -hold -e sudo python3 /home/debian/joubert/cozinha.py &"

#============== DISPLAY ==============================================#

DISPLAY_PORT = 6000
DISPLAY_IP_SRV = '10.8.40.91'
