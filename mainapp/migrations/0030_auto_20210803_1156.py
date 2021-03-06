# Generated by Django 3.2.3 on 2021-08-03 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0029_portfolio_img_3'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecordTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.CharField(choices=[('9:00', '9:00'), ('10:00', '10:00'), ('11:00', '11:00'), ('12:00', '12:00'), ('13:30', '13:30'), ('15:00', '15:00'), ('16:00', '16:00'), ('17:00', '17:00'), ('18:00', '18:00'), ('19:00', '19:00')], max_length=32, verbose_name='часы работы')),
                ('master', models.CharField(max_length=128)),
                ('date', models.CharField(max_length=64)),
                ('is_free', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'Время записи к специалисту',
            },
        ),
        migrations.AlterModelOptions(
            name='time',
            options={'verbose_name_plural': 'Время'},
        ),
    ]
