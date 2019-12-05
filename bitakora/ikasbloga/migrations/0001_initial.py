# Generated by Django 2.0.7 on 2019-11-12 11:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('slug', models.SlugField(blank=True, help_text='Leave blank to have the URL auto-generated from the title.', max_length=2000, null=True, verbose_name='URL')),
            ],
            options={
                'verbose_name_plural': 'Levels',
                'verbose_name': 'Level',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('slug', models.SlugField(blank=True, help_text='Leave blank to have the URL auto-generated from the title.', max_length=2000, null=True, verbose_name='URL')),
                ('year', models.IntegerField()),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ikasbloga.Level')),
            ],
            options={
                'verbose_name_plural': 'Rooms',
                'verbose_name': 'Room',
            },
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('slug', models.SlugField(blank=True, help_text='Leave blank to have the URL auto-generated from the title.', max_length=2000, null=True, verbose_name='URL')),
            ],
            options={
                'verbose_name_plural': 'Schools',
                'verbose_name': 'School',
            },
        ),
        migrations.AddField(
            model_name='room',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ikasbloga.School'),
        ),
    ]
