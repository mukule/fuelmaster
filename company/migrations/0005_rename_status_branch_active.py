# Generated by Django 5.0.4 on 2024-04-28 05:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0004_branch_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='branch',
            old_name='status',
            new_name='active',
        ),
    ]
