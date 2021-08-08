# Generated by Django 3.1.1 on 2021-02-14 06:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0023_auto_20210214_0639'),
    ]

    operations = [
        migrations.AddField(
            model_name='contacts',
            name='action',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='mainapp.actionsnews', verbose_name='акция'),
        ),
        migrations.AlterField(
            model_name='contacts',
            name='date_field',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.workdays', verbose_name='дата услуги'),
        ),
        migrations.AlterField(
            model_name='contacts',
            name='time_field',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.time', verbose_name='время услуги'),
        ),
        migrations.AlterField(
            model_name='masters',
            name='master_services',
            field=models.ManyToManyField(blank=True, to='mainapp.Services', verbose_name='услуги мастера'),
        ),
    ]
