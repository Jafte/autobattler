# Generated by Django 4.2.11 on 2024-05-01 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('robots', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='robot',
            name='heal',
            field=models.SmallIntegerField(default=10),
        ),
        migrations.AddField(
            model_name='robot',
            name='max_damage',
            field=models.SmallIntegerField(default=100),
        ),
        migrations.AddField(
            model_name='robot',
            name='min_damage',
            field=models.SmallIntegerField(default=10),
        ),
    ]