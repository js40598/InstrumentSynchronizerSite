# Generated by Django 3.1.7 on 2021-03-29 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('synchronizer', '0006_auto_20210328_2054'),
    ]

    operations = [
        migrations.AddField(
            model_name='recording',
            name='cut',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='recording',
            name='synchronized',
            field=models.BooleanField(default=False),
        ),
    ]