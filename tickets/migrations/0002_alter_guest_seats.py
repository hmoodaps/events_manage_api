# Generated by Django 5.1.1 on 2024-09-15 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guest',
            name='seats',
            field=models.JSONField(blank=True, default=list),
        ),
    ]
