# Generated by Django 3.1.1 on 2021-02-03 03:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='masters',
            name='greeting',
            field=models.TextField(blank=True, verbose_name='краткое приветствие'),
        ),
    ]
