#!/usr/bin/env python
import os
import smtplib
import mimetypes
import time
import sys

from time import time, sleep
import commands
from email.MIMEMultipart import MIMEMultipart
from email.MIMEImage import MIMEImage
from email.Encoders import encode_base64
from email.MIMEText import MIMEText

#######################################  VARIABLES  DE INICIALIZACION ###########



#######################################  CABECERAS 2 INICIO #######################
msg = MIMEMultipart()
msg['From']="alertacaltec@gmail.com"
msg['To']="leopoldo.lenin@gmail.com"
#msg['Subject']="Alerta Lectura de Temperatura"

####################################### CABECERAS 2 FIN    #######################


#######################################  3 PROCESMIENTO INICIO ######################################

hora = commands.getstatusoutput("date")
datazo = str(hora)
data   = datazo.split("'")
datito = data[1]
claqueta = str(datito)
fecha = claqueta.split(" ")
mes = fecha[1]
peggy = 0
calabacita = 0
for bondy in fecha :
     if(bondy=="UTC"):
             calabacita = peggy
     peggy = peggy +1

dia = fecha[calabacita-2]
referencia = int(dia)
if ( referencia>=9):
      payaso = 3
else :
      payaso = 4

print fecha
mes = fecha[calabacita - payaso] 


print" Este es el dia "+dia
print" Este es el mes "+mes

tag = str(dia)+str(mes)
tag2 = str(dia)+" "+str(mes)

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
real  = tag+"ENVIA"+".txt"
estadis = tag+"ESTADISTICAS"+".txt"

msg['Subject']=str(dia)+"  "+str(mes)+" Temperatura de equipos remotos > 45"


#######################################  3 PROCESAMIENTO  FIN ###############################################






#######################################  4 ENVIO  INICIO  ########################### ###########

foto = open("/mnt/flash/automata/foto.png", "rb")
adjuntafoto = MIMEImage(foto.read())
adjuntafoto.add_header('Content-Disposition', 'attachment; filename =foto.png')
msg.attach(adjuntafoto)

msg.attach(MIMEText(' Estimados Ingenieros les enviamos la informacion de sites que sobrepasan los 45 Grados Centigrados,  Caltec','html'))





file = open("/mnt/flash/automata/AVISOS/"+real, "rb")
attach_image = MIMEText(file.read())
attach_image.add_header('Content-Disposition', 'attachment; filename = '+real)
msg.attach(attach_image)

file2 = open("/mnt/flash/automata/AVISOS/"+estadis, "rb")
attach_image2 = MIMEText(file2.read())
attach_image2.add_header('Content-Disposition', 'attachment; filename = '+estadis)
msg.attach(attach_image2)


mailServer = smtplib.SMTP('smtp.gmail.com',587)
mailServer.ehlo()
mailServer.starttls()
mailServer.ehlo()
mailServer.login("alertacaltec@gmail.com","Torata2016")


mailServer.sendmail("alertacaltec@gmail.com", "jhony.serva@telefonica.com", msg.as_string())
sleep(15)
mailServer.sendmail("alertacaltec@gmail.com", "juan.carrasco1607@gmail.com", msg.as_string())
sleep(15)
mailServer.sendmail("alertacaltec@gmail.com", "juan.arias@telefonica.com", msg.as_string())
sleep(15)
mailServer.sendmail("alertacaltec@gmail.com", "juan.olazabal@telefonica.com", msg.as_string())
sleep(15)
mailServer.sendmail("alertacaltec@gmail.com", "guillermo.robles@telefonica.com", msg.as_string())
sleep(15)
mailServer.sendmail("alertacaltec@gmail.com", "zenon.benites@telefonica.com", msg.as_string())
sleep(15)
mailServer.sendmail("alertacaltec@gmail.com", "luisroca@caltec.com.pe", msg.as_string())
sleep(15)
mailServer.sendmail("alertacaltec@gmail.com", "jreynapl@gmail.com", msg.as_string())
sleep(15)
mailServer.sendmail("alertacaltec@gmail.com", "aballesteros@caltec.com.pe", msg.as_string())
sleep(15)

mailServer.sendmail("alertacaltec@gmail.com", "leopoldo.lenin@gmail.com", msg.as_string())


mailServer.close()

#######################################  4  ENVIO  FIN  #####################################
