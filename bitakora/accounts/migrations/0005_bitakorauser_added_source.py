# Generated by Django 2.0.7 on 2019-11-11 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_bitakorauser_usertype'),
    ]

    operations = [
        migrations.AddField(
            model_name='bitakorauser',
            name='added_source',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
