# Generated by Django 4.2.11 on 2024-05-02 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('robots', '0002_robot_heal_robot_max_damage_robot_min_damage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='robot',
            name='heal',
        ),
        migrations.RemoveField(
            model_name='robot',
            name='max_damage',
        ),
        migrations.RemoveField(
            model_name='robot',
            name='max_health',
        ),
        migrations.RemoveField(
            model_name='robot',
            name='min_damage',
        ),
        migrations.AddField(
            model_name='robot',
            name='agility',
            field=models.SmallIntegerField(default=10),
        ),
        migrations.AddField(
            model_name='robot',
            name='strength',
            field=models.SmallIntegerField(default=15),
        ),
        migrations.AlterField(
            model_name='robot',
            name='status',
            field=models.CharField(choices=[('DEAD', 'Нет сигнала'), ('WAITING', 'В режиме ожидании'), ('ON_MISSION', 'Исполняет задание')], default='WAITING', max_length=64),
        ),
    ]