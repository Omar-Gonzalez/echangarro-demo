# Generated by Django 2.2.2 on 2020-03-07 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordenes', '0002_auto_20200305_0056'),
    ]

    operations = [
        migrations.AddField(
            model_name='orden',
            name='guia_de_envio',
            field=models.CharField(blank=True, max_length=640, null=True),
        ),
        migrations.AlterField(
            model_name='orden',
            name='estado',
            field=models.CharField(choices=[('TENTATIVA', 'TENTATIVA'), ('PENDIENTE PAGO', 'PENDIENTE PAGO'), ('PAGADO', 'PAGADO'), ('ENVIADO', 'ENVIADO'), ('ENTREGADO', 'ENTREGADO'), ('CANCELADO', 'CANCELADO'), ('DEVUELTO', 'DEVUELTO')], default='INICIADO', max_length=110),
        ),
        migrations.AlterField(
            model_name='orden',
            name='preferencia_de_pago',
            field=models.CharField(choices=[('MERCADO PAGO', 'MERCADO PAGO'), ('PAYPAL', 'PAYPAL'), ('TRANSFERENCIA BANCARIA', 'TRANSFERENCIA BANCARIA')], default='MERCADO LIBRE', max_length=110),
        ),
    ]
