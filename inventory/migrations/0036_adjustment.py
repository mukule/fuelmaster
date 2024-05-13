# Generated by Django 5.0.4 on 2024-05-12 18:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0005_rename_status_branch_active'),
        ('inventory', '0035_alter_compositeproduct_components'),
    ]

    operations = [
        migrations.CreateModel(
            name='Adjustment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref_number', models.CharField(max_length=100)),
                ('reason', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('quantity', models.FloatField()),
                ('adjusted_quantity', models.FloatField()),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.branch')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.product')),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.warehouse')),
            ],
        ),
    ]
