#!/usr/bin/env python

###########################  LIBRERIAS  #########################################

import os
from socket  import * 
import threading
import SocketServer

from jsonrpclib import Server
import urllib
import  socket
import time
from time import time, sleep
import commands

from jsonrpclib import Server
import urllib
from Queue import Queue
from threading import Thread
from time import time, sleep
from subprocess import Popen, PIPE
import sys


#################################################################################

#######################################  VARIABLES  DE INICIALIZACION ###########

SERVER_HOST = '192.168.12.48'
SERVER_PORT = 8000 
BUF_SIZE = 4096

inscritos = []
myHosts = []

#archivo = open( '/mnt/flash/automata/direcciones.txt','r' )
#linea=archivo.readline()
#while linea!="":
#            linea=archivo.readline()
#            linea=linea.rstrip("\n'")
#            linea=linea.lstrip("'")
#            inscritos.append(linea)
#archivo.close()

prendidos = []
apagados = []
caidos = []


inscritos.append(sys.argv[1])



###################################################################################


################## 1 INICIO  DE CLASE  ThreadReport ########################################################
class ThreadReport(Thread):
    """Threaded OS command which returns to a queue"""
    def __init__(self, queueIn, queueOut):
        Thread.__init__(self)
        self.get_queue = queueIn
        self.put_queue = queueOut
    
    def _get(self):
        return self.get_queue.get()
    def _done(self):
        self.get_queue.task_done()
    def _put(self,toPut):
        return self.put_queue.put(toPut)

    def run(self):
        while True:
            myCommand = self._get() #maybe command should consist of a popen command list and a callback for that command
            cmdLst = myCommand[0]
            fnXf = myCommand[1]
            try:
                pipe = Popen(cmdLst, stdout=PIPE)
                myOut = fnXf(pipe.communicate()[0])
            except Exception as e:
                print "%s, %s"%(",".join(cmdLst), str(fnXf))
                myOut = None
            self._done()
            self._put(myOut)
 ################## 1   FIN  DE CLASE  ThreadReport ########################################################
                   
#################### 2   INCIO  DE CLASE ThreadPing  ####################################################################
class ThreadPing(ThreadReport):
    """Threaded Pings"""
    def run(self):
        while True:
            myCommand = self._get() #maybe command should consist of a popen command list and a callback for that command
            if not myCommand or len(myCommand) != 2 or type(myCommand)!= type([]):
                print "%r"%myCommand
                raise Exception("command: %r"%myCommand)       
            cmdLst = myCommand[0]
            fnXf = myCommand[1]
            print cmdLst[-1]
            myOut = False
            thisCounter = 0
            while not myOut and thisCounter < 10:
                try:
                    thisCounter += 1
                    if type(cmdLst) != type([]):
                        raise Exception("need a list")
                    pipe = Popen(cmdLst, stdout=PIPE)
                    myOut = fnXf(pipe.communicate()[0])
                except Exception as e:
                    print "%s, %s"%(",".join(cmdLst), str(fnXf))
                    raise e
                    myOut = None
                    sleep(500)
            self._done()
            if myOut:
                self._put(myOut)
################## 2  FIN  DE CLASE  ThreadPing     ########################################################

############################ 3  INICIO DE CLASE myReport ####################################################
class myReport(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue
        self.total = 0
        self.lstOut = []
        
    def run(self):
        while True:
            try:
                lstOut = self.queue.get()
                self.total += 1
                if lstOut:
                        self.lstOut.append([lstOut[0],lstOut[3]])
                
            except Exception as e:
                print lstOut
            self.queue.task_done()

############################## 3  FIN DE CLASE  myReport ###################################################


############################################  4  inicio de bloque funcion doPing  ##################################
def doPing(q_hosts,q_report,someone):
    myHosts = someone
    dThreads = len(myHosts) if len(myHosts) < 1024 else 1024
    # print("Pinging %i Hosts\nusing %i threads:"%(len(myHosts),dThreads))
    #spawning pools of threads, and passing them the q_hosts instance 
    for i in range(dThreads):
        t = ThreadPing(q_hosts,q_report)
        t.setDaemon(True)
        print t
        t.start()
    #populate queue with data -if this were expensive (i/o bound), having the ability to work on the queue while it is populated is nice!
    for myInt, myhost in enumerate(myHosts):
        q_hosts.put([['ping','-c 3', myhost], lambda x: x.split("\n")])
    #now that is going, we only need one thread for summing
    myRep = myReport(q_report)
    myRep.setDaemon(True)
    myRep.start()
    #wait on the queues until everything has been processed     
    q_hosts.join()
    q_report.join()
    return dThreads, myRep.total, myRep.lstOut
    t.join()
    t.isAlive()
    #print t.status()
###########################################  4 fin de bloque funcion doPing ##################################################


###########################################  4.5 inicio bloque funcion DICCIONARIO ##################################################
remotos={'192.168.101.3':"IMACITA",'192.168.101.5':"ISPACAS",'192.168.101.7':"MINAS-MISKI",'192.168.101.9':"CHONTAL",'192.168.101.11':"COSPAN",
         '192.168.101.13':"HUILCATE",'192.168.101.15':"LA_BERMEJA",'192.168.101.17':"PUCARA",'192.168.101.19':"LLATA",'192.168.101.23':"CENTRAL_CEDRO_RICO",
         '192.168.101.25':"VIRA_VIRA",'192.168.101.27':"CHIRIACCO",'192.168.101.29':"VILLA_VIRGEN",'192.168.101.31':"PUERTO_INCA",'192.168.101.33':"RAURA",'192.168.101.35':"SELVA_DE_ORO",
         '192.168.101.37':"BACAS",'192.168.101.39':"RAJAN",'192.168.101.41':"ORELLANA",'192.168.101.43':"CAJAS_CANCHAQUE",'192.168.101.45':"CULEBREROS",
         '192.168.101.47':"HINTON",'192.168.101.49':"POTRERILLO",'192.168.101.51':"SICCEQUISTERIO",'192.168.101.53':"ALTO_CUNUMBAZA",'192.168.101.55':"BETANIA",
         '192.168.101.57':"SAN-MARTIN",'192.168.101.59':"SHAMBOYACU",'192.168.101.61':"TRES_UNIDOS",'192.168.101.63':"NUEVO_CHANCHAMAYO",'192.168.101.65':"YAUYOS-LIMA",
         '192.168.101.67':"COLASAY",'192.168.101.69':"SAN_LORENZO",'192.168.101.71':"CANAYRE",'192.168.101.73':"PUERTO_ESPERANZA",'192.168.101.75':"TAMBORAPA_PUEBLO",
         '192.168.101.77':"AMBATO_TAMBORAPA",'192.168.101.79':"SANTA_ROSA",'192.168.101.81':"PALMA_REAL",'192.168.101.83':"HUANCASANCOS",'192.168.101.95':"JERILLO",
         '192.168.101.105':"COCOCHO",'192.168.101.111':"PUENTECILLOS",'192.168.101.129':"TRAPICHE",'192.168.101.133':"JERILLO",'192.168.101.135':"LA_TORTUGA_PIURA"}

###########################################  4.5 fin bloque funcion DICCIONARIO ##################################################





############################################  5 inicio de funcion getPings   ######################################################
def getPings(algun):
    #build the Queues
    q_hosts = Queue()
    q_report = Queue() 
    start = time()
    dThreads, lTotal, lstOut = doPing(q_hosts,q_report,algun)
    eTime = time() - start
    
    for lstLine in lstOut:
                         
                         #print "ESTA ES LA SALIDA"+lstLine[1]
                         #print "ESTA    "+lstLine[0]  
                         if( (  ('Destination Host Unreachable')  in lstLine[1]) or ('100% packet loss') in lstLine[1]):
                                 print(" ENLACE  APAGADO ")+ lstLine[1]
                                  
                                 apagados.append(algun)
                                 algo = str(algun)
                                 algo = algo.lstrip("['")
                                 algo = algo.rstrip("']")
                                 #print "************************* oOo ***************************"                       
                                 
                             #   try:
                             #      s4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                             #   except socket.error, e:
                             #       print "Error creating socket no se formo el "
   
                             #   try:
                             #       s4.connect(('192.168.12.203',4000))
                             #   except socket.gaierror, e:
                             #       print "No se ubica al servidor escuchando----->: %s" % e
                             #   try:
                             #       s4.sendall("**"+"|SW3|"+"P6"+"|APAGADO|"+algo+"|0.0|0.0|0.0|%%")
                             #   except socket.error, e:
                             #       print "No se pudo enviar datos al servidor milk: %s" % e 
                                                                                                
                          
                         else  :   
                                  print("ENLACE  ACTIVO ") + lstLine[1]
                                  prendidos.append(algun) 
                                  dire = str(algun)
                                  dire = dire.lstrip("['")
                                  dire = dire.rstrip("']")
                                  octetos = dire.split(".")
                                  archi = str(octetos[3])
                                  remoto = int(archi)+1
                                  remoto = str(remoto)                              
                                  octetos[3] = remoto
                                  impar = str(octetos[0])+"."+str(octetos[1])+"."+str(octetos[2])+"."+str(octetos[3])
  
                                  #client(dire,80,"puerto usado",6)
                                  culebron ="snmpwalk "+dire+" -v1 1.3.6.1.4.1.6247.80.1.3.12.1 "
                                  culebron2 = '| grep  ".6247.80.1.3.12.1.1.2." | cut -d "." -f10 | sed "s/ Hex-STRING\://g" | tac'
                                  
                                  #pidetx = "snmpwalk "+dire+" -v1 1.3.6.1.4.1.6247.80.1.3.8.6.1.10.1  | cut -d ' ' -f4"
                                  #piderx ="snmpwalk "+dire+" -v1 1.3.6.1.4.1.6247.80.1.3.8.6.1.22.1  | cut -d ' ' -f4 "
                                  #pidelocal = "snmpwalk "+dire+" -v1 1.3.6.1.4.1.6247.80.1.3.2.5.0 | cut -d ' ' -f4"
                                  #pidebno  = "snmpwalk "+dire+" -v1 1.3.6.1.4.1.6247.80.1.3.5.1.0 | cut -d ' ' -f4 "  
                                  pidetempe = "snmpwalk "+impar+" -v1 1.3.6.1.4.1.6247.80.1.1.1.2.0 | cut -d ':' -f4"
                                  
                                  res1 = commands.getstatusoutput(culebron+culebron2)
                                  macs = str(res1)
                                  uno = macs.split()
                                  este = uno[1]
                                  este1 = este.split("'")
                                  este2 = este1[1]
                                  hora = commands.getstatusoutput("date")
                                  #tx = commands.getstatusoutput(pidetx)
                                  #rx = commands.getstatusoutput(piderx)
                                  #ebnoremoto = commands.getstatusoutput(pidebno)
                                  #ebnolocal = commands.getstatusoutput(pidelocal)
                                  temperatura = commands.getstatusoutput(pidetempe)
                                  tempe    = str(temperatura)
                                  tempe  =  tempe.split("'")
                                  tem  = tempe[1]                                   
                                  datazo = str(hora)   
                                                                
                                  data   = datazo.split("'")
                                  datito = data[1]
                                  print  datito
                                  fichero = open( '/mnt/flash/automata/TEMPERATURA/'+archi+".txt",'a' )
                                  fichero.write("MACS DE   "+str(dire)+" --> "+str(este2)+"   ----  TEMPERATURA  DE  :  "+impar+" ---->  "+str(tem)+" -- MARCA --  "+str(datito)+"  \n ")
                                  #fichero.write(str(res1)+"\n")
                                  #fichero.close
                                  print tempe
                                  #print "TX --------:"+str(tx)+"   RX -----:"+str(rx)+"  EBNOLOCAL -----:"+str(ebnolocal)+"  EBNOREMOTO ----:"+str(ebnoremoto) 
                                  #print  res1
                                  #if( int(este2) > 9 ):
                                  #         fichero2 = open('/mnt/flash/automata/TEMPERATURA/CANDIDATOS.txt','a' )
                                  #         fichero2.write( str(datito)+"|-----"+"TEMPERATURA--"+impar+"--:|  "+str(tem)+" |-----MACS LOCAL---- "+str(dire)+"  --->  "+str(este2)+" |  \n ")
                                  #         #fichero2.write(str(res1)+"\n")                                  
                                  #         fichero2.close
                                  if(  ('Timeout: No Response from ')  in tempe[1] ):
                                           tem = int(8)
                                           if remotos.has_key(impar):
                                               nombre2 = remotos.get(impar)
                                           else :
                                               nombre2 = impar
                                           claqueta2 =str(datito)
                                           fecha2 = claqueta2.split(" ")
                                           horale2 = str(fecha2[3])
                                           #if(fecha2[2]==" "):
                                           #           dia1 = fecha2[3]
                                           #else:
                                           #           dia1 = fecha2[2]

                                           dia1 = fecha2[2]
                                           menos2 = str(datito)
                                           me2 = menos2.split(" ")
                                           marquita2 = str(me2[3])
                                           mar2 = marquita2.split(":")
                                           year2 = str(me2[5])
                                           tempera2 = str(tem)
                                           print "*******************mar******"
                                           print fecha2[1]
                                           fichero4 = open('/mnt/flash/automata/AVISOS/'+str(dia1)+str(fecha2[1])+'NOCONTESTAN.txt','a' )                                     
                                           fichero4.write( me2[2]+" "+me2[1]+"  "+me2[4]+" "+mar2[0]+":"+mar2[1]+"   "+impar+"      "+nombre2+"  "+tempera2+"   "+"   \n ")                  

                                  if( int(tem) > 45 ):
                                           claqueta = str(datito)
                                           fecha = claqueta.split(" ")
                                           horale = str(fecha[3])
                                           #if(str(fecha[2])==" "):
                                           #          dia1 = fecha[3]
                                           #else: 
                                           #          dia1 = fecha[2]
                                           dia1 = fecha[2]
                                                                                                                            
                                           
                                           #print "mes "
                                           #print fecha[1]
                                           
                                           fichero3 = open('/mnt/flash/automata/AVISOS/'+str(dia1)+str(fecha[1])+'.txt','a' )
                                           if remotos.has_key(impar):
                                               nombre = remotos.get(impar)
                                           else :
                                               nombre = impar
                                           if( int(tem)>=100) :
                                              tem = int(1)
                                           menos = str(datito)
                                           me = menos.split(" ")
                                           marquita = str(me[3])
                                           print " esta es la marquita"
                                           print marquita
                                           mar = marquita.split(":")
                                           year = str(me[5])
                                           tempera = str(tem)
                                               
                                           
                                           fichero3.write( me[3]+" "+me[1]+"  "+me[4]+" "+mar[0]+":"+mar[1]+"   "+impar+"      "+nombre+"  "+tempera+"   "+"   \n ")
                                           fichero3.close              
                                  print  "MACS DE   "+str(dire)+"-->   "+str(este2)+"   ----  TEMPERATURA  DE  :  "+impar+" ----> "+str(tem)+" -- MARCA --  "+str(datito)     
            
                                    
                                  
                        
########################################  5 fin de bloque getPings #####################################################################


#######################  6  INICIO MODULO  cliente #################################
def client(ip, port, mensaje,puerto):
 try: 
    try:
            tubo = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, e:
            print "Error creating socket no se formo el "
 
    try:
            tubo.connect((ip,port))
    except socket.gaierror, e:
            print "No se ubica al servidor escuchando----->: %s" % e
    
    try:
            tubo.send("GET /status.htm HTTP/1.0\n\n") # Send request
            
    except socket.error, e:
            print "No se pudo enviar datos al servidor milk: %s" % e
         
    #time.sleep(0.25) # delays for 1 seconds
    print " MARCA  3 ------- "+ ip
    tubo = urllib.urlopen("http://monitor:1234@"+ip+"/status.htm")
    print " MARCA  4  ------"
    htmlSource = tubo.read()
    print "================================="
    marcaA = 0
    marcaAA = 0
    marcaB = 0
    marcaBB = 0
    marcaC = 0
    marcaCC = 0
    indiA = htmlSource.find("Remote Eb/No:")
    marcaA = htmlSource.count("td",indiA+15,indiA+35)
    marcaAA = htmlSource.find("<b>",indiA+20,indiA+50)
    datoA  = htmlSource[marcaAA+5:(marcaAA+12)]
    comparaA = datoA[0:5]
    #print comparaA
    
    if comparaA.isalnum():
           print("Esta caido el enlace")
           estado = "CAIDO"
    else  :
           print("Tiene valor ebno")
    
    indiB = htmlSource.find("Eb/No:")
    marcaB = htmlSource.count("td",indiB+15,indiB+35)
    marcaBB = htmlSource.find("<b>",indiB+20,indiB+50)
    datoB  = htmlSource[marcaBB+5:(marcaBB+12)]
    indiC = htmlSource.find("Signal Level:")
    marcaC = htmlSource.count("td",indiC+15,indiC+30)
    marcaCC = htmlSource.find("<b>",indiC+35,indiC+50)
    datoC = htmlSource[marcaCC+5:(marcaCC+10)]+" "+htmlSource[marcaCC+15:marcaCC+18]
    print mensaje 
    print "Eb/No  remoto ----  "+datoA
    print "Eb/No  Local -----  "+datoB
    print "Nivel de Signal---  "+datoC
    direccion = str(ip)
    try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, e:
            print "Error creating socket no se formo el "
    
    try:
            s.connect(('192.168.12.82',4000))
    except socket.gaierror, e:
          print "No se ubica al servidor escuchando----->: %s" % e
        
    try:
            s.sendall("**"+"|SW3|"+"P"+str(puerto)+"|ACTIVO|"+direccion+"|"+datoA+"|"+datoB+"|"+datoC+"|%%")
    except socket.error, e:
            print "No se pudo enviar datos al servidor milk: %s" % e
    
    
 finally:
     tubo.close()
####################### FINAL 6 MODULO  cliente #################################


######################### INICIO  7  CLASE  MANEJADOR  HILOS ###########################
class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    
    def handle(self):
        data = self.request.recv(1024)
        cur_thread = threading.current_thread()
        response = "%s: %s" %(cur_thread.name, data)
        self.request.sendall(response)
######################### FIN   7  CLASE  MANEJADOR  HILOS ###########################




class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    """Nothing to add here, inherited everything necessary from parents"""
    pass


if __name__ == "__main__":
 
    # Run server
    #server = ThreadedTCPServer((SERVER_HOST, SERVER_PORT), ThreadedTCPRequestHandler)
    #ip, port = server.server_address # retrieve ip address

    # Start a thread with the server -- one  thread per request
    #server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread exits
    #server_thread.daemon = True
    #server_thread.start()
    #print "El servidor esta corriendo en el hilo definido: %s"  %server_thread.name
    print "**********************************************************************************************************************************************************************"
    # Run clients
    indi = 0;
    
    i = 1
    while i < 2:
        for auxi1 in inscritos:      
                              cual=[]
                              cual.append(inscritos[indi])
                              getPings(cual)
                              indi= indi+1                          
                              i = i+1
        # print " ***********  PRENDIDOS -----"+str(prendidos)
        #print prendidos
        #print " ************  APAGADOS  -----"+str(apagados)
        #print apagados   
        indi = 0
        prendidos = []
        apagados = []
    
        
    
    

 





