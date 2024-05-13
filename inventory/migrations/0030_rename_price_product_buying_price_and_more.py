# Generated by Django 5.0.4 on 2024-05-12 06:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0005_rename_status_branch_active'),
        ('inventory', '0029_purchasesaccount_branch_salesaccount_branch'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='price',
            new_name='buying_price',
        ),
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, default='default_product_image.jpg', null=True, upload_to='product_images'),
        ),
        migrations.AddField(
            model_name='product',
            name='purchases_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.purchasesaccount'),
        ),
        migrations.AddField(
            model_name='product',
            name='sales_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.salesaccount'),
        ),
        migrations.AddField(
            model_name='product',
            name='selling_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='warehouse',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.warehouse'),
        ),
        migrations.AlterField(
            model_name='product',
            name='branch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='company.branch'),
        ),
    ]
