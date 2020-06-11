import os
import datetime
import sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
from dotenv import load_dotenv
load_dotenv(verbose=True)
from echangarro.globals import EMAIL_GLOBAL


def notificacion_error(codigo, path):
    fecha_y_tiempo = datetime.datetime.now()
    message = Mail(
        from_email=EMAIL_GLOBAL,
        to_emails=[EMAIL_GLOBAL],
        subject=f'error codigo {codigo} en tanquemania.com',
        html_content=f'Se registro un error {codigo} en tanquemania en path: {path} \n- {fecha_y_tiempo.strftime("%Y-%m-%d %H:%M:%S")}')
    try:
        print(os.environ.get('SENDGRID_API_KEY'))
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
    except Exception as e:
        print(e)


def notificacion_500(path):
    fecha_y_tiempo = datetime.datetime.now()
    message = Mail(
        from_email=EMAIL_GLOBAL,
        to_emails=[EMAIL_GLOBAL],
        subject='error codigo 500',
        html_content=f'Se registro un error 500 en tanquemania.com en path: {path} \n- {fecha_y_tiempo.strftime("%Y-%m-%d %H:%M:%S")}')
    try:
        print(os.environ.get('SENDGRID_API_KEY'))
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
    except Exception as e:
        print(e)
