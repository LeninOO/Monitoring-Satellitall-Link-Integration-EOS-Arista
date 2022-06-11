
#!/usr/bin/env python



import os
from socket  import * 
import threading
import SocketServer

from jsonrpclib import Server
import urllib
import  socket
import time
import sys
import time
from time import time, sleep
import commands





hora = commands.getstatusoutput("date")
datazo = str(hora) 
data   = datazo.split("'")
datito = data[1]
claqueta = str(datito)
fecha = claqueta.split(" ")
horale = str(fecha[4])
horale = horale[0:2]
turno ="M"
if( int(horale)>=16) :
      turno ="N"
if( (int(horale)>=8) and (int(horale)<= 16)):
      turno ="T"
if( int(horale)<= 8):
     turno ="M"
#print fecha[1]
#print "dia "+ fecha[3]
#print "hora "+fecha[4]
archivo = fecha[3]+fecha[1]+turno+".txt"
#print  archivo
fichero = open( '/mnt/flash/automata/AVISOS/'+archivo,'r' )
pasada = fichero.readlines()
original = len(pasada)
limit = original - 1
valla = limit
cursor2 = 1
maceta = "  "
puntos=[]
while( cursor2 < valla ):
   temporal2 = pasada[cursor2]  
   otro2 = temporal2.split(" ")
   print otro2[6]
   lugar = otro2[6]
   lug = str(lugar) 
   for x in puntos:
      if( lug!=puntos[x]):
         puntos.insert(cursor2,lug)
         print puntos
   #print puntos
   maceta = lug
   cursor2 = cursor2 +1
print puntos

        


     



