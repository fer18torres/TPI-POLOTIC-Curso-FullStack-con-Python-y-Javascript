# Generated by Django 3.2.4 on 2021-06-29 09:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AppKAA', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Articulos',
            new_name='Articulo',
        ),
        migrations.RenameModel(
            old_name='Clientes',
            new_name='Cliente',
        ),
    ]