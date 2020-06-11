# MESSAGES.WARNINGS
PERFIL_INCOMPLETO = 'Para poder realizar un pedido es necesario que confirmes tu correo y completes tu perfil, ' \
                    '<a href=\'/perfil/\'>completa tu perfil aqui</a>'

# MESSAGES.ERRORS
LOGIN_INVALIDO = "Correo de cuenta o contraseña invalidos, por favor intenta de nuevo <br> ¿Olvidaste tu contraseña ? <strong><a href='/perfil/genera-pwd/'> <i class='fa fa-sign-in-alt'></i> Genera una nueva</a></strong>"
IMG_DEMACIADO_GRANDE = "La imagen que estas tratando de cargar excede el tamaño maximo de 1500x1500 pixeles y 500Kbs"
SIN_EXISTENCIA = 'Lo sentimos, actualmente no tenemos existencias de este producto.'

# INFO ERROS
CARRO_VACIO = 'Aun no tienes ningun producto en tu carro, intenta agregar algun producto de tu preferencia'

# CHOICES.ESTADOS
ESTADOS_MEXICO = (
    ('Distrito Federal', 'Distrito Federal'),
    ('Jalisco', 'Jalisco'),
    ('Michoacan', 'Michoacan'),
)

ESTADO_ORDEN_CHOICES = (
    ('TENTATIVA', 'TENTATIVA'),
    ('PENDIENTE PAGO', 'PENDIENTE PAGO'),
    ('PAGADO', 'PAGADO'),
    ('ENVIADO', 'ENVIADO'),
    ('ENTREGADO', 'ENTREGADO'),
    ('CANCELADO', 'CANCELADO'),
    ('DEVUELTO', 'DEVUELTO'),
)

# PREFERENCIAS DE PAGO
PREFERENCIA_PAGO_CHOICES = (
            ('MERCADO PAGO', 'MERCADO PAGO'),
            ('PAYPAL', 'PAYPAL'),
            ('TRANSFERENCIA BANCARIA', 'TRANSFERENCIA BANCARIA'),
        )

# UPLOAD SIZE
# 2.5MB - 2621440
IMG_MAX_UPLOAD_SIZE = 2621440

#EMAIL GLOBAL DE NOTIFICACIONES ECHANGARRO
EMAIL_GLOBAL = 'notificaciones.tanquemania@gmail.com'