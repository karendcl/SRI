# Generated by Django 5.0.1 on 2024-02-22 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Document', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
