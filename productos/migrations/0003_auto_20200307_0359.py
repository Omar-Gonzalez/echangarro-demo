# Generated by Django 2.2.2 on 2020-03-07 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0002_auto_20200304_0359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='escala',
            field=models.CharField(blank=True, choices=[('1/20', '1/20'), ('1/24', '1/24'), ('1/32', '1/32'), ('1/35', '1/35'), ('1/48', '1/48'), ('1/72', '1/72'), ('1/150', '1/150'), ('1/350', '1/350'), ('1/700', '1/700'), ('1/3000', '1/3000')], max_length=110, null=True),
        ),
    ]
