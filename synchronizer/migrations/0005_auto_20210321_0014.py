# Generated by Django 3.1.7 on 2021-03-20 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('synchronizer', '0004_auto_20210320_1010'),
    ]

    operations = [
        migrations.AddField(
            model_name='recording',
            name='slug',
            field=models.SlugField(blank=True),
        ),
        migrations.AlterField(
            model_name='recording',
            name='identifier',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterUniqueTogether(
            name='recording',
            unique_together={('project', 'identifier')},
        ),
    ]