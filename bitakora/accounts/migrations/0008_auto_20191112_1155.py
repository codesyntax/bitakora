# Generated by Django 2.0.7 on 2019-11-12 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20191111_1457'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bitakorauser',
            options={'verbose_name': 'Blog erabiltzailea', 'verbose_name_plural': 'Blog erabiltzaileak'},
        ),
        migrations.AlterField(
            model_name='bitakorauser',
            name='usertype',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Normal'), (2, 'Student'), (3, 'Teacher')], default=0),
        ),
    ]
