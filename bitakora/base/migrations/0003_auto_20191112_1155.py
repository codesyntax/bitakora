# Generated by Django 2.0.7 on 2019-11-12 11:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20160413_1647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='featured_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='photologue.Photo', verbose_name='Featured Image'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='header_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='photologue.Photo'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='license',
            field=models.CharField(choices=[('cc-by-sa', 'CC-BY-SA'), ('copyright', 'Copyright')], default='cc-by-sa', max_length=200, verbose_name='License'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='template',
            field=models.CharField(choices=[('one-page-wonder.css', 'One page wonder'), ('minimalist-blog.css', 'Minimalist')], default='one-page-wonder.css', max_length=200, verbose_name='Template'),
        ),
    ]
