# Generated by Django 3.1.1 on 2021-02-03 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_masters_master_specialization'),
    ]

    operations = [
        migrations.AddField(
            model_name='services',
            name='service_id',
            field=models.CharField(blank=True, max_length=128, verbose_name='id текста на странице'),
        ),
    ]
