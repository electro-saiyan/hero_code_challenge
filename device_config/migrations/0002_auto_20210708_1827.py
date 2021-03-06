# Generated by Django 3.2.5 on 2021-07-08 18:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('device_config', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='deviceconfig',
            name='active',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='deviceconfig',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='deviceconfig',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
