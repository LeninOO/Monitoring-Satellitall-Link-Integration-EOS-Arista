#----------------------
import os
import smtplib
import string
import email

from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
from email.Utils import formatdate
from email import Encoders

#_________________
def mandar_mail(
    pm_servidor_correo,
    pm_login_usuario,
    pm_login_password,
    pm_emisor_nombre,
    pm_emisor_correo,
    pm_receptor_nombre,
    pm_receptor_correo,
    pm_asunto,
    pm_archivo_texto,
    pm_archivo_html,
    pm_adjuntos = [],
    pm_acuse_recibo = False,
    pm_imagenes_embebidas = []):
    assert type(pm_adjuntos) == list
    assert type(pm_imagenes_embebidas) == list
    msgRaiz = MIMEMultipart('related')
    msgRaiz['From'] = pm_emisor_nombre + ' <' + pm_emisor_correo +'>'
    msgRaiz['To'] = pm_receptor_correo
    msgRaiz['Subject'] = pm_asunto
    msgRaiz['Date'] = formatdate(localtime = True)
    msgRaiz.preamble = '' #De momento, no lo uso
    msgRaiz.epilogue = '' #De momento, no lo uso

    if pm_acuse_recibo:
        msgRaiz['Disposition-Notification-To'] = pm_emisor_correo
 
    msgAlternativo = MIMEMultipart('alternative')
    msgRaiz.attach(msgAlternativo)

    msgTexto = MIMEText(pm_archivo_texto, 'plain', pm_encoding_cuerpo)
    msgAlternativo.attach(msgTexto)

    msgHtml = MIMEText(pm_archivo_html, 'html', pm_encoding_cuerpo)
    msgAlternativo.attach(msgHtml)

    for imagen in pm_imagenes_embebidas:
        archivo_imagen = open(imagen, 'rb')
        msgImage = MIMEImage(archivo_imagen.read())
        archivo_imagen.close()

        msgImage.add_header('Content-ID', '<' + imagen + '>')
        msgRaiz.attach(msgImage)

    for file in pm_adjuntos:
        adjunto = MIMEBase('application', "octet-stream")
        adjunto.set_payload(open(file, "rb").read())
        Encoders.encode_base64(adjunto)
        adjunto.add_header('Content-Disposition', 'attachment; filename 
= "%s"' %  os.path.basename(file))
        msgRaiz.attach(adjunto)

    servidor = smtplib.SMTP(pm_servidor_correo)
    servidor.ehlo()
    servidor.login(pm_login_usuario, pm_login_password)
    try:
        servidor.sendmail(pm_emisor_correo, pm_receptor_correo, 
msgRaiz.as_string())
        servidor.quit()
        resultado =  True
    except:
        resultado = False

    return(resultado)
