
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
import math



publica = " "
hora = commands.getstatusoutput("date")
datazo = str(hora) 
data   = datazo.split("'")
datito = data[1]
claqueta = str(datito)
fecha = claqueta.split(" ")
mes = fecha[1]
dia = fecha[3]
#print fecha
#print" Este es el dia "+dia
#print" Este es el mes "+mes
tag = str(dia)+str(mes)
tag2 = str(dia)+" "+str(mes)
ruta ="/mnt/flash/automata/AVISOS/"+tag+".txt"
mudos ="/mnt/flash/automata/AVISOS/"+tag+"NOCONTESTAN.txt"
horale = str(fecha[3])
horale = horale[0:2]
turno ="M"
zorro = dict()
lamb = dict()
mudos2 = open(mudos,'r')
mudos3 = mudos2.readlines()
sordos =[]
cuales = len(mudos3)
cuales = cuales - 2
campana = cuales
incremental = 2
while( incremental < cuales ):
       recibe = mudos3[incremental]
       eslabon = str(recibe)
       eslava = eslabon.split(" ")
       paredes = eslava[5]
       horita = paredes.split(":")
       nombre1 = eslava[14]
       repetidos1 = 0
       for a in sordos:
            if(a==nombre1):
                repetidos1 = repetidos1 + 1
       if(repetidos1<=0):
                sordos.append(nombre1)
                zorro[nombre1]= paredes        
       incremental = incremental+1

ultimos =[]
while( campana > 1 ):
       recibe1 = mudos3[campana]
       eslabon1 = str(recibe1)
       eslava1 = eslabon1.split(" ")
       paredes1 = eslava1[5]
       horita1 = paredes1.split(":")
       nombre1 = eslava1[14]
       parecido = 0
       for a in ultimos:
            if(a==nombre1):
                parecido = parecido + 1
       if(parecido<=0):
                ultimos.append(nombre1)
                lamb[nombre1]= paredes1
       campana  = campana - 1

calidos=["  "]
cursor1 = 1
ficha1 = open(ruta,'r' )
lineas1=ficha1.readlines()
limite1 = len(lineas1)
lim = int(limite1)
lim = lim - 2
tempo = lineas1[3]
tem =tempo.split(" ")
inicio = tem[5] 
inici = inicio.split(":")
ini  = int(inici[0])
tempo2 = lineas1[lim]
tem2 = tempo2.split(" ")
final = tem2[5]
fina = final.split(":")
fin = int(fina[0])
intervalo = fin - ini
intervalo = intervalo+1

while( cursor1 < lim ):
       temporal1 = lineas1[cursor1]
       cadena1 = str(temporal1)
       cade1 = cadena1.split(" ")
       nombre = cade1[14]    
       largo = len(calidos)
       repetidos = 0
       for indice in calidos: 
            if(indice==nombre):   
                repetidos = repetidos + 1       
       if(repetidos<=0):
                calidos.append(nombre)  
       cursor1 = cursor1+1






ficha2 = open( ruta,'r' )
lineas2=ficha2.readlines()
limite2 = len(lineas2)
lim2 = int(limite2)
lim2 = lim2 - 2
anchoperiodo = 1
pericote = 1
GENERAL ={}
IMPRIME ={}
actual =ini
LIBRO = {}
for q in calidos:
       LIBRO[q] =""

while( actual<= fin):
   for w in calidos:
           cursor2 = 1
           jarrito = [] 
           while( cursor2 < lim2):
               temporal2 = lineas2[cursor2]
               cadena2 = str(temporal2)
               cade2 = cadena2.split(" ")
               ipcita =cade2[8]
               nombre2 = cade2[14]
               grados = cade2[17]
               horacio = cade2[5]
               hora = horacio.split(":")
               #print hora
               ho = hora[0]
               h = int(ho)
               diario = cade2[1]
               if( (str(w)==str(nombre2))and(h == actual) ):
                                  jarrito.append(grados)               
               cursor2 = cursor2+1
             
           LIBRO[w]= jarrito
           
   
   muestra={}
   for j in calidos:
         sumatoria = 0
         for z in LIBRO[j]:
                  sumatoria = sumatoria+int(z) 
         marcas=len(LIBRO[j])
         if(marcas>0):
               promedio = (sumatoria)/marcas
               muestra.setdefault(j,promedio)
               promedio = 0     
         else:
               
               muestra.setdefault(j,0)
  
   GENERAL.setdefault(pericote,muestra)
   
   pericote = pericote+1
   actual = actual+1

#print  LIBRO
#print GENERAL[1].get('COCOCHO')
IMPRIME ={}


for v in calidos:
          otra=[]
          publica = v
          p = 1          
          while( p <= intervalo):
                    aux1 = GENERAL[p].get(publica)
                    otra.append(aux1)
                    p = p+1
                      
          
          IMPRIME.setdefault(v,otra) 
          
#print IMPRIME
print "#########################################################################################"
print "  TEMPERATURA PROMEDIO CADA HORA  "+dia+" "+mes+" INTERVALO : "+str(ini)+" HORAS   A  : "+str(fin)+" HORAS"
print "#########################################################################################"
print "                                                      "
print " Cada valor representa una hora de monitoreo, si el valor es cero"
print " Significa que el site no ha registrado una lectura > 45 grados esa hora"
print "  o  que el site no contesta, y debe verificar la lista de site que no contestan "


print "                                                                   "                           

for  h in calidos:
    
    print " %s______%s " %(h,IMPRIME[h]) 
print "======================================================================="
print "                  "
print "                  "
print "==============  SITES REMOTOS QUE NO CONTESTAN AL  "+dia+" "+mes+"====="
print "      "
for clave,valor in zorro.iteritems():
            print " %s________inicio %s   fin %s" %(clave,valor,lamb.get(clave))

    
print "======================================================================="
print "                                                                                                                            "
print "                                                                                                                            "

