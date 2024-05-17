# Generated by Django 4.2.11 on 2024-05-16 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('raids', '0003_remove_raid_bots_result_remove_raid_users_result_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='raid',
            name='status',
            field=models.CharField(choices=[(0, 'New'), (1, 'In Progress'), (2, 'Finished')], default=0, max_length=50, verbose_name='status'),
        ),
    ]
