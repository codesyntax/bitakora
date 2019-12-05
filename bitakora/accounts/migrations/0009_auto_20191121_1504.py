# Generated by Django 2.0.7 on 2019-11-21 15:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ikasbloga', '0003_auto_20191121_1504'),
        ('accounts', '0008_auto_20191112_1155'),
    ]

    operations = [
        migrations.AddField(
            model_name='bitakorauser',
            name='code',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='bitakorauser',
            name='school',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ikasbloga.School'),
        ),
    ]
