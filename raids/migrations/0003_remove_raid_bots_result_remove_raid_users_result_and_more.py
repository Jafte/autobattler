# Generated by Django 4.2.11 on 2024-05-16 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('raids', '0002_raid_robots'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='raid',
            name='bots_result',
        ),
        migrations.RemoveField(
            model_name='raid',
            name='users_result',
        ),
        migrations.AddField(
            model_name='raid',
            name='bots_state',
            field=models.JSONField(blank=True, default=list, verbose_name='bots state'),
        ),
        migrations.AddField(
            model_name='raid',
            name='config_state',
            field=models.JSONField(blank=True, default=dict, verbose_name='config state'),
        ),
        migrations.AddField(
            model_name='raid',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='raid',
            name='users_state',
            field=models.JSONField(blank=True, default=list, verbose_name='users state'),
        ),
    ]
