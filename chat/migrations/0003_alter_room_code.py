# Generated by Django 4.2.4 on 2023-09-05 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_room_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='code',
            field=models.CharField(max_length=8, unique=True),
        ),
    ]
