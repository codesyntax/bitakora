# Generated by Django 2.0.7 on 2019-11-21 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ikasbloga', '0002_auto_20191112_1159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='level',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Level name'),
        ),
        migrations.AlterField(
            model_name='room',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Room name'),
        ),
        migrations.AlterField(
            model_name='school',
            name='name',
            field=models.CharField(max_length=200, verbose_name='School name'),
        ),
    ]
