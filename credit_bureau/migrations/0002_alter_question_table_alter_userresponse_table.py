# Generated by Django 5.1.3 on 2024-11-12 06:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('credit_bureau', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='question',
            table='question',
        ),
        migrations.AlterModelTable(
            name='userresponse',
            table='user_response',
        ),
    ]
