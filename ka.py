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




def getPings(algun):
    q_hosts = Queue()
    q_report = Queue() 
    start = time()
    dThreads, lTotal, lstOut = doPing(q_hosts,q_report,algun)
    eTime = time() - start
    
    for lstLine in lstOut:
                         
                           
                         if( (  ('Destination Host Unreachable')  in lstLine[1]) or ('100% packet loss') in lstLine[1]):
                                 print(" ENLACE  APAGADO ")+ lstLine[1]
                                  
                                 apagados.append(algun)
                                 algo = str(algun)
                                 algo = algo.lstrip("['")
                                 algo = algo.rstrip("']")
                                 
                            
                                                                                                
                          
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
  
                                  culebron ="snmpwalk "+dire+" -v1 1.3.6.1.4.1.6247.80.1.3.12.1 "
                                  culebron2 = '| grep  ".6247.80.1.3.12.1.1.2." | cut -d "." -f10 | sed "s/ Hex-STRING\://g" | tac'
                                  
                                  
                                  pidetempe = "snmpwalk "+impar+" -v1 1.3.6.1.4.1.6247.80.1.1.1.2.0 | cut -d ':' -f4"
                                  
                                  res1 = commands.getstatusoutput(culebron+culebron2)
                                  macs = str(res1)
                                  uno = macs.split()
                                  este = uno[1]
                                  este1 = este.split("'")
                                  este2 = este1[1]
                                  hora = commands.getstatusoutput("date")
                                  temperatura = commands.getstatusoutput(pidetempe)
                                  tempe    = str(temperatura)
                                  tempe  =  tempe.split("'")
                                  tem  = tempe[1]                                   
                                  datazo = str(hora)   
                                                            
                                  data   = datazo.split("'")
                                  
                                  datito = data[1]
                                  
                                  fichero = open( '/mnt/flash/automata/TEMPERATURA/'+archi+".txt",'a' )
                                  fichero.write("MACS DE   "+str(dire)+" --> "+str(este2)+"   ----  TEMPERATURA  DE  :  "+impar+" ---->  "+str(tem)+" -- MARCA --  "+str(datito)+"  \n ")
                                  print tempe
                                  if(  ('Timeout: No Response from ')  in tempe[1] ):
                                           tem = int(8)
                                           if remotos.has_key(impar):
                                               nombre2 = remotos.get(impar)
                                           else :
                                               nombre2 = impar
                                           claqueta2 =str(datito)
                                           
                                           fecha2 = claqueta2.split(" ")
                                           
                                           horale2 = str(fecha2[2])
                                           
                                           
                                           dia1 = fecha2[3]
                                           menos2 = str(datito)
                                           me2 = menos2.split(" ")
                                           peggy = 0
                                           calabacita = 0
                                           for bondy in me2 :
                                                    
                                                 if(bondy=="UTC"):
                                                               calabacita = peggy
                                                 peggy = peggy +1
                                                                                         
                                                                                                                       
                                           marquita2 = str(me2[calabacita-1])
                                           mar2 = marquita2.split(":")
                                           year2 = str(me2[calabacita+1])
                                           tempera2 = str(tem)
                                                                                                          
                                           referencia = int(fecha2[calabacita -2])
                                           if ( referencia>=9):
                                                        payaso = 3
                                           else :
                                                        payaso = 4

                                           fichero4 = open('/mnt/flash/automata/AVISOS/'+str(fecha2[calabacita-2])+str(fecha2[calabacita-payaso])+'NOCONTESTAN.txt','a' )                                     
                                           fichero4.write( me2[calabacita-2]+" "+me2[calabacita-payaso]+"  "+mar2[0]+":"+mar2[1]+"   "+impar+"      "+nombre2+"  "+tempera2+"   "+"   \n ")                  

                                  if( int(tem) > 45 ):
                                           claqueta = str(datito)
                                           fecha = claqueta.split(" ")
                                           horale = str(fecha[3])
                                           
                                           peggy1 = 0
                                           calabacita1 = 0
                                           for bondy1 in fecha :
                                                 if(bondy1=="UTC"):
                                                              calabacita1 = peggy1
                                                 peggy1 = peggy1 +1
                                          
                                           dia1 = fecha[calabacita1-2]
                                           referencia2 = int(dia1)
                                           if ( referencia2>=9):
                                                              payaso2 = 3
                                           else :
                                                              payaso2 = 4
                                                         

                                          

               	                           fichero3 = open('/mnt/flash/automata/AVISOS/'+str(dia1)+str(fecha[calabacita1-payaso2])+'.txt','a' )
                                           if remotos.has_key(impar):
                                               nombre = remotos.get(impar)
                                           else :
                                               nombre = impar
                                           if( int(tem)>=100) :
                                              tem = int(1)
                                           menos = str(datito)
                                           me = menos.split(" ")
                                           marquita = str(me[calabacita1 -1])
                                           mar = marquita.split(":")
                                           year = str(me[calabacita1+1])
                                           tempera = str(tem)
                                                 
                                           
                                           fichero3.write( me[calabacita1-2]+" "+me[calabacita1-payaso2]+" "+me[calabacita1+1]+"  "+mar[0]+":"+mar[1]+"   "+impar+"      "+nombre+"  "+tempera+"   "+"   \n ")
                                           fichero3.close              
                                  print  "MACS DE   "+str(dire)+"-->   "+str(este2)+"   ----  TEMPERATURA  DE  :  "+impar+" ----> "+str(tem)+" -- MARCA --  "+str(datito)     
            
                                    
                                  
                        
########################################  5 fin de bloque getPings #####################################################################

if __name__ == "__main__":
 
    
    print "**********************************************************************************************************************************************************************"
    
    indi = 0;
    inscritos =['10.119.25.54']
    
    i = 1
    while i < 2:
        for auxi1 in inscritos:      
                              cual=[]
                              cual.append(inscritos[indi])
                              getPings(cual)
                              indi= indi+1                          
                              i = i+1
        indi = 0
        prendidos = []
        apagados = []

