# Generated by Django 3.1.1 on 2021-02-14 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0018_auto_20210209_2355'),
    ]

    operations = [
        migrations.AddField(
            model_name='masters',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
