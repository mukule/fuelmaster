# Generated by Django 5.0.4 on 2024-05-13 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0040_adjustmentreason_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adjustment',
            name='adjusted_quantity',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
