#!/usr/bin/python
# -*- coding: utf-8 -*-

# Enviar correo Gmail con Python
# www.pythondiario.com

import smtplib

fromaddr = 'leninorihuela@caltec.com.pe'
toaddrs  = 'leopoldo.lenin@gmail.com'
msg = 'Correo enviado utilizano Python + smtplib en www.pythondiario.com'


# Datos
username = 'torata2961@gmail.com'
password = 'torata'

# Enviando el correo

#server = smtplib.SMTP('204.84.244.49:587')
#server.starttls()
#server.login(username,password)
#server.sendmail(fromaddr, toaddrs, msg)
for x in range(1, 11):
        print repr(x).rjust(2), repr(x*x).rjust(3),
        # notar la coma al final de la linea anterior
        print repr(x*x*x).rjust(4), repr(x).rjust(5), repr(x).rjust(6),repr(x).rjust(7),repr(x).rjust(8),repr(x).rjust(9),repr(x).rjust(10)

server.quit()
