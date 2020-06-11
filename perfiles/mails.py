import os
import datetime
import sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
from dotenv import load_dotenv
from echangarro.globals import EMAIL_GLOBAL
load_dotenv(verbose=True)


def confirma_usuario_con(email, host, uuid):
    message = Mail(
        from_email=EMAIL_GLOBAL,
        to_emails=[email, EMAIL_GLOBAL],
    )
    message.dynamic_template_data = {
            'tema': f'Bienvenido {email} a {host}, La Bodega del Hobby',
            'mensaje': f"¡Gracias por registrate en TANQUEMANIA la Bodega del Hobby! <br/> Por favor confirma tu correo, <a href='https://{host}/perfil/confirma-correo/{uuid}'>sigue esta liga &raquo;<a/>"
    }
    message.template_id = 'd-44160c651dcd4d299cbf2174ade1bd1c'
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
    except Exception as e:
        print(e)


def notificacion_nuevo_usuario(email):
    fecha_y_tiempo = datetime.datetime.now()
    message = Mail(
        from_email=EMAIL_GLOBAL,
        to_emails=EMAIL_GLOBAL,
        subject=f'Notificacion de nuevo usuario {email}',
        html_content=f'- Se registro nuevo usuario con email {email} \n- Se le envio correo de confirmacion al mismo \n- {fecha_y_tiempo.strftime("%Y-%m-%d %H:%M:%S")}')
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
    except Exception as e:
        print(e)


def genera_nueva_contraseña(email, host, uuid):
    message = Mail(
        from_email=EMAIL_GLOBAL,
        to_emails=[email, EMAIL_GLOBAL],
    )
    message.dynamic_template_data = {
            'tema': 'Genera tu nueva contraseña en TANQUEMANIA',
            'mensaje': f'Haz solicitado restablecer tu contraseña de echangarro \n- Por favor sigue la siguiente liga para generar una nueva contraseña: http://{host}/perfil/nuevo-pwd/{uuid}/'
    }
    message.template_id = 'd-44160c651dcd4d299cbf2174ade1bd1c'
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
    except Exception as e:
        print(e)