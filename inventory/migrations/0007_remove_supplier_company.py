# Generated by Django 5.0.4 on 2024-04-24 08:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_supplier'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='supplier',
            name='company',
        ),
    ]
