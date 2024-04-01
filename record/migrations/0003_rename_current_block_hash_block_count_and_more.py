# Generated by Django 4.2.10 on 2024-04-01 12:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('record', '0002_record_block'),
    ]

    operations = [
        migrations.RenameField(
            model_name='block',
            old_name='current',
            new_name='hash',
        ),
        migrations.AddField(
            model_name='block',
            name='count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='block',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='record',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
