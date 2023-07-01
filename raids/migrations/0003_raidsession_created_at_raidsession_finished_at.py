# Generated by Django 4.2.2 on 2023-07-01 00:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('raids', '0002_alter_raidsession_action_log_alter_raidsession_bots'),
    ]

    operations = [
        migrations.AddField(
            model_name='raidsession',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='raidsession',
            name='finished_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
