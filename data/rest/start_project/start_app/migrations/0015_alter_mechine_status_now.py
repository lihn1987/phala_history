# Generated by Django 4.0.4 on 2022-05-09 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('start_app', '0014_alter_mechine_start_time_alter_mechine_status_now'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mechine',
            name='status_now',
            field=models.CharField(default='', help_text='当前状态', max_length=100, verbose_name='当前状态'),
        ),
    ]
