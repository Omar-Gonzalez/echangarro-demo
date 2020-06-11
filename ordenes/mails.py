import os
import datetime
import sendgrid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
from dotenv import load_dotenv
from echangarro.globals import EMAIL_GLOBAL
load_dotenv(verbose=True)


def notifica_creacion_de_orden(orden):
    productos = ''
    for producto in orden.productos:
        productos = f'{productos}<p>({producto.cantidad}) - {producto.producto.nombre} - SubTotal: <b>${producto.sub_total}</b></p>'
    message = Mail(
        from_email=EMAIL_GLOBAL,
        to_emails=[orden.user.username, EMAIL_GLOBAL],
    )
    message.dynamic_template_data = {
            'numero_de_orden': orden.pk,
            'total_orden': orden.total_con_envio,
            'nombre_cliente': orden.user.perfil.nombre,
            'preferencia_de_pago': orden.preferencia_de_pago,
            'productos': productos
    }
    message.template_id = 'd-0bcb54e14b7c4d6abb2261e801154bc4'
    try:
        print(os.environ.get('SENDGRID_API_KEY'))
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
    except Exception as e:
        print(e)
