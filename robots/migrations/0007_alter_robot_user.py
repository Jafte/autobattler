# Generated by Django 4.2.11 on 2024-05-20 01:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('robots', '0006_remove_robot_epitaph_remove_robot_killed_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='robot',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='robots', to=settings.AUTH_USER_MODEL),
        ),
    ]
