# Generated by Django 3.1.1 on 2021-02-07 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0009_auto_20210207_0038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contacts',
            name='client_name',
            field=models.CharField(max_length=10, verbose_name='имя клиента'),
        ),
    ]
