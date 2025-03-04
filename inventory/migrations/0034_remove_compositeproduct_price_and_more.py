# Generated by Django 5.0.4 on 2024-05-12 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0033_alter_product_image_compositeproduct'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='compositeproduct',
            name='price',
        ),
        migrations.AddField(
            model_name='compositeproduct',
            name='buying_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='compositeproduct',
            name='selling_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
