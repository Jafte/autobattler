# Generated by Django 4.2.11 on 2024-05-10 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='robot_options',
            field=models.JSONField(default=dict, verbose_name='robot options'),
        ),
    ]
