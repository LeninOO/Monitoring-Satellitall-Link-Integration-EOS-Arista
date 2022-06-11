
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

horale = str(fecha[3])
horale = horale[0:2]
turno ="M"
periodo ="Manana" 
if( int(horale)>=16) :
      turno ="N"
if( (int(horale)>8) and (int(horale)< 16)):
      turno ="T"
if( int(horale)<=8):
     turno ="M"
archivo = tag+".txt"

if(turno=="M"):
      periodo = "Manana"
if(turno=="T"):
      periodo = "Tarde"
if(turno=="N"):
      periodo = "Noche"





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

while( actual<= fin):

   LIBRO = {}
   for q in calidos:
       LIBRO[q] =""
   
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
               if( (str(w)==str(nombre2))and(h == actual)  ):
                                  jarrito.append(grados)               
               cursor2 = cursor2+1
           LIBRO[w]= jarrito
   
   #print LIBRO['COCOCHO'] 
   
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
    

#print GENERAL
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
print "  VALORES PROMEDIO CADA HORA DE MONITOREO   "+dia+" "+mes+" INTERVALO : "+str(ini)+" HORAS   A  : "+str(fin)+" HORAS"
print "#########################################################################################"
print "                                                      "
print " Cada valor representa una hora de monitoreo, si el valor es cero"
print " Significa que el site no ha registrado una lectura > 45 grados esa hora"
print "                                                   "
print " Por Ejemplo :   ('BETANIA',[0,0,0,0,47,46,46,47,50,46,0]                                    "
print " Con periodo de muestreo entre 8-18 horas,  significa que 8,9,10,11, no tuvo valor mayor 45  "
print " a las 12 tuvo valor promedio 47 grados, a la  13 y 14 valor promedio de  46 grados, 15 horas"
print " un valor promedio de 47 grados,  y asi sucesivamente , si tiene un valor menor a 45 su   "
print " valor figura como '0' .                                                               " 
print "                                                                                      "
print "                                                                                      "
print "                                                                                      "
print "********************************************************************************************"




for  h in calidos:
    #print calidos[h]+IMPRIME[h]
    print (h,IMPRIME[h]) 

#nsajito ="ALERTA DEL"+str(fecha[2]+" "+fecha[0]+" TURNO "+periodo
#print mensajito
#cadenita = "cat"+" /mnt/flash/automata/AVISOS/"+archivo+" | -i -s["+periodo+"] email  leninorihuela@caltec.com.pe"
#entrada = "mnt/flash/automata/AVISOS/"+archivo
#salida = "mnt/flash/automata/AVISOS/"+"ENVIO"+archivo
#commands.getstatusoutput(
#archivo4=open('/mnt/flash/automata/AVISOS/'+archivo,'r')
#espejo=archivo4.readlines()
  

#for (clave, valor) in mi_diccionario.items():
     



