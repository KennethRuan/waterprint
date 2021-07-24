# Generated by Django 3.2.5 on 2021-07-24 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='total_footprint',
        ),
        migrations.AddField(
            model_name='profile',
            name='friends',
            field=models.ManyToManyField(blank=True, null=True, to='frontend.Profile'),
        ),
    ]
